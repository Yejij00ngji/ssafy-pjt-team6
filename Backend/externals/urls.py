from django.urls import path
from . import views

urlpatterns = [
    # 유튜브 검색/조회
    path('search/', views.youtube_search)
]
