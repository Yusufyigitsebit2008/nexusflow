"""
Django settings for config project.
"""

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv # .env okumak için

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-varsayilan-key-degistir-bunu')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

ALLOWED_HOSTS = ["*"] 

# 4. UYGULAMALAR
INSTALLED_APPS = [
    'daphne', # ASGI için en üstte olmalı
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 3. Parti Paketler
    'rest_framework',
    'corsheaders',
    'channels',
    
    # Bizim Uygulamalarımız
    'users',
    'boards',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # En üstlerde olmalı
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = "config.asgi.application"

# 5. VERİTABANI (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nexusflow_db',
        'USER': 'nexusflow_user',
        'PASSWORD': 'nexusflow_password',
        'HOST': '127.0.0.1',
        'PORT': '5433', # Senin port ayarın
    }
}

# 6. KULLANICI MODELİ
AUTH_USER_MODEL = 'users.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 7. STATİK VE MEDYA DOSYALARI
STATIC_URL = 'static/'

# Dosya yükleme (Attachment) için gerekli:
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 8. WEBSOCKET (CHANNELS) AYARLARI
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# 9. REST FRAMEWORK & JWT AYARLARI
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', 
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# 10. CORS AYARLARI (Frontend'e İzin Ver)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]