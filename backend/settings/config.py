#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from json_environ import Environ
from django.conf import settings as dj_settings
import django

import filters

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BACKEND_DIR, '..', '.env.json')

env = Environ(path=ENV_PATH)

DEBUG = env("DEBUG", default=True)
SECRET_KEY = env("SECRET_KEY", default="kminvupn=7dbw70e!#njo8qas2bx$tmw$nv1pt$g30&+f4(8c)")

REDIS_LOCATION = '{0}/{1}'.format(env('REDIS_URL', default='redis://127.0.0.1:6379'), 0)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'TIMEOUT': None,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
                                        # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }
    }
}
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': os.path.join(BACKEND_DIR, '..', 'cache'),
        }
    }

dj_settings.configure(CACHES=CACHES, DEBUG=DEBUG)
django.setup()

settings = {
    'TEMPLATES': {
        'ROOT_DIR': 'templates',     # Include the 'templates/' directory.
        'PACKAGE_DIRS': ['apistar']  # Include the built-in apistar templates.
    },
    'STATICS': {
        'ROOT_DIR': 'static',       # Include the 'statics/' directory.
        'PACKAGE_DIRS': ['apistar']  # Include the built-in apistar static files.
    }
}


