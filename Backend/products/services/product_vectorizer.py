from sklearn.preprocessing import MinMaxScaler
import numpy as np

# 상품 벡터화 함수
def vectorize_product(option, rate_min=1.0, rate_max=5.0):
    base = option.intr_rate or 0
    max_r = option.intr_rate2 or base
    gap = max_r - base

    return [
        gap / (rate_max - rate_min + 1e-6),    # 조건 난이도
        option.save_trm / 36,                  # 장기성
        1.0 if option.intr_rate_type_nm == "복리" else 0.0,
        max_r / rate_max                       # 보상 기대
    ]
