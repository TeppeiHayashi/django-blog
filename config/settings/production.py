'''
本番環境の設定ファイル
'''

import django_heroku
import dj_database_url
from config.aws.conf import *  # noqa
from config.settings.base import *  # noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

SECRET_KEY = os.environ.get('SECRET_KEY')  # noqa E405

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangogirls',
        'USER': 'name',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # noqa E405

MEDIA_URL = 'https://%s/%s/' % (AWS_S3_URL, 'media')  # noqa E405

db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)

django_heroku.settings(locals())
