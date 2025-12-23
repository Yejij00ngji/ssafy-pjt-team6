from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles_view_create),  # 게시글 조회 및 생성
    path('<int:article_pk>/', views.article_detail),  # 게시글 상세 (삭제, 수정)
    path('<int:article_pk>/comments/', views.comment_create),  # 댓글 생성
    path('comments/<int:comment_pk>/', views.comment_detail),  # 댓글 상세 (삭제, 수정)
    path('<int:article_pk>/like/', views.article_like),
]
