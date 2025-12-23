from rest_framework import serializers
# from .models import FinancialProduct, ProductOption, Subscription
from .models import FinancialProduct, ProductOption, Subscription


# class ProductOptionSerializer(serializers.ModelSerializer):
#   # product_detail = FinancialProductSerializer(source='product', read_only=True)

#   # product_name = serializers.ReadOnlyField(source='product.fin_prdt_nm')
#   # bank_name = serializers.ReadOnlyField(source='product.kor_co_nm')

#   class Meta:
#     model = ProductOption
#     fields = [
#       'id',
#       'intr_rate_type_nm',
#       'save_trm',
#       'intr_rate',
#       'intr_rate2',
#     ]

# class FinancialProductSerializer(serializers.ModelSerializer):
#   # options = 'ProductOptionSerializer'(many=True, read_only=True)

#   save_trm = serializers.SerializerMethodField()

#   class Meta:
#     model = FinancialProduct
#     fields = [
#       'id',
#       'dcls_strt_day',
#       'kor_co_nm',
#       'fin_prdt_nm',
#       'save_trm',
#     ]

#   def get_save_trm(self, obj):
#     return list(obj.options.values_list('save_trm', flat=True))
  
# class FinancialProductDetailsSerializer(serializers.ModelSerializer):
#   # options = ProductOptionSerializer(many=True, read_only=True)

#   options = serializers.SerializerMethodField()

#   class Meta:
#     model = FinancialProduct
#     fields = [
#       'dcls_strt_day',
#       'kor_co_nm',
#       'fin_prdt_nm',
#       'join_deny',
#       'join_way',
#       'spcl_cnd',
#       'options',
#     ]

#   def get_options(self, obj):
#     serializer = ProductOptionSerializer(obj.options.all(), many=True)
#     return serializer.data

class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        # 상품 연결 정보(product)는 부모에서 들고 있으므로 제외하고 나머지만 포함
        fields = ('intr_rate_type_nm', 'save_trm', 'intr_rate', 'intr_rate2')

class FinancialProductSerializer(serializers.ModelSerializer):
    # 역참조(related_name='options')를 통해 상품에 속한 옵션 리스트를 가져옵니다.
    options = ProductOptionSerializer(many=True, read_only=True)
    
    # 가독성을 위해 choices의 Label 값(예: '정기예금')을 보여주는 필드 추가 (선택사항)
    product_type_display = serializers.CharField(source='get_product_type_display', read_only=True)

    class Meta:
        model = FinancialProduct
        fields = (
            'id', 'product_type', 'product_type_display', 'fin_prdt_cd', 
            'kor_co_nm', 'fin_prdt_nm', 'join_way', 'mtrt_int', 
            'spcl_cnd', 'join_deny', 'join_member', 'etc_note', 
            'rsrv_type_nm', 'options'
        )
        
# 상품 상세 정보
# 1. 옵션 시리얼라이저 (상세용: 모든 수치 포함)
class ProductOptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = '__all__'  # 상세 보기에서는 id를 포함한 모든 정보를 보여줍니다.

# 2. 상품 상세 시리얼라이저
class FinancialProductDetailSerializer(serializers.ModelSerializer):
    # 중첩된 옵션 정보
    options = ProductOptionDetailSerializer(many=True, read_only=True)
    
    # [추가 기능] 이 상품의 최고 금리만 따로 추출해서 상단에 보여주기 위함
    max_intr_rate = serializers.SerializerMethodField()
    
    # 가공된 텍스트 정보
    product_type_nm = serializers.CharField(source='get_product_type_display', read_only=True)

    class Meta:
        model = FinancialProduct
        fields = (
            'id', 'product_type', 'product_type_nm', 'fin_prdt_cd', 
            'kor_co_nm', 'fin_prdt_nm', 'join_way', 'mtrt_int', 
            'spcl_cnd', 'join_deny', 'join_member', 'etc_note', 
            'rsrv_type_nm', 'options', 'max_intr_rate'
        )

    # 최고 금리를 계산하는 로직
    def get_max_intr_rate(self, obj):
        options = obj.options.all()
        if options.exists():
            # 옵션들 중 intr_rate2(우대금리 포함)가 가장 높은 값을 반환
            return max([opt.intr_rate2 for opt in options if opt.intr_rate2 is not None], default=0)
        return 0
        
        
# 상품 추천 전용
class RecommendedProductSerializer(FinancialProductSerializer):
    # 추천 알고리즘에 의해 계산된 점수를 담을 필드
    recommend_score = serializers.FloatField(read_only=True, default=0.0)

    class Meta(FinancialProductSerializer.Meta):
        fields = FinancialProductSerializer.Meta.fields + ('recommend_score',)
        
# [심화] 유저 맞춤형 정보를 포함한 상세 시리얼라이저
class UserCustomProductDetailSerializer(FinancialProductDetailSerializer):
    is_recommended = serializers.SerializerMethodField()

    class Meta(FinancialProductDetailSerializer.Meta):
        fields = FinancialProductDetailSerializer.Meta.fields + ('is_liked', 'is_recommended')

    def get_is_recommended(self, obj):
        # 1. 현재 로그인한 유저의 클러스터(1~5그룹) 확인
        # 2. 해당 클러스터의 추천 상품 리스트에 이 상품(obj)이 포함되는지 확인
        # (이 로직은 추천 엔진 결과값과 연동됩니다)
        return True # 예시 데이터
      
# 가입한 상품보기  
class SubscriptionSerializer(serializers.ModelSerializer):
  # product_option_info = ProductOptionSerializer(source='product_option', read_only=True)

  product_name = serializers.ReadOnlyField(source='product_option.product.fin_prdt_nm')
  bank_name = serializers.ReadOnlyField(source='product_option.product.kor_co_nm')
  save_trm = serializers.ReadOnlyField(source='product_option.save_trm')
  intr_rate = serializers.ReadOnlyField(source='product_option.intr_rate')
  intr_rate2 = serializers.ReadOnlyField(source='product_option.intr_rate2')
  class Meta:
        model = Subscription
        fields = [
            'id', 'product_option', 'amount', 'subscribed_at', 'expired_at',
            'product_name', 'bank_name', 
            'init_intr_rate', 'init_intr_rate2', 'init_save_trm', 'init_intr_rate_type_nm',
            'save_trm', 'intr_rate', 'intr_rate2',
        ]
        read_only_fields = ['user', 'subscribed_at', 'expired_at', 'init_intr_rate', 'init_intr_rate2', 'init_save_trm', 'init_intr_rate_type_nm',
        ]

  def create(self, validated_data):
        return Subscription.objects.create(**validated_data)