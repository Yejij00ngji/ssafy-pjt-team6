# community/serializers.py
from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()  # settings에 정의된 내 커스텀 user 모델 가져오기

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username') # nickname이 있다면 포함

class ArticleListSerializer(serializers.ModelSerializer):
    # 작성자 정보를 상세하게 포함 (인프런 스타일)
    user = UserSerializer(read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'user', 'title', 'category', 'is_complete', 'views', 
                  'comment_count', 'like_count', 'created_at')

# 댓글
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # 댓글 작성자 정보

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article', 'user')

class ArticleSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    # article 모델의 related_name='comments'를 사용하여 댓글 목록을 가져옴
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'views', 'like_users')