from django.urls import path, include
from . import views

urlpatterns = [
  path('', include('dj_rest_auth.urls')),
  path('signup/', include('dj_rest_auth.registration.urls')),
  path('profile/', views.profile_update_view),
  path('financial-profile/', views.getClusterInfo),
  # path('finacial-profile/', views.financial_profile),
  # 'login/'을 빼고 명확하게 API임을 나타내는 주소로 바꿉니다.
  # 현재 urls.py의 경로가 google/login/으로 설정되어 있는데, 이는 django-allauth가 기본적으로 사용하는 내부 경로와 이름이 겹치거나 충돌을 일으킬 가능성이 매우 높습니다.
  path('naver/', views.NaverLogin.as_view(), name='naver_login'),
  path('kakao/', views.KakaoLogin.as_view(), name='kakao_login'), 
  path('google/token/', views.GoogleLogin.as_view(), name='google_api_login'),
  # path('user/status/', views.get_user_status, name='user_status'), # 이 경로도 없어서 404가 나는 중입니다.
]