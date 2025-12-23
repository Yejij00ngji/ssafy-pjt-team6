from users.services.user_vectorizer import vectorize_user
from products.services.product_vectorizer import vectorize_product
from products.services.similarity import cosine_similarity
from products.services.weighting import cluster_weight
from products.services.cluster_distribution import get_top_products_by_cluster
from products.services.confidence import calculate_confidence
from products.models import ProductOption

def recommend_products(user, top_n=5):
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

        scored.append({
            'product_option': option,
            'score': final_score,
            'similarity': sim,
            'cluster_weight': weight
        })
        all_scores.append(final_score)

    for r in scored:
        r["confidence"] = calculate_confidence(r["score"], all_scores)

    return sorted(scored, key=lambda x: x['score'], reverse=True)[:top_n]
