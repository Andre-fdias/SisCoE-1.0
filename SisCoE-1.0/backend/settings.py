import os
from pathlib import Path
from django.contrib.messages import constants
from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())
AUTH_USER_MODEL = 'accounts.User'

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# Application definition

INSTALLED_APPS = [
    'backend.accounts',  # <<<
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps de terceiros
    'django_extensions',
    'widget_tweaks',
    'compressor',
    'django_seed',
     'fontawesomefree',
    # minhas apps
    'backend.core',
    'backend.crm',
    'backend.efetivo',
    'backend.adicional',
    'backend.faisca',
    'backend.rpt',
    'backend.bm',
    'backend.municipios',
    'backend.documentos',
    'backend.agenda',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'backend.accounts.middleware.UserActionLoggingMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#   'default': {
#      'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': BASE_DIR / 'db.sqlite3',
# }
# }

# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'siscoe_db',
        'USER': 'postgres',
        'PASSWORD': 'davi2807',
        'HOST': 'localhost',  # Alterado de 'db' para 'localhost'
        'PORT': '5432',        # Porta padrão do PostgreSQL
    }
}

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
EMAIL_HOST = config('EMAIL_HOST', 'localhost')  # localhost 0.0.0.0
EMAIL_PORT = config('EMAIL_PORT', 1025, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

DECIMAL_SEPARATOR = ','


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
RUN_SERVER_PORT = 8090  # Escolha uma porta diferente (por exemplo, 8081, 8090)


LOGIN_REDIRECT_URL = 'core:index'

MESSAGE_TAGS = {
 constants.DEBUG: 'alert-primary',
 constants.ERROR: 'alert-danger',
 constants.SUCCESS: 'alert-success',
 constants.INFO: 'alert-info',
 constants.WARNING: 'alert-warning',
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

GROQ_API_KEY = config('GROQ_API_KEY')

AUTH_USER_MODEL = 'accounts.User'

ADMIN_DEFAULT_PERMISSIONS = [
    'add', 'change', 'delete', 'view'
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

