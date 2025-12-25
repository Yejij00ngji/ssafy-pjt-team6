from products.services.vectorizer import vectorize_product, vectorize_user
from products.services.cluster_distribution import get_top_products_by_cluster
from products.services.math_utils import calculate_confidence, cosine_similarity, cluster_weight
from ai.services.recommendation_explainer import explain_recommendation, get_embedding

from products.models import ProductOption, RecommendationHistory

from concurrent.futures import ThreadPoolExecutor # 병렬 처리 (계산 빠르게)

def recommend_products(user, top_n=3, user_query=None):
    profile = user.financialprofile
    user_vec = vectorize_user(profile)
    # 1. 사용자 쿼리 임베딩 (검색어가 있을 때만)
    query_vec = get_embedding(user_query) if user_query else None

    cluster_products = get_top_products_by_cluster(profile.cluster_label)
    cluster_prob_map = {
        p['product_option_id']: p['ratio']
        for p in cluster_products
    }


    scored = []
    # 1단계: 모든 상품에 대해 마이데이터 유사도(Base Score)만 계산 (API 호출 X)
    for option in ProductOption.objects.all():
        product_vec = vectorize_product(option)
        sim = cosine_similarity(user_vec, product_vec)
        weight = cluster_weight(cluster_prob_map.get(option.id, 0.01))
        
        scored.append({
            'product_option': option,
            'base_score': sim * weight,
            'similarity': sim,
        })

    # 2단계: 마이데이터 점수 높은 상위 20개만 후보(Candidates)로 선정
    candidates = sorted(scored, key=lambda x: x['base_score'], reverse=True)[:20]

    # 3단계: 후보 20개에 대해서만 자연어 유사도(Semantic Score) 계산
    query_vec = get_embedding(user_query) if user_query else None
    all_final_scores = []

    for item in candidates:
        final_score = item['base_score']
        
        if query_vec:
            # 2. 🔥 [핵심] 20개의 임베딩을 '동시에' 요청 (병렬 처리)
            def fetch_semantic_score(item):
                opt = item['product_option']
                text = f"{opt.product.fin_prdt_nm} {opt.product.etc_note}"
                prod_emb = get_embedding(text)
                if prod_emb:
                    sem_sim = cosine_similarity(query_vec, prod_emb)
                    item['score'] = (item['base_score'] * 0.7) + (sem_sim * 0.3)
                else:
                    item['score'] = item['base_score']
                return item

            # 최대 20개의 쓰레드를 열어 한꺼번에 API 요청을 보냅니다.
            with ThreadPoolExecutor(max_workers=20) as executor:
                candidates = list(executor.map(fetch_semantic_score, candidates))
        else:
            for item in candidates:
                item['score'] = item['base_score']

        # 🔥 [핵심 수정] confidence 계산을 위해 모든 후보의 score 리스트 추출
        all_final_scores = [c['score'] for c in candidates]
        
        # 2. 각 candidate에 confidence 키 추가
        for c in candidates:
            # calculate_confidence 함수가 정의되어 있어야 합니다.
            c["confidence"] = calculate_confidence(c["score"], all_final_scores)

        # 3. 최종 정렬 및 상위 N개 추출 (이제 confidence가 포함됨)
        top_recommendations = sorted(candidates, key=lambda x: x['score'], reverse=True)[:top_n]

        # 4. AI 분석 병렬 호출
        with ThreadPoolExecutor(max_workers=top_n) as executor:
            reasons = list(executor.map(lambda r: explain_recommendation(user, r, user_query), top_recommendations))

        for i, r in enumerate(top_recommendations):
            r["ai_analysis"] = reasons[i]

        return top_recommendations

    # all_scores = []

    # # 최적화: 쿼리마다 DB 접근을 줄이기 위해 select_related 사용 권장
    # options = ProductOption.objects.select_related('product').all()

    # for option in options:
    #     # 1. 마이데이터 기반 기본 점수
    #     product_vec = vectorize_product(option)
    #     sim = cosine_similarity(user_vec, product_vec)

    #     cluster_prob = cluster_prob_map.get(option.id, 0.01)
    #     weight = cluster_weight(cluster_prob)

    #     # 기초 점수
    #     final_score = sim * weight
            
    #     # 2. [핵심] 임베딩 기반 시맨틱 유사도 가산점
    #     if query_vec:
    #         # 상품명과 설명을 합쳐서 임베딩 (실제 서비스에선 이 값을 DB에 미리 저장해두는게 베스트!)
    #         product_text = f"{option.product.fin_prdt_nm} {option.product.etc_note}"
    #         product_text_vec = get_embedding(product_text)
            
    #         if product_text_vec:
    #             semantic_sim = cosine_similarity(query_vec, product_text_vec)
    #             # 마이데이터 점수 70% + 자연어 검색 점수 30% 비율로 혼합
    #             final_score = (final_score * 0.7) + (semantic_sim * 0.3)

    #     all_scores.append(final_score)

    #     scored.append({
    #         'product_option': option,
    #         'score': final_score,
    #         'similarity': sim,
    #         'cluster_weight': weight,
    #         # gms explainer에 필요한 데이터 미리 매칭
    #         'fin_prdt_nm': option.product.fin_prdt_nm,
    #         'intr_rate': option.intr_rate,
    #         'intr_rate2': option.intr_rate2,
    #         'save_trm': option.save_trm,
    #     })

    # for r in scored:
    #     r["confidence"] = calculate_confidence(r["score"], all_scores)
        
    # 🔥 3단계: 먼저 "정렬"하고 "자르기" (여기가 포인트!)
    # top_recommendations = sorted(scored, key=lambda x: x['score'], reverse=True)[:top_n]
        
    # 🔥 4. AI 설명 병렬 호출 (속도 향상의 핵심!)
    # max_workers는 동시에 보낼 요청 수입니다.
    # with ThreadPoolExecutor(max_workers=top_n) as executor:
    #     # 각 추천 상품에 대해 explain_recommendation 함수를 동시에 실행
    #     reasons = list(executor.map(lambda r: explain_recommendation(user, r, user_query), top_recommendations))

    # # 5. 생성된 설명을 결과에 매칭
    # # 이제 reasons는 JSON(dict) 형태
    # for i, r in enumerate(top_recommendations):
    #     # 이제 r["reason"]에는 dict{"reason", "report", "nudge"} 전체가 들어갑니다.
    #     r["ai_analysis"] = reasons[i]

    # return top_recommendations


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
