from rest_framework import serializers
from .models import DepositProducts, DepositOptions, Subscription

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
  
class SubscriptionSerializer(serializers.ModelSerializer):
  # deposit_option_info = DepositOptionsSerializer(source='deposit_option', read_only=True)

  product_name = serializers.ReadOnlyField(source='deposit_option.product.fin_prdt_nm')
  bank_name = serializers.ReadOnlyField(source='deposit_option.product.kor_co_nm')
  save_trm = serializers.ReadOnlyField(source='deposit_option.save_trm')
  intr_rate = serializers.ReadOnlyField(source='deposit_option.intr_rate')
  intr_rate2 = serializers.ReadOnlyField(source='deposit_option.intr_rate2')
  class Meta:
      model = Subscription
      fields = ['id', 'deposit_option', 'amount', 'subscribed_at', 'expired_at','product_name', 'bank_name', 'save_trm', 'intr_rate', 'intr_rate2', ]
      read_only_fields = ['user', 'subscribed_at', 'expired_at', ]

  def create(self, validated_data):
     return Subscription.objects.create(**validated_data)