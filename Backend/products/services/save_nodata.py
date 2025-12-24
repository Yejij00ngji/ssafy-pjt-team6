import joblib
import os
import numpy as np
from django.conf import settings

# 1. 모델 파일 경로 설정 (예: base_dir/ml_models/...)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'kmeans_model.pkl')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'scaler.pkl')

# 미동의자 클러스터 할당
def assign_cluster_logic(profile):
    try:
        model = joblib.load(MODEL_PATH)
        
        # 2. 피처 데이터 구성 (학습 때와 동일한 순서여야 함!)
        # annual_income_amt, inv_ratio, withdrawable_ratio, growth, expense_ratio 순서 가정
        # 만약 모델이 비율(ratio)을 원한다면 계산해서 넣어줘야 합니다.
        
        input_data = pd.DataFrame([{
            'annual_income_amt': profile.annual_income_amt,
            'inv_ratio': profile.invest_eval_amt / (profile.annual_income_amt * 2) if profile.annual_income_amt > 0 else 0,
            'withdrawable_ratio': profile.withdrawable_amt / profile.balance_amt if profile.balance_amt > 0 else 0,
            'expense_growth_rate': profile.expense_growth_rate,
            'expense_to_income_ratio': profile.expense_to_income_ratio
        }])

        # 3. 스케일링 및 예측
        scaler = joblib.load(SCALER_PATH)
        input_scaled = scaler.transform(input_data)
        cluster = model.predict(input_scaled)[0]
        
        # cluster = model.predict(input_data)[0] # 스케일러 없을 경우
        return int(cluster)

    except Exception as e:
        print(f"모델 예측 실패: {e}")
        return 0 # 실패 시 기본값

# db에 저장
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