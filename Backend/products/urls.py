from django.urls import path
from . import views

urlpatterns = [
    # 전체 상품 목록 조회
    path('products/', views.products),
    path('products/<int:pk>/', views.product_details),
    path('subscriptions/', views.subscriptions),
    path('subscriptions/<int:subscription_id>/', views.subscriptions),
    path('recommendations/', views.get_recommendations),
    path('recommendations/survey/', views.submit_survey),  # 미동의자 로직
    path('mydata/disconnect/', views.disconnect_mydata),
    path('mydata/update/', views.update_mydata), 
    # path('user/status/', views.get_user_status), # 이 유저 상태 가져오기
]