from django.urls import path
from . import views

urlpatterns = [
    # 데이터 수집 및 저장 URL 추가
    path('save-deposit-products/', views.save_deposit_products),
    # 전체 상품 목록 조회
    # path('deposit-products/', views.deposit_products),
]
