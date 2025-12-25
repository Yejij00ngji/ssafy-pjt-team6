import joblib
import os
import pandas as pd
import numpy as np
import pandas as pd
from django.conf import settings

<<<<<<< HEAD
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
=======
# 모델 파일 경로 설정
MODEL_DIR = os.path.join(settings.BASE_DIR, 'ml_models')
MODEL_PATH = os.path.join(MODEL_DIR, 'kmeans_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
MAP_PATH = os.path.join(MODEL_DIR, 'persona_map.pkl')
>>>>>>> feat/ai


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

"""
미동의자 클러스터 할당
"""
def assign_cluster_logic(profile):
    profile=validate_and_sanitize_profile(profile)   # 검사 실행
    try:
        # 1. 모델, 스케일러, 페르소나 맵 로드
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        # seed_mydata에서 저장한 맵을 불러옵니다.
        persona_map = joblib.load(MAP_PATH) 
        
        # 2. 피처 데이터 구성 (seed_mydata의 df 구성과 동일한 순서/키값 필수)
        total_assets = profile.balance_amt + profile.invest_eval_amt + 1
        input_data = pd.DataFrame([{
            'inc': profile.annual_income_amt, # seed_mydata에서 'inc'로 썼다면 여기서도 'inc'
            'inv_ratio': profile.invest_eval_amt / total_assets,
            'withdrawable_ratio': profile.withdrawable_amt / total_assets,
            'growth': profile.expense_growth_rate,
            'expense_ratio': profile.expense_to_income_ratio
        }])

        # 3. 스케일링 및 예측
        input_scaled = scaler.transform(input_data)
        cluster_id = int(model.predict(input_scaled)[0])
        
        # 4. 번호에 맞는 이름 찾기
        cluster_name = persona_map.get(cluster_id, "일반 사용자")
        
        return cluster_id, cluster_name

    except Exception as e:
        print(f"❌ 모델 예측 실패: {e}")
        return 0, "미분류" # 에러 시 기본값

# db에 저장
def update_profile_by_survey_safe(profile, data):
    # 이제 profile을 직접 받았으므로 user.financialprofile을 호출할 필요가 없습니다.
    profile.annual_income_amt = int(data.get('annual_income_amt', 0))
    profile.invest_eval_amt = int(data.get('invest_eval_amt', 0))
    profile.balance_amt = int(data.get('balance_amt', 0))
    profile.withdrawable_amt = int(data.get('withdrawable_amt', 0))
    profile.expense_growth_rate = float(data.get('expense_growth_rate', 1.0))
    profile.expense_to_income_ratio = float(data.get('expense_to_income_ratio', 0.0))
    
<<<<<<< HEAD
    # 클러스터 할당 (모델 로직이 불안하면 일단 주석 처리하고 테스트하세요)
    profile.cluster_label = assign_cluster_logic(profile)

    # profile.cluster_label = 1 # 임시 테스트용
=======
    # [수정] 클러스터 번호와 이름을 동시에 받아서 저장
    cluster_id, cluster_name = assign_cluster_logic(profile)
    profile.cluster_label = cluster_id
    profile.cluster_name = cluster_name
>>>>>>> feat/ai
    
    profile.save()
    return profile