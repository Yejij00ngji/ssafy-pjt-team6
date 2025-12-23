# OpenAI API 호출
from openai import OpenAI
from django.conf import settings
from ai.prompts import RECOMMEND_EXPLAIN_PROMPT

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def explain_recommendation(user, rec):
    prompt = RECOMMEND_EXPLAIN_PROMPT.format(
        cluster=user.financialprofile.cluster_label,
        similarity=round(rec["similarity"], 2),
        cluster_weight=round(rec["cluster_weight"], 2),
        confidence_percent=int(rec["confidence"] * 100),
        base_rate=rec["product_option"].intr_rate,
        max_rate=rec["product_option"].intr_rate2,
        term=rec["product_option"].save_trm,
        rate_type=rec["product_option"].intr_rate_type_nm
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content
