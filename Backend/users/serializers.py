from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User
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
    user.save()
    return user
  
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'nickname', 
            'email',
            'birth_date',
            # 'salary',
            # 'possessions', 
            'is_mydata_agreed'
        )
        read_only_fields = ['username', 'birth_data',]

class CustomTokenSerializer(serializers.Serializer):
    # 토큰 필드 (기본 LoginSerializer/RegistrationSerializer 응답에 포함됨)
    key = serializers.CharField()
    
    # 사용자 정보를 위한 필드
    user = UserDetailSerializer()
