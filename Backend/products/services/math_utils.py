import numpy as np

# 코사인 유사도 계산 함수
# 절대값보다 방향성이 중요
def cosine_similarity(u, v):
    u = np.array(u)
    v = np.array(v)
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-6)

# 신뢰도 점수 계산
def calculate_confidence(target_score, all_scores):
    """
    추천 결과의 상대적 신뢰도 (0~1)
    """
    lower_count = sum(1 for s in all_scores if s < target_score)
    return round(lower_count / len(all_scores), 2)

# 클러스터 가중치 계산 함수
def cluster_weight(cluster_prob, alpha=0.7):
    return alpha + (1 - alpha) * cluster_prob
