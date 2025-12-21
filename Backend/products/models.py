from django.db import models
from django.conf import settings
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
    

# 상품 가입 목록 테이블
class Subscription(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='subscriptions'
  )

  deposit_option = models.ForeignKey(
    DepositOptions,
    on_delete=models.CASCADE,
    related_name='subscribers'
  )

  amount = models.BigIntegerField(default=0)

  subscribed_at = models.DateField(auto_now_add=True)
  expired_at = models.DateField(null=True, blank=True)

  is_active = models.BooleanField(default=True)  # 만기가 지났거나 해지했을 경우 필터링

  class Meta:
    unique_together = ('user', 'deposit_option')