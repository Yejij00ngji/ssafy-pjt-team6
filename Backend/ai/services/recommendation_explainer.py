import requests
import json
import os
from django.conf import settings

# prompts: MYDATA / SURVEY 템플릿이 있으면 사용, 없으면 기존 하나로 폴백
try:
    from ai.prompts import (
        RECOMMEND_EXPLAIN_PROMPT,
        RECOMMEND_EXPLAIN_PROMPT_MYDATA,
        RECOMMEND_EXPLAIN_PROMPT_SURVEY,
    )
except Exception:
    from ai.prompts import RECOMMEND_EXPLAIN_PROMPT
    RECOMMEND_EXPLAIN_PROMPT_MYDATA = RECOMMEND_EXPLAIN_PROMPT
    RECOMMEND_EXPLAIN_PROMPT_SURVEY = RECOMMEND_EXPLAIN_PROMPT

# .env에서 설정값 가져오기 (settings.py에 등록되어 있다면 settings.GMS_API_KEY 등으로 사용 가능)
GMS_KEY = os.getenv('GMS_API_KEY')
LLM_URL = os.getenv('LLM_ENDPOINT')
LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4o')
EMBEDDING_URL = os.getenv('EMBEDDING_ENDPOINT')


def get_embedding(text):
    """
    사용자가 입력한 텍스트(자연어)를 벡터로 변환
    """
    headers = {
        "Authorization": f"Bearer {GMS_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "text-embedding-3-small",
        "input": text
    }

    try:
        response = requests.post(EMBEDDING_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()['data'][0]['embedding']
    except Exception as e:
        print(f"Embedding Error: {e}")
        return None


def explain_recommendation(user, rec, user_query=None, is_mydata=True):
    """
    LLM을 호출하여 {reason, report, nudge}를 반환합니다.
    - user: Django User instance (optional financialprofile)
    - rec: dict, 상품/추천 메타 (fin_prdt_nm, intr_rate, intr_rate2, save_trm, similarity, cluster_weight, confidence 등)
    - user_query: optional 자연어 의도
    - is_mydata: True(동의자, 실제 수치 사용), False(설문 기반)
    반환: dict {"reason": str, "report": str, "nudge": str}
    """

    # 안전한 기본값
    default_response = {
        "reason": "데이터를 기반으로 선정된 맞춤형 상품입니다.",
        "report": "현재 자산 상황에서 가장 안정적인 수익을 기대할 수 있습니다.",
        "nudge": "더 늦기 전에 오늘부터 자산 관리를 시작해보세요!"
    }

    # 프로필/수치 수집 (민감 정보는 로그에 직접 노출하지 않음)
    profile = getattr(user, 'financialprofile', None)

    # 선택할 프롬프트 템플릿
    prompt_template = RECOMMEND_EXPLAIN_PROMPT_MYDATA if is_mydata else RECOMMEND_EXPLAIN_PROMPT_SURVEY

    # 값 준비 (template에 맞는 키들)
    try:
        # product fields (rec may contain different keys)
        product_name = rec.get("fin_prdt_nm") or rec.get("product_name") or "추천상품"
        base_rate = rec.get("intr_rate")
        max_rate = rec.get("intr_rate2", base_rate)
        term = rec.get("save_trm")
        rate_type = rec.get("intr_rate_type_nm", "단리")
        similarity = rec.get("similarity", 0)
        cluster_weight = rec.get("cluster_weight", 0)
        confidence_percent = int((rec.get("confidence", 0) or 0) * 100)

        if is_mydata and profile:
            annual_income = getattr(profile, 'annual_income_amt', None)
            total_assets = (getattr(profile, 'balance_amt', 0) or 0) + (getattr(profile, 'invest_eval_amt', 0) or 0)
            cluster = getattr(profile, 'cluster_name', None) or getattr(profile, 'cluster_label', '미분류')

            # prompt 변수 매핑
            prompt = prompt_template.format(
                cluster=cluster,
                annual_income=annual_income if annual_income is not None else "정보없음",
                total_assets=total_assets,
                user_query=user_query if user_query else "없음",
                product_name=product_name,
                base_rate=base_rate,
                max_rate=max_rate,
                term=term,
                rate_type=rate_type,
                similarity=round(similarity, 2),
                cluster_weight=round(cluster_weight, 2),
                confidence_percent=confidence_percent
            )
        else:
            # survey path: 덜 민감한/범위 기반 필드 제공
            # annual_income_range 추정 혹은 폴백 텍스트
            annual_income_range = rec.get('annual_income_range') or "알 수 없음"
            cluster = rec.get('cluster_name') or (getattr(profile, 'cluster_name', None) or "설문 기반 페르소나")

            prompt = prompt_template.format(
                cluster=cluster,
                annual_income_range=annual_income_range,
                user_query=user_query if user_query else "없음",
                product_name=product_name,
                base_rate=base_rate,
                max_rate=max_rate,
                term=term,
                similarity=round(similarity, 2),
                cluster_weight=round(cluster_weight, 2),
                confidence_percent=confidence_percent
            )

    except Exception as e:
        print(f"Prompt build error: {e}")
        return default_response

    headers = {
        "Authorization": f"Bearer {GMS_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "당신은 금융 분석가이며 반드시 JSON으로 응답합니다."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.35,
        "max_tokens": 750
    }

    try:
        print(f"--- LLM 호출 (is_mydata={is_mydata}) 시작 ---")
        # 민감 데이터는 로그에 직출하지 않음; 대신 cluster/상품명 정도만 로깅
        safe_log = {
            "cluster": (getattr(profile, 'cluster_name', None) or getattr(profile, 'cluster_label', None)) if profile else rec.get('cluster_name'),
            "product": product_name,
            "is_mydata": is_mydata
        }
        print("LLM 호출 메타:", safe_log)

        response = requests.post(LLM_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        content = response.json()['choices'][0]['message']['content']
        ai_result = json.loads(content)
        print(f"--- LLM 호출 성공 ---")
        # 보장된 키를 반환하도록 후처리
        return {
            "reason": ai_result.get("reason") or default_response["reason"],
            "report": ai_result.get("report") or default_response["report"],
            "nudge": ai_result.get("nudge") or default_response["nudge"]
        }

    except Exception as e:
        print(f"!!! LLM 호출 실패: {str(e)} !!!")
        return default_response