import joblib
import os
import pandas as pd
import numpy as np
from django.conf import settings

def assign_cluster_logic(profile):
    model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'financial_kmeans_1.pkl')
    scaler_path = os.path.join(settings.BASE_DIR, 'ml_models', 'financial_scaler_1.pkl')

    try:
        # 모델 및 스케일러 로드
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        # 1. 학습 시와 동일한 총 자산(Total Assets) 계산
        # 학습 코드에서 (p.balance_amt + p.invest_eval_amt + 1)를 분모로 사용함
        total_assets = profile.balance_amt + profile.invest_eval_amt + 1

        # 2. 피처 데이터 구성 (학습 때 사용한 순서와 이름을 정확히 일치시킴)
        # 학습 시 순서: ['inc', 'inv_ratio', 'withdrawable_ratio', 'growth', 'expense_ratio']
        input_data = pd.DataFrame([{
            'inc': profile.annual_income_amt,
            'inv_ratio': profile.invest_eval_amt / total_assets,
            'withdrawable_ratio': profile.withdrawable_amt / total_assets,
            'growth': profile.expense_growth_rate,
            'expense_ratio': profile.expense_to_income_ratio
        }])

        # 3. 스케일링 (학습 데이터의 평균/표준편차 적용)
        # DataFrame을 넣을 때 컬럼명이 학습 시와 다르면 경고가 뜰 수 있으므로 순서에 주의
        input_scaled = scaler.transform(input_data)
        
        # 4. 예측
        cluster = model.predict(input_scaled)
        
        return int(cluster[0])

    except Exception as e:
        print(f"모델 예측 실패: {e}")
        return 0

def update_profile_by_survey_safe(profile, data):
    # 이제 profile을 직접 받았으므로 user.financialprofile을 호출할 필요가 없습니다.
    profile.annual_income_amt = int(data.get('annual_income_amt', 0))
    profile.invest_eval_amt = int(data.get('invest_eval_amt', 0))
    profile.balance_amt = int(data.get('balance_amt', 0))
    profile.withdrawable_amt = int(data.get('withdrawable_amt', 0))
    profile.expense_growth_rate = float(data.get('expense_growth_rate', 1.0))
    profile.expense_to_income_ratio = float(data.get('expense_to_income_ratio', 0.0))
    
    # 클러스터 할당 (모델 로직이 불안하면 일단 주석 처리하고 테스트하세요)
    profile.cluster_label = assign_cluster_logic(profile)

    # profile.cluster_label = 1 # 임시 테스트용
    
    profile.save()
    return profile