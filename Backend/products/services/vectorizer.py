from sklearn.preprocessing import MinMaxScaler
import numpy as np
from users.models import FinancialProfile

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


# 상품 벡터와 상대 비교를 위한 사용자 벡터화
def vectorize_user(profile):
    total_assets = profile.balance_amt + profile.invest_eval_amt + 1

    risk_preference = profile.invest_eval_amt / total_assets
    liquidity_preference = profile.withdrawable_amt / total_assets
    long_term_preference = profile.expense_growth_rate
    reward_seeking = 1 - profile.expense_to_income_ratio

    return [
        risk_preference,
        liquidity_preference,
        long_term_preference,
        reward_seeking
    ]
