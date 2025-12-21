from django.db import models
from datetime import date

# ----------------------------------------------------------------------
# 금융감독원 예/적금 상품 목록
# ----------------------------------------------------------------------
class DepositProducts(models.Model):
    # 필수 식별자 필드 (baseList 매핑)
    # FinCo API의 상품 고유 코드는 데이터베이스의 PK/Unique Key가 되어야 합니다.
    fin_co_no = models.CharField(max_length=50)       # 금융회사 코드
    fin_prdt_cd = models.CharField(max_length=50, unique=True) # 금융상품 코드 (API PK)
    
    # 상품 정보 필드 (baseList 매핑)
    kor_co_nm = models.CharField(max_length=100)       # 금융회사명
    fin_prdt_nm = models.CharField(max_length=100)     # 금융상품명
    join_member = models.TextField()                   # 가입 대상
    join_way = models.TextField()                      # 가입 방법
    
    # 상세 정보 (baseList 매핑)
    # 우대 조건은 추천 로직(FR04)에서 핵심적인 필드가 되므로 반드시 저장합니다.
    spcl_cnd = models.TextField(null=True, blank=True) # 우대 조건 (nullable 허용)
    mtrt_int = models.TextField(null=True, blank=True) # 만기 후 이자율 (텍스트가 복잡하여 TextField)
    etc_note = models.TextField(null=True, blank=True) # 기타 유의사항

    # 부가 정보 (baseList 매핑)
    max_limit = models.BigIntegerField(null=True, blank=True) # 최고 한도 (숫자가 커질 수 있으므로 BigIntegerField 권장)
    join_deny = models.IntegerField()                  # 가입 제한 (1:제한없음, 2:일부제한, 3:제한)
    
    # 분류 및 메타 데이터
    product_type = models.CharField(max_length=10, default='DEPOSIT') # 상품 분류 ('DEPOSIT' 또는 'SAVING')
    dcls_strt_day = models.CharField(max_length=8)     # 공시 시작일 (YYYYMMDD)
    
    # 데이터 업데이트 추적용 필드 (Django 기본 기능 활용)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.kor_co_nm}] {self.fin_prdt_nm}'
    

class DepositOptions(models.Model):
    # 관계 설정: FinanceProduct 모델의 fin_prdt_cd와 연결됩니다.
    # related_name='options'를 설정하면 FinanceProduct.objects.get(..).options.all()로 접근 가능합니다.
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='options')

    # 금리/기간 필드 (optionList 매핑)
    intr_rate_type = models.CharField(max_length=10)   # 저축 금리 유형 코드 (S:단리, M:복리 등)
    intr_rate_type_nm = models.CharField(max_length=10) # 저축 금리 유형명 (단리/복리)
    save_trm = models.IntegerField()                   # 저축 기간 (단위: 개월, 6, 12, 24, 36 등)
    intr_rate = models.FloatField(null=True, blank=True) # 저축 기본 금리
    intr_rate2 = models.FloatField(null=True, blank=True) # 최고 우대 금리 (추천의 핵심)

    # 복합 유니크 제약 조건 (중요)
    # 한 상품(product)에 대해 같은 기간(save_trm)과 같은 금리 유형이 중복될 수 없습니다.
    class Meta:
        unique_together = ('product', 'save_trm', 'intr_rate_type_nm')

    def __str__(self):
        return f'{self.product.fin_prdt_nm} - {self.save_trm}개월 ({self.intr_rate2}%)'
    

# ----------------------------------------------------------------------
# 마이데이터 유저 정보
# ----------------------------------------------------------------------
from django.conf import settings

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
    
    # [설문 항목] risk_tolerance: 표준 명세에는 없으나 금감원 투자성향 가이드를 따름
    risk_tolerance = models.IntegerField(choices=[(0, '안정'), (1, '중립'), (2, '공격')], default=0)
    
    # [AI 분석 항목] k-means로 분류된 페르소나 라벨
    cluster_label = models.CharField(max_length=50, null=True, blank=True)
    
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