from api_server.settings.base import *
import os

DEBUG = True
ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('APP_DB_ENGINE', 'django.db.backends.sqlite3'),
#         'NAME': os.environ.get('DB_NAME', 'db.sqlite'),
#         'USER': os.environ.get('DB_USER', ''),
#         'PASSWORD': os.environ.get('DB_PASSWORD', ''),
#         'HOST': os.environ.get('DB_HOST', None),
#         'PORT': os.environ.get('DB_PORT', None),
#         }
#         }
#
# # #개발 CHANNEL
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [(os.environ.get('CHANNEL_HOSTS'), 6379)],
#         },
#     },
# }
#
# SECRET_KEY = os.environ.get('SECRET_KEY', 'unsafe-secret-key')
# algorithm = os.environ.get('algorithm')


#운영DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rds-pleasy',
        'USER': 'root',
        'PASSWORD': 'muzip1234',
        'HOST': 'rds-pleasy.cmlxitxykyhn.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

# #개발 CHANNEL
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

SECRET_KEY = 'django-insecure-1g7a2v+aq5nh4x3s2vulna7u18(8i8kv=)_qc7u$bi6m5_#tz%'

algorithm='HS256'
