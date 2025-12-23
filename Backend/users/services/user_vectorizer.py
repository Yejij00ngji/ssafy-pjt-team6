import numpy as np
from sklearn.preprocessing import MinMaxScaler
from users.models import FinancialProfile

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

