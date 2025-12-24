import requests
import json
import os
from django.conf import settings
from ai.prompts import RECOMMEND_EXPLAIN_PROMPT

# .env에서 설정값 가져오기 (settings.py에 등록되어 있다면 settings.GMS_API_KEY 등으로 사용 가능)
GMS_KEY = os.getenv('GMS_API_KEY')
LLM_URL = os.getenv('LLM_ENDPOINT') # https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions
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
        # GMS 임베딩 엔드포인트 호출
        response = requests.post(
            EMBEDDING_URL, 
            headers=headers, 
            json=payload, 
            timeout=10
        )
        response.raise_for_status()
        return response.json()['data'][0]['embedding']
    except Exception as e:
        print(f"Embedding Error: {e}")
        return None

def explain_recommendation(user, rec, user_query=None):
    """
    기존 추천 사유 생성을 넘어, 통합 AI 리포트(사유, 리포트, 넛지)를 생성합니다.
    """
    print(f"--- GMS API 호출 시작 (모델: {LLM_MODEL}) ---")
    
    # 프롬프트
    prompt = RECOMMEND_EXPLAIN_PROMPT.format(
            cluster=user.financialprofile.cluster_label,
            # 입력값이 없으면 "기본 금융 페르소나 분석"으로 대체
            user_query=user_query if (user_query and user_query.strip()) else "현재 페르소나에 최적화된 자산 관리",
            product_name=rec.get("fin_prdt_nm"),
            # 넛지 근거
            similarity=round(rec.get("similarity", 0), 2),
            cluster_weight=round(rec.get("cluster_weight", 0), 2),
            confidence_percent=int(rec.get("confidence", 0) * 100),
            # 상품 구조
            base_rate=rec.get("intr_rate"), 
            max_rate=rec.get("intr_rate2", rec.get("intr_rate")),
            term=rec.get("save_trm"),
            rate_type=rec.get("intr_rate_type_nm", "단리")
    )

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
        "response_format": { "type": "json_object" }, # JSON 모드 활성화
        "temperature": 0.4
    }

    try:
        response = requests.post(LLM_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
            
        content = response.json()['choices'][0]['message']['content']
        print(f"--- GMS API 호출 성공! ---")
            
        # JSON 문자열을 파이썬 딕셔너리로 변환
        return json.loads(content)

    except Exception as e:
        print(f"!!! GMS API 호출 실패: {str(e)} !!!")
        # 실패 시 기본 구조 반환 (에러 방지)
        return {
            "reason": "데이터를 기반으로 선정된 맞춤형 상품입니다.",
            "report": "현재 자산 상황에서 가장 안정적인 수익을 기대할 수 있습니다.",
            "nudge": "더 늦기 전에 오늘부터 자산 관리를 시작해보세요!"
        }