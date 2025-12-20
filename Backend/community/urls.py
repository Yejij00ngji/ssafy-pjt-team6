from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles_view_create),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/comments/', views.comment_create),
]
