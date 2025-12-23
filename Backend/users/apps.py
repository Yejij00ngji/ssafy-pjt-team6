from django.apps import AppConfig
import joblib
import os

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    scaler = None
    kmeans = None

    def ready(self):
        # 서버 시작 시 모델 로드
        from django.conf import settings
        scaler_path = os.path.join(settings.ML_MODELS_DIR, 'financial_scaler.pkl')
        if os.path.exists(scaler_path):
            UsersConfig.scaler = joblib.load(scaler_path)