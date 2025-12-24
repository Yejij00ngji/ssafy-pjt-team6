import joblib
import os
import numpy as np
from django.conf import settings

# 모델 파일 경로 설정 (예: base_dir/ml_models/...)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'kmeans_model.pkl')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'scaler.pkl')

def update_profile_by_survey_safe(profile, data):
    # 이제 profile을 직접 받았으므로 user.financialprofile을 호출할 필요가 없습니다.
    profile.annual_income_amt = int(data.get('annual_income_amt', 0))
    profile.invest_eval_amt = int(data.get('invest_eval_amt', 0))
    profile.balance_amt = int(data.get('balance_amt', 0))
    profile.withdrawable_amt = int(data.get('withdrawable_amt', 0))
    profile.expense_growth_rate = float(data.get('expense_growth_rate', 1.0))
    profile.expense_to_income_ratio = float(data.get('expense_to_income_ratio', 0.0))
    
    # 클러스터 할당 (모델 로직이 불안하면 일단 주석 처리하고 테스트하세요)
    # profile.cluster_label = assign_cluster_logic(profile) 
    profile.cluster_label = 1 # 임시 테스트용
    
    profile.save()
    return profile