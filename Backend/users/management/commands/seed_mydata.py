import numpy as np
import random
import pandas as pd
import joblib
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 앱 위치에 따른 정확한 참조
from users.models import FinancialProfile
from products.models import ProductOption, Subscription 

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

        product_options = list(ProductOption.objects.all())
        if not product_options:
            self.stdout.write(self.style.ERROR("상품 옵션이 없습니다. seed_products를 먼저 실행하세요."))
            return
        
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
                
            # 2. 가입 내역 생성 (핵심 수정 부분: Snapshot 필드 반영)
            if random.random() < sub_p:
                selected_option = random.choice(product_options)
                Subscription.objects.create(
                    user=user,
                    product_option=selected_option,
                    amount=random.randint(1000000, 10000000),
                    # 새로 추가한 Snapshot 필드들!
                    init_intr_rate=selected_option.intr_rate or 0,
                    init_intr_rate2=selected_option.intr_rate2 or 0,
                    init_save_trm=selected_option.save_trm,
                    init_intr_rate_type_nm=selected_option.intr_rate_type_nm,
                    is_active=True
                )

        # 2. 클러스터링 (비지도 학습)
        df = pd.DataFrame([{
            'id': p.id, 
            'inc': p.annual_income_amt, 
            'inv_ratio': p.invest_eval_amt / (p.balance_amt + p.invest_eval_amt + 1),
            'withdrawable_ratio': p.withdrawable_amt / (p.balance_amt + p.invest_eval_amt + 1),  # 현금 유동성: 총 자산 중 '지금 당장 예적금으로 묶어도 되는 비율'
            'growth': p.expense_growth_rate, 
            'expense_ratio': p.expense_to_income_ratio
        } for p in profiles])

        scaler = StandardScaler()
        scaled = scaler.fit_transform(df[['inc', 'inv_ratio', 'withdrawable_ratio', 'growth', 'expense_ratio']])
        
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(scaled)


        # 1. 클러스터별 평균 특징 계산
        summary = df.groupby('cluster').mean()

        # 2. 특징에 따른 페르소나 매핑 (가장 두드러진 특징 기준)
        # 소득이 가장 높은 그룹 -> 자산 관리 전문가
        expert_id = summary['inc'].idxmax()
        # 지출 비율이 가장 높은 그룹 -> YOLO족
        yolo_id = summary['expense_ratio'].idxmax()
        # 투자 비중이 가장 높은 그룹 -> 공격적 투자자
        aggressive_id = summary['inv_ratio'].idxmax()
        # 현금 유동성이 가장 높은 그룹 -> 홀더
        holder_id = summary['withdrawable_ratio'].idxmax()

        # 매핑 사전 구성 (나머지 하나는 자동으로 '성실한 저축왕' 할당)
        all_ids = set(df['cluster'].unique())
        assigned_ids = {expert_id, yolo_id, aggressive_id, holder_id}
        steady_id = list(all_ids - assigned_ids)[0] if (all_ids - assigned_ids) else None

        persona_map = {
            expert_id: "자산 관리 전문가",
            yolo_id: "YOLO족",
            aggressive_id: "공격적 투자자",
            holder_id: "현금 홀더",
            steady_id: "성실한 저축왕"
        }

        # 3. DB 업데이트 (라벨 번호와 명칭을 동시에 저장)
        for _, row in df.iterrows():
            p_name = persona_map.get(row['cluster'], "일반 사용자")
            FinancialProfile.objects.filter(id=row['id']).update(
                cluster_label=int(row['cluster']),
                cluster_name=p_name
            )

        # 모델 저장 경로 설정
        model_dir = os.path.join(settings.BASE_DIR, 'ml_models')
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        # 스케일러와 모델 저장
        joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
        joblib.dump(kmeans, os.path.join(model_dir, 'kmeans_model.pkl'))

        # [추가 제안] 나중에 설문조사에서 persona_map을 똑같이 쓰기 위해 이것도 저장해두면 좋습니다!
        joblib.dump(persona_map, os.path.join(model_dir, 'persona_map.pkl'))

        self.stdout.write(self.style.SUCCESS(f"✨ AI 페르소나 매칭 완료: {persona_map}"))
        self.stdout.write(self.style.SUCCESS("마이데이터 생성, 클러스터링 및 모델 저장 완료!"))
