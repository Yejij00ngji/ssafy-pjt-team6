# your_app/management/commands/seed_finance.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import FinancialProfile
from products.services import simulate_mydata_linking
import random
from datetime import timedelta, date

User = get_user_model()

class Command(BaseCommand):
    help = '비지도학습을 위한 가상 금융 데이터 100건을 생성합니다.'

    def handle(self, *args, **options):
        for i in range(100):
            # 1. 랜덤 생년월일 생성 (20세 ~ 65세)
            days_ago = random.randint(20*365, 65*365)
            random_birth_date = date.today() - timedelta(days=days_ago)

            # 2. 가상 유저 생성 (User 모델의 birth_date 필드에 직접 입력)
            username = f'user{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'password': 'password123',
                    'birth_date': random_birth_date  # 유저 모델의 필드 사용
                }
            )
            
            # 만약 이미 존재하는 유저라면 생년월일만 업데이트
            if not created:
                user.birth_date = random_birth_date
                user.save()

            # 3. 프로필 생성 및 설문 데이터 랜덤 초기화
            profile, _ = FinancialProfile.objects.get_or_create(
                user=user,
                defaults={
                    'risk_tolerance': random.randint(0, 2),
                    'saving_purpose': random.choice(['MOKDON', 'EMERGENCY', 'RETIRE']),
                }
            )

            # 4. 마이데이터 시뮬레이션 호출
            simulate_mydata_linking(profile)
            
        self.stdout.write(self.style.SUCCESS(f'성공적으로 {User.objects.count()}명의 유저와 금융 프로필을 매칭했습니다!'))