from __future__ import unicode_literals

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    'podcast',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'NAME': None,
        },
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    }
]

STATIC_URL = '/static/'

USE_TZ = True

ROOT_URLCONF = 'podcast.urls'

import django
django.setup()
