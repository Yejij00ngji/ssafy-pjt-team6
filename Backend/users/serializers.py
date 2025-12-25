from dj_rest_auth.registration.serializers import RegisterSerializer, SocialLoginSerializer
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialApp, SocialAccount
from rest_framework import serializers
from .models import User, FinancialProfile

class CustomRegisterSerializer(RegisterSerializer):
    birth_date = serializers.DateField(required=False, allow_null=True)
        # 필드명을 모델과 맞추어 is_mydata_linked로 변경 (혹은 기존 필드 유지 후 매핑)
    is_mydata_linked = serializers.BooleanField(default=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['birth_date'] = self.validated_data.get('birth_date')
        data['is_mydata_linked'] = self.validated_data.get('is_mydata_linked')
        return data
        
    def save(self, request):
        # 1. 기본 유저 정보 저장
        user = super().save(request)
        user.birth_date = self.validated_data.get('birth_date')
        
        if user.email:
            user.username = user.email
        user.save()

        # 2. FinancialProfile 생성 및 마이데이터 상태 저장
        # FinancialProfile 모델이 유저와 OneToOne 관계라고 가정합니다.
        # 프로필이 이미 생성되어 있을 수 있으므로 update_or_create를 사용하는 것이 안전합니다.
        agreed_status = self.validated_data.get('is_mydata_linked', False)
        
        FinancialProfile.objects.update_or_create(
            user=user,
            defaults={'is_mydata_linked': agreed_status}
        )

        return user
  
class UserDetailSerializer(serializers.ModelSerializer):
    is_mydata_linked = serializers.SerializerMethodField()

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
            'is_mydata_linked'
        )
        read_only_fields = ['username', 'email']

    # 해당 필드의 데이터를 가져오는 메서드
    def get_is_mydata_linked(self, obj):
        try:
            # User 모델과 FinancialProfile이 OneToOne 관계일 때 역참조
            # (관계를 정의할 때 related_name을 지정하지 않았다면 기본적으로 financialprofile 입니다)
            return obj.financialprofile.is_mydata_linked
        except FinancialProfile.DoesNotExist:
            # 프로필이 생성되지 않았을 경우 기본값 반환
            return False

class CustomTokenSerializer(serializers.Serializer):
    # 토큰 필드 (기본 LoginSerializer/RegistrationSerializer 응답에 포함됨)
    key = serializers.CharField()
    
    # 사용자 정보를 위한 필드
    user = UserDetailSerializer()

"""
소셜 로그인
"""
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