from products.services.vectorizer import vectorize_product, vectorize_user
from products.services.cluster_distribution import get_top_products_by_cluster
from products.services.math_utils import calculate_confidence, cosine_similarity, cluster_weight
from ai.services.recommendation_explainer import explain_recommendation

from products.models import ProductOption
from concurrent.futures import ThreadPoolExecutor # 병렬 처리 (계산 빠르게)

def recommend_products(user, top_n=3, user_query=None):
    profile = user.financialprofile
    user_vec = vectorize_user(profile)

    cluster_products = get_top_products_by_cluster(profile.cluster_label)
    cluster_prob_map = {
        p['product_option_id']: p['ratio']
        for p in cluster_products
    }

    scored = []
    all_scores = []

    for option in ProductOption.objects.all():
        product_vec = vectorize_product(option)
        sim = cosine_similarity(user_vec, product_vec)

        cluster_prob = cluster_prob_map.get(option.id, 0.01)
        weight = cluster_weight(cluster_prob)

        final_score = sim * weight

        # 자연어 입력 가산점 로직 (초간단 버전)
        if user_query:
            # 상품명이나 특이사항에 검색어가 포함되면 가산점 부여 (예: +0.2점)
            target_text = f"{option.product.fin_prdt_nm} {option.product.etc_note}"
            if user_query in target_text:
                final_score += 0.2

        all_scores.append(final_score)

        scored.append({
            'product_option': option,
            'score': final_score,
            'similarity': sim,
            'cluster_weight': weight,
            # gms explainer에 필요한 데이터 미리 매칭
            'fin_prdt_nm': option.product.fin_prdt_nm,
            'intr_rate': option.intr_rate,
            'intr_rate2': option.intr_rate2,
            'save_trm': option.save_trm,
        })

    for r in scored:
        r["confidence"] = calculate_confidence(r["score"], all_scores)
        
    # 🔥 3단계: 먼저 "정렬"하고 "자르기" (여기가 포인트!)
    top_recommendations = sorted(scored, key=lambda x: x['score'], reverse=True)[:top_n]
        
    # 🔥 4. AI 설명 병렬 호출 (속도 향상의 핵심!)
    # max_workers는 동시에 보낼 요청 수입니다.
    with ThreadPoolExecutor(max_workers=top_n) as executor:
        # 각 추천 상품에 대해 explain_recommendation 함수를 동시에 실행
        reasons = list(executor.map(lambda r: explain_recommendation(user, r, user_query), top_recommendations))

    # 5. 생성된 설명을 결과에 매칭
    # 이제 reasons는 JSON(dict) 형태
    for i, r in enumerate(top_recommendations):
        # 이제 r["reason"]에는 dict{"reason", "report", "nudge"} 전체가 들어갑니다.
        r["ai_analysis"] = reasons[i]

    return top_recommendations

from products.models import RecommendationHistory

# 추천 상품 기록하기 (db)
def save_recommendations(user, profile, recommendations):
    histories = []

    for rec in recommendations:
        histories.append(
            RecommendationHistory(
                user=user,
                product_option=rec["product_option"],
                score=rec["score"],
                confidence=rec["confidence"],
                cluster_label=profile.cluster_label,
            )
        )

    RecommendationHistory.objects.bulk_create(histories)
    return histories
