from rest_framework import serializers
from .models import DepositProducts, DepositOptions

class DepositOptionsSerializer(serializers.ModelSerializer):
  # product_detail = DepositProductsSerializer(source='product', read_only=True)

  # product_name = serializers.ReadOnlyField(source='product.fin_prdt_nm')
  # bank_name = serializers.ReadOnlyField(source='product.kor_co_nm')

  class Meta:
    model = DepositOptions
    fields = [
      'id',
      'intr_rate_type_nm',
      'save_trm',
      'intr_rate',
      'intr_rate2',
    ]

class DepositProductsSerializer(serializers.ModelSerializer):
  # options = 'DepositOptionsSerializer'(many=True, read_only=True)

  save_trm = serializers.SerializerMethodField()

  class Meta:
    model = DepositProducts
    fields = [
      'id',
      'dcls_strt_day',
      'kor_co_nm',
      'fin_prdt_nm',
      'save_trm',
    ]

  def get_save_trm(self, obj):
    return list(obj.options.values_list('save_trm', flat=True))
  
class DepositProductsDetailsSerializer(serializers.ModelSerializer):
  # options = DepositOptionsSerializer(many=True, read_only=True)

  options = serializers.SerializerMethodField()

  class Meta:
    model = DepositProducts
    fields = [
      'dcls_strt_day',
      'kor_co_nm',
      'fin_prdt_nm',
      'join_deny',
      'join_way',
      'spcl_cnd',
      'options',
    ]

  def get_options(self, obj):
    serializer = DepositOptionsSerializer(obj.options.all(), many=True)
    return serializer.data