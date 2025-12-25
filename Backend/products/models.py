from django.db import models
from django.conf import settings
from datetime import date

# ----------------------------------------------------------------------
# 금융감독원 예/적금 상품 목록
# ----------------------------------------------------------------------

class FinancialProduct(models.Model):
    # 1. 상품 구분 (정기예금 vs 적금)
    PRODUCT_TYPE_CHOICES = [
        ('DEPOSIT', '정기예금'),
        ('SAVING', '적금'),
    ]
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)
    
    # 2. 공통 정보
    fin_prdt_cd = models.CharField(max_length=100, unique=True) # 상품 코드
    kor_co_nm = models.CharField(max_length=100)               # 금융회사명
    fin_prdt_nm = models.CharField(max_length=100)               # 상품명
    join_way = models.TextField(null=True)                      # 가입 방법
    mtrt_int = models.TextField(null=True)                      # 만기 후 이율
    spcl_cnd = models.TextField(null=True)                      # 우대 조건
    join_deny = models.IntegerField(null=True)                  # 가입 제한 (1:제한없음, 2:서민전용..)
    join_member = models.TextField(null=True)                   # 가입 대상
    etc_note = models.TextField(null=True)                      # 기타 유의사항
    
    # 3. 적금 전용 필드 (정기예금일 경우 null 허용)
    rsrv_type_nm = models.CharField(max_length=100, null=True)   # 적립 방식 (정액적립식, 자유적립식)

class ProductOption(models.Model):
    # 어떤 상품의 옵션인지 연결
    product = models.ForeignKey(FinancialProduct, on_delete=models.CASCADE, related_name='options')
    
    fin_prdt_cd = models.CharField(max_length=100)
    intr_rate_type_nm = models.CharField(max_length=100)        # 저축 금리 유형 (단리/복리)
    save_trm = models.IntegerField()                            # 저축 기간 (단위: 개월)
    intr_rate = models.FloatField(null=True)                    # 저축 금리
    intr_rate2 = models.FloatField(null=True)                   # 최고 우대 금리
    # embedding = models.JSONField(null=True, blank=True)         # 임베딩 벡터를 저장할 필드 추가 (빠른 ai 기능을 위해 필요)


# 상품 가입 목록 테이블
class Subscription(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='subscriptions'
  )

  product_option = models.ForeignKey(
    ProductOption,
    on_delete=models.SET_NULL,  # 상품 정보가 삭제되어도 가입 이력은 남김
    null=True,
    related_name='subscribers'
  )
  
  # --- 가입 시점의 데이터 박제 (Snapshot Fields) ---
  # 상품 테이블의 데이터가 변해도 이 값들은 유지됩니다.
  init_intr_rate = models.FloatField(help_text="가입 당시 기본 금리")
  init_intr_rate2 = models.FloatField(help_text="가입 당시 우대 금리")
  init_save_trm = models.IntegerField(help_text="가입 당시 저축 기간(월)")
  init_intr_rate_type_nm = models.CharField(max_length=100, help_text="가입 당시 금리 유형(단리/복리)")

  amount = models.BigIntegerField(default=0)

  subscribed_at = models.DateField(auto_now_add=True)
  expired_at = models.DateField(null=True, blank=True)

  is_active = models.BooleanField(default=True)  # 만기가 지났거나 해지했을 경우 필터링

  class Meta:
    unique_together = ('user', 'product_option')
    
  def __str__(self):
        return f"{self.user.username} - {self.product_option.product.fin_prdt_nm if self.product_option else '삭제된 상품'}"
  

class RecommendationHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommendation_histories"
    )
    product_option = models.ForeignKey(
        ProductOption,
        on_delete=models.CASCADE,
        related_name="recommended_histories"
    )

    score = models.FloatField()
    confidence = models.FloatField()
    cluster_label = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "product_option", "created_at")

    def __str__(self):
        return f"{self.user.username} - {self.product_option.id}"
