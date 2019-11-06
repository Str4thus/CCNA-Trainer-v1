import os
from .defaults import *


SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

STATIC_URL = '/static/'
STATIC_ROOT = '/static_files/'

DEBUG = False
ALLOWED_HOSTS = ['0.0.0.0', '.strathus-dev.me', '127.0.0.1', '192.168.99.100']