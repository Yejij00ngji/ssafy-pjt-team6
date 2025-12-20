# community/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from community.models import Article
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Command(BaseCommand):
    help = '카테고리별 랜덤 게시글 데이터를 생성합니다.'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='생성할 게시글 개수')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        user = User.objects.first()
        
        if not user:
            self.stdout.write(self.style.ERROR('유저가 없습니다. 먼저 유저를 생성해주세요.'))
            return

        # 모델의 CATEGORY_CHOICES의 첫 번째 값들(Key)만 추출
        categories = ['notice', 'study', 'contest', 'qna', 'free']
        
        titles = [
            "함께 공모전 나가실 분!", "금융 데이터 분석 스터디 모집", "오늘 배운 내용 정리",
            "질문 있습니다.. 도와주세요!", "자유로운 게시판입니다.", "공지사항 확인 부탁드립니다",
            "이거 어떻게 해결하나요?", "재테크 초보 탈출기", "코인 시장 전망", "파이썬 장고 기초"
        ]

        for i in range(total):
            Article.objects.create(
                user=user,
                title=f"{random.choice(titles)} ({i+1})",
                content=f"이것은 {i+1}번째 생성된 테스트 본문입니다. " * 3,
                category=random.choice(categories), # 영어 코드명 사용
                views=random.randint(0, 500),
                # like_users=random.randint(0, 100)
            )

        self.stdout.write(self.style.SUCCESS(f'{total}개의 게시글이 생성되었습니다!'))