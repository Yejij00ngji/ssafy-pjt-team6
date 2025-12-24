import numpy as np
import random
import os

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib
import os
from django.conf import settings
from django.shortcuts import get_object_or_404

from users.models import FinancialProfile

# ====================================================
# 마이데이터를 가상으로 생성 & 데이터 정규분포화
# ====================================================
def simulate_mydata_linking(user_profile):
    age = user_profile.age  # 미리 저장된 나이 사용
    
    # 페르소나 확률 결정 (테스트를 위해 랜덤하게 부여 후 그에 맞는 수치 생성)
    persona = random.choice(['yolo', 'holder', 'aggressive', 'steady', 'silver'])
    
    if persona == 'yolo': # 욜로족: 소득 대비 지출 높음, 저축 낮음
        income = np.random.normal(35000000, 5000000)
        expense_ratio = random.uniform(0.8, 0.95) # 소득의 80~95% 소비
        invest_ratio = random.uniform(0.01, 0.1)
        
    elif persona == 'holder': # 현금 홀더: 잔액은 많으나 예적금 안 함
        income = np.random.normal(50000000, 10000000)
        expense_ratio = random.uniform(0.4, 0.6)
        invest_ratio = random.uniform(0.05, 0.15)
        # 특징: withdrawable_amt(출금가능액)를 balance의 80% 이상으로 설정
        
    elif persona == 'aggressive': # 공격적 투자자: 투자 비중 압도적
        income = np.random.normal(60000000, 15000000)
        expense_ratio = random.uniform(0.3, 0.5)
        invest_ratio = random.uniform(0.6, 0.8) # 자산의 60~80%가 투자
        
    elif persona == 'steady': # 자산 형성 모범생: 소득 대비 저축률 높음
        income = np.random.normal(45000000, 8000000)
        expense_ratio = random.uniform(0.2, 0.4)
        invest_ratio = random.uniform(0.2, 0.4)
        
    else: # 은퇴/안정형: 고소득, 고자산, 투자 낮음
        income = np.random.normal(90000000, 20000000)
        expense_ratio = random.uniform(0.2, 0.3)
        invest_ratio = random.uniform(0.1, 0.2)

    # DB 필드에 매칭
    user_profile.annual_income_amt = int(income)
    total_assets = int(income * random.uniform(0.5, 5.0)) # 경력에 따른 자산 배수
    user_profile.invest_eval_amt = int(total_assets * invest_ratio)
    user_profile.balance_amt = total_assets - user_profile.invest_eval_amt
    
    # 지출액 기반 월 저축액 계산
    monthly_income = income / 12
    user_profile.monthly_paid_amt = int(monthly_income * (1 - expense_ratio))
    
    # 현금 홀더 특화 로직
    if persona == 'holder':
        user_profile.withdrawable_amt = int(user_profile.balance_amt * 0.9)
    else:
        user_profile.withdrawable_amt = int(user_profile.balance_amt * 0.2)

    user_profile.is_mydata_linked = True
    user_profile.save()

# ====================================================
# 5개의 그룹으로 클러스터링 (기준만 있고 정답 레이블은 없음)
# ====================================================
def run_financial_clustering():
    profiles = FinancialProfile.objects.filter(is_mydata_linked=True)
    data = []

    for p in profiles:
        total_asset = p.balance_amt + p.invest_eval_amt + 1
        data.append({
            'id': p.id,
            'income': p.annual_income_amt,
            'age': p.age,
            'invest_ratio': p.invest_eval_amt / total_asset, # 투자 비중
            'save_ratio': (p.monthly_paid_amt * 12) / (p.annual_income_amt + 1), # 저축률
            'liquidity_ratio': p.withdrawable_amt / (p.balance_amt + 1) # 유동성 비중
        })

    df = pd.DataFrame(data)
    features = ['income', 'age', 'invest_ratio', 'save_ratio', 'liquidity_ratio']
    
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[features])

    # K=5 설정
    kmeans = KMeans(n_clusters=5, init='k-means++', n_init=20, random_state=42)
    df['cluster'] = kmeans.fit_predict(scaled_data)

    # [중요] 전략 B를 위해 Scaler와 KMeans 모델 저장
    scaler_path = os.path.join(settings.ML_MODELS_DIR, 'financial_scaler.pkl')
    kmeans_path = os.path.join(settings.ML_MODELS_DIR, 'financial_kmeans.pkl')
        
    joblib.dump(scaler, scaler_path)
    joblib.dump(kmeans, kmeans_path)

    # 결과 DB 반영
    for _, row in df.iterrows():
        profile = FinancialProfile.objects.get(id=row['id'])
        profile.cluster_label = str(int(row['cluster']))
        profile.save()

def predict_user_cluster(profile):
    """신규 유저 1명의 데이터를 받아 클러스터 라벨을 반환"""
    try:
        # 1. 저장된 모델 로드
        scaler_path = os.path.join(settings.ML_MODELS_DIR, 'financial_scaler.pkl')
        kmeans_path = os.path.join(settings.ML_MODELS_DIR, 'financial_kmeans.pkl')

        scaler = joblib.load(scaler_path)
        kmeans = joblib.load(kmeans_path)

        # 2. 유저 데이터를 모델 입력 형태(2D array)로 변환
        total_asset = profile.balance_amt + profile.invest_eval_amt + 1
        user_features = [[
            profile.annual_income_amt,
            profile.age,
            profile.invest_eval_amt / total_asset,
            (profile.monthly_paid_amt * 12) / (profile.annual_income_amt + 1),
            # profile.expense_growth_rate,
            # profile.expense_to_income_ratio
            float(profile.withdrawable_amt / (profile.balance_amt + 1)) # liquidity_ratio (이게 빠져있었음)
        ]]

        # 3. 스케일링 및 예측
        scaled_features = scaler.transform(user_features) # fit_transform이 아닌 transform만!
        cluster_id = kmeans.predict(scaled_features)[0]

        # 4. 결과 저장
        profile.cluster_label = str(int(cluster_id))
        profile.save()
        return profile.cluster_label
    
    except FileNotFoundError:
        # 모델 파일이 없으면 전체 클러스터링 한 번 실행
        run_financial_clustering()
        return predict_user_cluster(profile)
    
# 미동의자 클러스터 분류
def assign_cluster_logic(profile):
    # 1. 모델 파일 경로 설정 (경로는 프로젝트 구조에 맞게 수정)
    model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'kmeans_model.pkl')
    scaler_path = os.path.join(settings.BASE_DIR, 'ml_models', 'scaler.pkl') # 스케일러도 있다면 로드

    try:
        model = joblib.load(model_path)
        
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
        scaler = joblib.load(scaler_path)
        input_scaled = scaler.transform(input_data)
        cluster = model.predict(input_scaled)[0]
        
        # cluster = model.predict(input_data)[0] # 스케일러 없을 경우
        return int(cluster)

    except Exception as e:
        print(f"모델 예측 실패: {e}")
        return 0 # 실패 시 기본값

# 미동의자 설문조사 > db 저장 함수  
# views.py 또는 services.py
# def update_profile_by_survey(user, survey_data):
#     profile, _ = FinancialProfile.objects.get_or_create(user=user)

#     try:
#         # 데이터가 프론트에서 넘어올 때 숫자인지 확인
#         profile.annual_income_amt = int(survey_data.get('annual_income_amt', 0))
#         profile.invest_eval_amt = int(survey_data.get('invest_eval_amt', 0))
#         profile.balance_amt = int(survey_data.get('balance_amt', 0))
#         profile.withdrawable_amt = int(survey_data.get('withdrawable_amt', 0))
        
#         # 소수점 데이터(Float) 처리
#         profile.expense_growth_rate = float(survey_data.get('expense_growth_rate', 1.0))
#         profile.expense_to_income_ratio = float(survey_data.get('expense_to_income_ratio', 0.0))
        
#         # KMeans 모델 pkl 호출 로직 (앞서 설명한 코드)
#         profile.cluster_label = assign_cluster_logic(profile) 
        
#         profile.save()
#         return profile
#     except (TypeError, ValueError) as e:
#         # 데이터 타입이 안 맞을 경우 에러 발생
#         raise Exception(f"데이터 형식 오류: {str(e)}")

# views.py 또는 services.py
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