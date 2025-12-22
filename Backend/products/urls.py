from django.urls import path
from . import views

urlpatterns = [
    # 전체 상품 목록 조회
    # path('deposit-products/', views.deposit_products),
    path('products/', views.products),
    path('products/<int:pk>/', views.product_details),
    path('subscriptions/', views.subscriptions),
]
