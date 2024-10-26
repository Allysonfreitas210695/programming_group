from datetime import timedelta
import os
from pathlib import Path
from decouple import config, Csv

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta usada para criptografar dados
SECRET_KEY = config('SECRET_KEY')

# Debug mode, deve ser False em produção
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos para o servidor
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())

# Aplicativos instalados no projeto
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # Aplicativo principal
    'corsheaders',  # Suporte para CORS
    'drf_yasg',  # Swagger UI para DRF
    'rest_framework',  # Django REST Framework
    'rest_framework.authtoken',  # Token para autenticação DRF
    'djoser',  # Sistema de gerenciamento de usuários
    "drf_spectacular",  # Ferramenta para gerar esquemas OpenAPI
    'django_filters',  # Suporte para filtros no DRF
]

# Middleware para o processamento de requisições
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuração de URLs do projeto
ROOT_URLCONF = 'programming_group.urls'

# Configuração dos templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração WSGI para o projeto
WSGI_APPLICATION = 'programming_group.wsgi.application'

# Configurações do Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Api Programming Group',
    'DESCRIPTION': 'API description',
    'VERSION': '1.0.0',
    'CONTACT': {
        'name': 'Allyson Bruno',
        'email': 'allyson.fernandes@alunos.ufersa.edu.br',
    },
    'LICENSE': {
        'name': 'License Name',
        'url': 'https://license.url',
    },
}

# Configuração do Djoser para gerenciamento de senhas
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
}

# Configuração do JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(weeks=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=4),
}

# Modelo de usuário personalizado
AUTH_USER_MODEL = 'core.User'

ASGI_APPLICATION = 'programming_group.asgi.application'

# Configuração do banco de dados
ENVIRONMENT = config('ENVIRONMENT', default='development')
if ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Validações de senha
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

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'channels': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}


# Internacionalização
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Configuração de arquivos estáticos
STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração de CORS
CORS_ORIGIN_ALLOW_ALL = True
