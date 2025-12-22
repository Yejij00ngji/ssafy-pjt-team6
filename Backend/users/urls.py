from django.urls import path, include
from . import views

urlpatterns = [
  path('', include('dj_rest_auth.urls')),
  path('signup/', include('dj_rest_auth.registration.urls')),
  path('profile/', views.profile_update_view),
  path('google/login/', views.GoogleLogin.as_view()),
]