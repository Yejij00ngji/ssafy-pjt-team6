# 마이데이터 연동/분석 핵심 로직
# 사용자가 버튼을 클릭하면 즉시 가상 데이터 생성하는 로직
import random
import numpy as np
from .models import FinancialProfile
from datetime import date

def simulate_mydata_linking(user_profile):
    # 1. User 모델의 birth_date를 활용한 나이 계산
    birth_date = user_profile.user.birth_date
    if birth_date:
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    else:
        age = 30 # 폴백(Fallback) 값

    # 2. 나이 기반 자산 생성 로직 (기존과 동일)
    if age < 30:
        mean_income, mean_asset, investment_weight = 35000000, 20000000, 0.3
    elif age < 45:
        mean_income, mean_asset, investment_weight = 55000000, 150000000, 0.5
    else:
        mean_income, mean_asset, investment_weight = 70000000, 400000000, 0.2
        
    # 2. 정규분포를 활용한 가상 데이터 생성 (현실성 확보)
    # 실제 연봉(annual_income_amt) 생성
    user_profile.annual_income_amt = int(np.random.normal(mean_income, mean_income*0.2))
    
    # [표준 항목: balance_amt] 총 잔액 (연봉의 일정 비율이 자산으로 쌓였다고 가정)
    total_assets = int(np.random.normal(mean_asset, mean_asset*0.3))
    user_profile.balance_amt = int(total_assets * (1 - investment_weight))
    
    # [표준 항목: invest_eval_amt] 투자 자산 평가액
    user_profile.invest_eval_amt = int(total_assets * investment_weight)
    
    # [표준 항목: monthly_paid_amt] 월 평균 저축액 (연봉의 10~40%)
    user_profile.monthly_paid_amt = int((user_profile.annual_income_amt * random.uniform(0.1, 0.4)) / 12)
    
    # [표준 항목: last_offered_rate] 현재 보유 상품 금리 (연 2.0% ~ 5.0% 사이)
    user_profile.last_offered_rate = round(random.uniform(2.0, 5.0), 2)
    
    # [표준 항목: withdrawable_amt] 출금 가능 금액 (잔액의 10~30%)
    user_profile.withdrawable_amt = int(user_profile.balance_amt * random.uniform(0.1, 0.3))

    # 3. 마이데이터 연동 상태 업데이트
    user_profile.is_mydata_linked = True
    user_profile.linked_org_count = random.randint(2, 8) # 2~8개 기관 연동 시뮬레이션
    
    user_profile.save()
    return user_profile