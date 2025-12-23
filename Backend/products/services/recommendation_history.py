from products.models import RecommendationHistory

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
