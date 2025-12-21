import numpy as np
import random
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 앱 위치에 따른 정확한 참조
from users.models import FinancialProfile
from products.models import DepositOptions, Subscription 

User = get_user_model()

class Command(BaseCommand):
    help = "가상 마이데이터 생성 및 클러스터링 라벨링 통합 스크립트"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("데이터 생성을 시작합니다..."))
        
        # 1. 초기화 (유저 프로필과 구독 정보만)
        Subscription.objects.all().delete()
        FinancialProfile.objects.all().delete()

        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR("유저가 없습니다. users.json을 먼저 실행하세요."))
            return

        deposit_options = list(DepositOptions.objects.all())
        
        profiles = []
        for user in users:
            # 페르소나 결정
            persona = random.choices(
                ['yolo', 'holder', 'aggressive', 'steady', 'silver'],
                weights=[25, 15, 20, 30, 10]
            )[0]

            # 페르소나별 기본 수치 세팅 (지출 변동률/비율 추가)
            if persona == 'yolo':
                income, inv_r, sub_p = 32000000, 0.05, 0.15
                growth, exp_inc_r = random.uniform(1.2, 1.5), random.uniform(0.8, 0.95)
            elif persona == 'holder':
                income, inv_r, sub_p = 48000000, 0.10, 0.35
                growth, exp_inc_r = random.uniform(0.9, 1.1), random.uniform(0.4, 0.6)
            elif persona == 'aggressive':
                income, inv_r, sub_p = 60000000, 0.75, 0.60
                growth, exp_inc_r = random.uniform(1.0, 1.2), random.uniform(0.3, 0.5)
            elif persona == 'steady':
                income, inv_r, sub_p = 50000000, 0.30, 0.95
                growth, exp_inc_r = random.uniform(0.95, 1.05), random.uniform(0.2, 0.4)
            else: # silver
                income, inv_r, sub_p = 90000000, 0.15, 0.90
                growth, exp_inc_r = random.uniform(0.8, 1.0), random.uniform(0.1, 0.3)

            # 데이터 생성
            total_assets = int(income * random.uniform(0.8, 5.0))
            invest_eval = int(total_assets * inv_r)
            balance = total_assets - invest_eval
            
            profile = FinancialProfile.objects.create(
                user=user,
                annual_income_amt=income,
                balance_amt=balance,
                invest_eval_amt=invest_eval,
                expense_growth_rate=growth,
                expense_to_income_ratio=exp_inc_r,
                monthly_paid_amt=int((income/12) * (1-exp_inc_r)),
                withdrawable_amt=int(balance * (0.9 if persona == 'holder' else 0.2)),
                is_mydata_linked=True
            )
            profiles.append(profile)

            # 가입 내역 생성
            if random.random() < sub_p and deposit_options:
                Subscription.objects.create(
                    user=user,
                    deposit_option=random.choice(deposit_options),
                    amount=random.randint(1000000, 10000000)
                )

        # 2. 클러스터링 (비지도 학습)
        df = pd.DataFrame([{
            'id': p.id, 'inc': p.annual_income_amt, 
            'inv': p.invest_eval_amt / (p.balance_amt + p.invest_eval_amt + 1),
            'growth': p.expense_growth_rate, 'ratio': p.expense_to_income_ratio
        } for p in profiles])

        scaler = StandardScaler()
        scaled = scaler.fit_transform(df[['inc', 'inv', 'growth', 'ratio']])
        
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(scaled)

        for _, row in df.iterrows():
            FinancialProfile.objects.filter(id=row['id']).update(cluster_label=str(int(row['cluster'])))

        self.stdout.write(self.style.SUCCESS("마이데이터 생성 및 AI 클러스터링 완료!"))