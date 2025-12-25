from dj_rest_auth.registration.serializers import RegisterSerializer, SocialLoginSerializer
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialApp, SocialAccount
from rest_framework import serializers
from .models import User, FinancialProfile

class CustomRegisterSerializer(RegisterSerializer):
    birth_date = serializers.DateField(required=False, allow_null=True)
    # 필드명을 모델과 맞추어 is_mydata_linked로 변경 (혹은 기존 필드 유지 후 매핑)
    is_mydata_linked = serializers.BooleanField(default=False, required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()  # 부모 데이터 먼저
        # 데이터가 없을 경우 none이나 기본값 할당
        data['birth_date'] = self.validated_data.get('birth_date')
        data['is_mydata_linked'] = self.validated_data.get('is_mydata_linked')
        return data
        
    def save(self, request):
        # 1. 기본 유저 정보 저장
        user = super().save(request)
        # 소셜 가입 시 birth_date가 없을 수 있으므로 안전하게 처리
        birth_date = self.validated_data.get('birth_date')
        if birth_date:
            user.birth_date = birth_date
        
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
        # DB에 있는 필드들을 그대로 매핑합니다.
        fields = [
            'annual_income_amt',
            'invest_eval_amt',
            'balance_amt',
            'withdrawable_amt',
            'expense_growth_rate',
            'expense_to_income_ratio',
            'cluster_label',
            'cluster_name',
        ]
        # 클러스터 정보는 수동 입력 방지를 위해 읽기 전용으로 설정 가능합니다.
        read_only_fields = ['cluster_label', 'cluster_name']

    def create(self, validated_data):
        # context에서 user를 가져오거나, 전달받은 데이터에서 추출
        user = self.context.get('request').user
        
        # update_or_create로 기존 프로필이 있으면 업데이트, 없으면 신규 생성
        profile, created = FinancialProfile.objects.update_or_create(
            user=user,
            defaults=validated_data
        )
        return profile