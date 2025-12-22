from django.urls import path, include
from . import views

urlpatterns = [
  path('', include('dj_rest_auth.urls')),
  path('signup/', include('dj_rest_auth.registration.urls')),
  path('profile/', views.profile_update_view),
  # 'login/'을 빼고 명확하게 API임을 나타내는 주소로 바꿉니다.
  # 현재 urls.py의 경로가 google/login/으로 설정되어 있는데, 이는 django-allauth가 기본적으로 사용하는 내부 경로와 이름이 겹치거나 충돌을 일으킬 가능성이 매우 높습니다.
  path('google/token/', views.GoogleLogin.as_view(), name='google_api_login'),
]