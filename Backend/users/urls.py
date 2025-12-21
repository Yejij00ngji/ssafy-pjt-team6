from django.urls import path, include
from . import views

urlpatterns = [
  path('', include('dj_rest_auth.urls')),
  path('signup/', include('dj_rest_auth.registration.urls')),
  # path('subscriptions/', views.subscriptions),
  # path('subscriptions/<int:pk>/')
]