from dj_rest_auth.registration.serializers import RegisterSerializer, SocialLoginSerializer
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialApp, SocialAccount
from rest_framework import serializers
from .models import User, FinancialProfile
from products.models import DepositProducts
from products.serializers import DepositOptionsSerializer

class CustomRegisterSerializer(RegisterSerializer):
  birth_date = serializers.DateField()
  # salary = serializers.IntegerField()
  # possessions = serializers.IntegerField()
  is_mydata_agreed = serializers.BooleanField()

  def get_cleaned_data(self):
    data = super().get_cleaned_data()
    data['birth_date'] = self.validated_data.get('birth_date')
    # data['salary'] = self.validated_data.get('salary')
    # data['possessions'] = self.validated_data.get('possessions')
    data['is_mydata_agreed'] = self.validated_data.get('is_mydata_agreed')
    return data
    
  def save(self, request):
    user = super().save(request)
    user.birth_date = self.validated_data.get('birth_date')
    # user.salary = self.validated_data.get('salary')
    # user.possessions = self.validated_data.get('possessions')
    user.is_mydata_agreed = self.validated_data.get('is_mydata_agreed')

    if user.email:
        user.username = user.email

    user.save()
    return user
  
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',  # 로그인한 유저 정보 알기 위해 반드시 필요함
            'username',
            'nickname', 
            'email',
            'birth_date',
            # 'salary',
            # 'possessions', 
            'is_mydata_agreed'
        )
        read_only_fields = ['username', 'email']

class CustomTokenSerializer(serializers.Serializer):
    # 토큰 필드 (기본 LoginSerializer/RegistrationSerializer 응답에 포함됨)
    key = serializers.CharField()
    
    # 사용자 정보를 위한 필드
    user = UserDetailSerializer()

# accounts/serializers.py

class CustomGoogleSerializer(SocialLoginSerializer):
    # 명시적으로 아무것도 하지 않고 부모 클래스에 맡깁니다.
    def validate(self, attrs):
        # view에서 context를 넘겨받아 부모 validate가 작동하게 합니다.
        attrs = super().validate(attrs)
        return attrs
    
# 마이데이터 Serializer
class FinancialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProfile
        # 요청에서 받을 5가지 필드 정의
        fields = [
            'balance_amt',
            'invest_eval_amt',
            'annual_income_amt',
            'monthly_paid_amt',
            'withdrawable_amt'
        ]

    def create(self, validated_data):
        # view에서 넘겨준 user 객체를 꺼냅니다.
        user = validated_data.pop('user')
        
        # update_or_create를 사용하여 기존 데이터가 있으면 덮어쓰고, 없으면 생성합니다.
        profile, created = FinancialProfile.objects.update_or_create(
            user=user,
            defaults={
                **validated_data,
            }
        )
        return profile