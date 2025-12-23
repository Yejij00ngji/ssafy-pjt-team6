from django.db.models import Count
from products.models import Subscription

# 클러스터별 상품 가입 분포 조회
def get_cluster_product_distribution(cluster_label):
    return (
        Subscription.objects
        .filter(
            user__financialprofile__cluster_label=cluster_label,
            is_active=True
        )
        .values('product_option_id')
        .annotate(subscribe_count=Count('id'))
        .order_by('-subscribe_count')
    )

# 비율로 변환 (같은 성향의 사용자 중 42%가 이 상품을 선택함)
def normalize_distribution(dist_qs):
    total = sum(d['subscribe_count'] for d in dist_qs) + 1
    return [
        {
            'product_option_id': d['product_option_id'],
            'ratio': d['subscribe_count'] / total
        }
        for d in dist_qs
    ]

# 상위 n개 후보 상품 추출 (아직 개인화 전)
def get_top_products_by_cluster(cluster_label, top_n=5):
    dist = get_cluster_product_distribution(cluster_label)
    return normalize_distribution(dist[:top_n])
