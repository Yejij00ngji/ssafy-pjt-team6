from django.db import models
from django.conf import settings

# 게시글
class Article(models.Model):
    CATEGORY_CHOICES = [
        ('notice', '공지사항'),
        ('study', '스터디/팀빌딩'),
        ('contest', '공모전'),
        ('qna', 'Q&A'),
        ('free', '자유게시판'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='free')
    image = models.ImageField(upload_to='community/', blank=True, null=True)
    
    # 조회수 및 추천
    views = models.PositiveIntegerField(default=0)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    
    # 공모전이나 스터디의 경우 '모집 중/완료' 상태가 필요함
    is_complete = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    
    # Q&A 게시판의 경우 '답변 채택' 기능이 중요함
    is_picked = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)