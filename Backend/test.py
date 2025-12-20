import json
import random
from datetime import date, timedelta

def generate_users(count=100):
    users = []
    # 'password123'을 Django 기본 알고리즘(pbkdf2_sha256)으로 해싱한 값입니다.
    # 이 값을 넣어야 실제로 프론트엔드에서 로그인이 가능합니다.
    hashed_password = "pbkdf2_sha256$1000000$wBGc085ipgtGdui1elcfPC$ewaG4QfLf90wYtg/GLLHZRbaRLI25h277hYoVIeVIys="

    for i in range(1, count + 1):
        # 랜덤 생년월일 (20세 ~ 50세 사이)
        days_ago = random.randint(7300, 18250)
        birth = date.today() - timedelta(days=days_ago)
        
        user_data = {
            "model": "users.user",  # ★중요: 본인의 User 모델이 있는 '앱이름.user'로 수정하세요
            "pk": i,
            "fields": {
                "username": f"user{i}",
                "password": hashed_password,
                "email": f"user{i}@example.com",
                "nickname": f"nickname{i}",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "date_joined": "2024-01-01T00:00:00Z",
                "birth_date": birth.isoformat(),
                "salary": random.randint(3000, 12000) * 10000, # 3천만 ~ 1억 2천
                "possessions": random.randint(1000, 50000) * 10000, # 1천만 ~ 5억
                "is_mydata_agreed": random.choice([True, False])
            }
        }
        users.append(user_data)

    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    print(f"✅ {count}명의 유저 데이터가 users.json으로 생성되었습니다.")

if __name__ == "__main__":
    generate_users(100)