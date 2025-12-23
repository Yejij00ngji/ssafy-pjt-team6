# users/adapters.py (파일 위치 확인 필요)
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        """
        소셜 로그인 시 전달받은 데이터를 바탕으로 User 인스턴스를 생성할 때 호출됩니다.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # 소셜 계정에서 제공하는 이메일이 있다면 username으로 강제 할당
        email = data.get('email')
        if email:
            user.username = email
            
        return user