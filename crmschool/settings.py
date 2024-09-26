from pathlib import Path
import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from decouple import config

from django.core.exceptions import ImproperlyConfigured
load_dotenv()

LOG_FILENAME = 'django.log'

logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.ERROR,  # або logging.DEBUG для отримання докладніших журналів
    format='%(asctime)s - %(levelname)s - %(message)s'
)

handler = RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == 'True'
DEBUG = False

# ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOST', default='').split(',')
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.0.210', '0.0.0.0', 'webuniverseua.com', 'www.webuniverseua.com', '161.35.66.41']
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'http://161.35.66.41',
    'http://192.168.0.210',
    'http://localhost',
    'http://webuniverseua.com',
    'http://www.webuniverseua.com',
    'http://webuniverseua.com:81'
]
AUTH_USER_MODEL = 'users.CustomUser'

SESSION_COOKIE_AGE = 60 * 60  # 60 minutes
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'centers',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crmschool.middleware.session_expire_redirect_middleware.SessionExpireRedirectMiddleware',
]


ROOT_URLCONF = 'crmschool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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

WSGI_APPLICATION = 'crmschool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'postgres',
#         'PORT': '5432',
#     }
# }

POSTGRES_DB = os.getenv("POSTGRES_DB")  # database name
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")  # database password
POSTGRES_USER = os.getenv("POSTGRES_USER")  # username
POSTGRES_HOST = os.getenv("POSTGRES_HOST")  # database host
POSTGRES_PORT = os.getenv("POSTGRES_PORT")  # database port


if all([POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_HOST, POSTGRES_PORT]):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": POSTGRES_DB,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
            "HOST": POSTGRES_HOST,
            "PORT": POSTGRES_PORT,
        }
    }
else:
    raise ImproperlyConfigured("Database configuration is incomplete. Please check your environment variables.")


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'uk-ua'

TIME_ZONE = 'Europe/Kyiv'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Secure cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = None
