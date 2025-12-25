from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from django.shortcuts import get_object_or_404
from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def articles_view_create(request):
    # 1. GET: 게시글 목록 조회 (카테고리 필터링 포함)
    if request.method == 'GET':
        category = request.GET.get('category')
        articles = Article.objects.all().order_by('-created_at')
        
        if category:
            articles = articles.filter(category=category)
            
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    # 2. POST: 새로운 게시글 작성
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        # 상세 조회 시 조회수 증가 로직 (선택)
        article.views += 1
        article.save()
        serializer = ArticleSerializer(article, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != article.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user != article.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 좋아요 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 로그인한 유저만 가능
def article_like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    user = request.user

    # 좋아요 토글 로직
    if article.like_users.filter(pk=user.pk).exists():
        # 이미 좋아요를 누른 경우 -> 취소
        article.like_users.remove(user)
        is_liked = False
    else:
        # 좋아요를 누르지 않은 경우 -> 추가
        article.like_users.add(user)
        is_liked = True
    
    context = {
        'is_liked': is_liked,
        'like_count': article.like_users.count()
    }
    return Response(context)    

# 댓글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'PUT':
        if request.user != comment.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    elif request.method == 'DELETE':
        if request.user != comment.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
