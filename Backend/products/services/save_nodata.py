import joblib
import os
import numpy as np
import pandas as pd
from django.conf import settings

# 1. 모델 파일 경로 설정 (예: base_dir/ml_models/...)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'kmeans_model.pkl')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'scaler.pkl')


def validate_and_sanitize_profile(profile):
    """데이터 유효성 검사 및 기본값 보정"""
    # 1. 소득이 0이거나 음수인 경우 (최소 생계비 수준으로 보정하거나 에러 처리)
    if profile.annual_income_amt <= 0:
        profile.annual_income_amt = 12000000  # 연 1200만원 기본값 예시
    
    # 2. 총 자산이 0인 경우 (분모 0 방지)
    total_assets = profile.balance_amt + profile.invest_eval_amt
    if total_assets <= 0:
        # 자산이 없다고 응답한 경우, 최소한의 계산을 위해 1원 설정
        total_assets = 1
        
    # 3. 비율이 1(100%)을 초과하는 경우 보정
    # 지출이 소득의 2배를 넘을 순 있지만, 스케일링을 위해 2.0으로 캡핑(Capping)
    if profile.expense_to_income_ratio > 2.0:
        profile.expense_to_income_ratio = 2.0
        
    return profile

# 미동의자 클러스터 할당
def assign_cluster_logic(profile):
    profile=validate_and_sanitize_profile(profile)   # 검사 실행
    try:
        model = joblib.load(MODEL_PATH)
        
        # 2. 피처 데이터 구성 (학습 때와 동일한 순서여야 함!)
        # annual_income_amt, inv_ratio, withdrawable_ratio, growth, expense_ratio 순서 가정
        # 만약 모델이 비율(ratio)을 원한다면 계산해서 넣어줘야 합니다.
        
        # 수정 후 (학습 로직과 동일하게)
        total_assets = profile.balance_amt + profile.invest_eval_amt + 1
        input_data = pd.DataFrame([{
            'annual_income_amt': profile.annual_income_amt,
            'inv_ratio': profile.invest_eval_amt / total_assets,
            'withdrawable_ratio': profile.withdrawable_amt / total_assets,
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