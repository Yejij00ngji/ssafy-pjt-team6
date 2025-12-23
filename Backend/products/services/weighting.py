# 클러스터 가중치 계산 함수
def cluster_weight(cluster_prob, alpha=0.7):
    return alpha + (1 - alpha) * cluster_prob