# OpenAI API 호출
from openai import OpenAI
from django.conf import settings
from ai.prompts import RECOMMEND_EXPLAIN_PROMPT

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def explain_recommendation(user, rec):
    # 호출 전 확인
    print(f"--- OpenAI API 호출 시작 (모델: gpt-4o-mini) ---")
    
    try:
    
        prompt = RECOMMEND_EXPLAIN_PROMPT.format(
            cluster=user.financialprofile.cluster_label,
            similarity=round(rec["similarity"], 2),
            cluster_weight=round(rec["cluster_weight"], 2),
            confidence_percent=int(rec["confidence"] * 100),
            # base_rate=rec["product_option"].intr_rate,
            # max_rate=rec["product_option"].intr_rate2,
            # term=rec["product_option"].save_trm,
            # rate_type=rec["product_option"].intr_rate_type_nm
            
            # 아래 4줄이 핵심 수정 포인트입니다!
            base_rate=rec.get("intr_rate"), 
            max_rate=rec.get("intr_rate2", rec.get("intr_rate")), # 데이터가 없을 경우 대비
            term=rec.get("save_trm"),
            rate_type=rec.get("intr_rate_type_nm", "단리")
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        print(f"--- OpenAI API 호출 성공! 응답 길이: {len(response.choices[0].message.content)} ---")

        return response.choices[0].message.content

    except Exception as e:
            # 실패 시 에러 내용 출력
            print(f"!!! OpenAI API 호출 실패: {str(e)} !!!")
            return "AI 추천 사유를 생성하는 중에 문제가 발생했습니다."
