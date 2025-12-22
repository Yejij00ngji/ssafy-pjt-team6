from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.
class User(AbstractUser):
  email = models.EmailField(unique=True)
  nickname = models.CharField(max_length=20, blank=True)  # 닉네임 추가
  birth_date = models.DateField(null=True, blank=True)
  # salary = models.IntegerField(null=True)
  # possessions = models.IntegerField(null=True)
  is_mydata_agreed = models.BooleanField(default=False)

  REQUIRED_FIELDS = [] # email은 기본적으로 필수이므로 생략 가능
  USERNAME_FIELD = 'username' # 여전히 username을 쓰지만 이메일 값이 들어갈 것임

  def __str__(self):
    return self.email

# ----------------------------------------------------------------------
# 마이데이터 유저 정보
# ----------------------------------------------------------------------
class FinancialProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # -------------------------------------------------------------------------
    # 1. 마이데이터 공통 인증 및 연동 정보 (MyData Common)
    # -------------------------------------------------------------------------
    is_mydata_linked = models.BooleanField(default=False)
    # [표준 규격] 전송요구 여부 및 연동 기관 수
    linked_org_count = models.IntegerField(default=0) 

    # -------------------------------------------------------------------------
    # 2. 은행 업권 (Bank Sector) - 예적금 추천의 핵심 데이터
    # -------------------------------------------------------------------------
    # [표준 항목: balance_amt] 현재 잔액 (자산 규모 파악용)
    balance_amt = models.BigIntegerField(default=0, help_text="현재 잔액 합계")
    
    # [표준 항목: withdrawable_amt] 출금 가능 금액 (유동성 파악 - 파킹통장 추천 근거)
    withdrawable_amt = models.BigIntegerField(default=0, help_text="출금 가능 금액")
    
    # [표준 항목: last_offered_rate] 최종 적용 금리 (현재 보유 상품과 추천 상품 금리 비교용)
    last_offered_rate = models.FloatField(default=0.0, help_text="현재 보유 상품 중 최고 금리")
    
    # [표준 항목: monthly_paid_amt] 월 납입액 (사용자의 저축 여력/습관 파악용)
    monthly_paid_amt = models.IntegerField(default=0, help_text="월 평균 저축 금액")

    # -------------------------------------------------------------------------
    # 3. 투자 업권 (Invest Sector) - 투자 성향 분석용
    # -------------------------------------------------------------------------
    # [표준 항목: eval_amt] 계좌 평가 금액 (주식/코인 등 위험자산 비중 파악)
    invest_eval_amt = models.BigIntegerField(default=0, help_text="투자 자산 평가 금액")
    
    # [표준 항목: purchase_amt] 투자 원금 (수익률 계산 및 성향 파악)
    invest_purchase_amt = models.BigIntegerField(default=0, help_text="투자 원금 합계")

    # -------------------------------------------------------------------------
    # 4. 가공 데이터 및 설문 (서비스 로직용)
    # -------------------------------------------------------------------------
    # [가공 항목] annual_income_amt: 실제 명세서에는 없지만 추천을 위해 연봉 데이터로 가공
    annual_income_amt = models.BigIntegerField(default=0)
        
    # [AI 분석 항목] k-means로 분류된 페르소나 라벨
    cluster_label = models.IntegerField(null=True, blank=True)
    
    # [추가] 저축 목적 (추천 로직의 필터로 활용)
    PURPOSE_CHOICES = [
        ('MOKDON', '목돈 마련'),
        ('EMERGENCY', '비상금'),
        ('RETIRE', '노후 준비'),
    ]
    saving_purpose = models.CharField(
        max_length=20, 
        choices=PURPOSE_CHOICES, 
        default='MOKDON'
    )

    # -------------------------------------------------------------------------
    # 5. 소비 패턴 분석 (Consumption Analysis)
    # -------------------------------------------------------------------------
    # [가공 항목] 전월 대비 지출 변동률 (욜로족/과소비 패턴 분석 핵심 지표)
    # 1.0이면 동일, 1.2이면 20% 증가, 0.8이면 20% 감소
    expense_growth_rate = models.FloatField(default=1.0, help_text="전월 대비 지출 변동률")

    # [가공 항목] 소득 대비 지출 비율 (자산 형성 가능성 파악)
    # 0.9 이상이면 소득의 대부분을 소비하는 욜로 성향으로 판단
    expense_to_income_ratio = models.FloatField(default=0.0, help_text="소득 대비 지출 비율")


    # 변수처럼 사용할 수 있게 도와주는 데코레이터
    # 따로 migration할 필요 없음
    @property
    def age(self):  # 메서드 이름을 age로 설정
        if not self.user.birth_date:
            return 30
        today = date.today()
        birth = self.user.birth_date
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    
    def __str__(self):
        return f"{self.user.username}'s Financial Profile"