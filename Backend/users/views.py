from django.shortcuts import render
from django.shortcuts import get_object_or_404
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserDetailSerializer, CustomGoogleSerializer

# Create your views here.

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated]) # 로그인한 사용자만 접근 가능
def profile_update_view(request):
    user = request.user
    
    # 1. 프로필 정보 조회 (GET)
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    # 2. 프로필 정보 수정 (PUT/PATCH)
    elif request.method in ['PUT', 'PATCH']:
        # partial=True를 설정하면 nickname이나 email 중 하나만 보내도 수정 가능합니다.
        serializer = UserDetailSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
# 1. 에러 우회용 클라이언트 클래스 정의
class ReliableOAuth2Client(OAuth2Client):
    def __init__(self, *args, **kwargs):
        if 'scope_delimiter' in kwargs:
            kwargs.pop('scope_delimiter')
        super().__init__(*args, **kwargs)
        
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:5173/login/callback" # Vue의 리디렉션 URI와 동일해야 함
    client_class = ReliableOAuth2Client
    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()
    
class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    callback_url = "http://localhost:5173/login/kakao/callback" # 프론트엔드 리다이렉트 경로
    client_class = ReliableOAuth2Client
    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()
    
class NaverLogin(SocialLoginView):
    adapter_class = NaverOAuth2Adapter
    callback_url = "http://localhost:5173/login/naver/callback" # 프론트엔드 URL
    client_class = ReliableOAuth2Client
    
    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()