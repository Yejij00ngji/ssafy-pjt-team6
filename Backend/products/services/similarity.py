# 코사인 유사도 계산 함수
# 절대값보다 방향성이 중요

import numpy as np

def cosine_similarity(u, v):
    u = np.array(u)
    v = np.array(v)
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-6)

