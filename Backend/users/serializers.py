from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User, Subscription
from products.models import DepositProducts
from products.serializers import DepositOptionsSerializer

class CustomRegisterSerializer(RegisterSerializer):
  birth_date = serializers.DateField()
  salary = serializers.IntegerField()
  possessions = serializers.IntegerField()
  is_mydata_agreed = serializers.BooleanField()

  def get_cleaned_data(self):
    data = super().get_cleaned_data()
    data['birth_date'] = self.validated_data.get('birth_date')
    data['salary'] = self.validated_data.get('salary')
    data['possessions'] = self.validated_data.get('possessions')
    data['is_mydata_agreed'] = self.validated_data.get('is_mydata_agreed')
    return data
    
  def save(self, request):
    user = super().save(request)
    user.birth_date = self.validated_data.get('birth_date')
    user.salary = self.validated_data.get('salary')
    user.possessions = self.validated_data.get('possessions')
    user.is_mydata_agreed = self.validated_data.get('is_mydata_agreed')
    user.save()
    return user
  
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 
            'birth_date', 
            'salary', 
            'possessions', 
            'is_mydata_agreed'
        )
        read_only_fields = fields

class CustomTokenSerializer(serializers.Serializer):
    # 토큰 필드 (기본 LoginSerializer/RegistrationSerializer 응답에 포함됨)
    key = serializers.CharField()
    
    # 사용자 정보를 위한 필드
    user = UserDetailSerializer()

class SubscriptionSerializer(serializers.ModelSerializer):
  # deposit_option_info = DepositOptionsSerializer(source='deposit_option', read_only=True)

  product_name = serializers.ReadOnlyField(source='deposit_option.product.fin_prdt_nm')
  bank_name = serializers.ReadOnlyField(source='deposit_option.product.kor_co_nm')
  save_trm = serializers.ReadOnlyField(source='deposit_option.save_trm')
  intr_rate = serializers.ReadOnlyField(source='deposit_option.intr_rate')
  intr_rate2 = serializers.ReadOnlyField(source='deposit_option.intr_rate2')
  class Meta:
      model = Subscription
      fields = ['id', 'deposit_option', 'amounts', 'subscribed_at', 'expired_at','product_name', 'bank_name', 'save_trm', 'intr_rate', 'intr_rate2', ]
      read_only_fields = ['user', 'subscribed_at', 'expired_at', ]

  def create(self, validated_data):
     return Subscription.objects.create(**validated_data)
  
