from users.services.user_vectorizer import vectorize_user
from products.services.product_vectorizer import vectorize_product
from products.services.similarity import cosine_similarity
from products.services.weighting import cluster_weight
from products.services.cluster_distribution import get_top_products_by_cluster
from products.services.confidence import calculate_confidence
from ai.services.recommendation_explainer import explain_recommendation

from products.models import ProductOption
from concurrent.futures import ThreadPoolExecutor # 병렬 처리 (계산 빠르게)

def recommend_products(user, top_n=3):
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
        all_scores.append(final_score)

        scored.append({
            'product_option': option,
            'score': final_score,
            'similarity': sim,
            'cluster_weight': weight
        })

    for r in scored:
        r["confidence"] = calculate_confidence(r["score"], all_scores)
        
    # 🔥 3단계: 먼저 "정렬"하고 "자르기" (여기가 포인트!)
    top_recommendations = sorted(scored, key=lambda x: x['score'], reverse=True)[:top_n]
        
    # 🔥 4. AI 설명 병렬 호출 (속도 향상의 핵심!)
    # max_workers는 동시에 보낼 요청 수입니다.
    with ThreadPoolExecutor(max_workers=top_n) as executor:
        # 각 추천 상품에 대해 explain_recommendation 함수를 동시에 실행
        reasons = list(executor.map(lambda r: explain_recommendation(user, r), top_recommendations))

    # 5. 생성된 설명을 결과에 매칭
    for i, r in enumerate(top_recommendations):
        r["reason"] = reasons[i]

    return top_recommendations