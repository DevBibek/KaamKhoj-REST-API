
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ften3!(isd-=4!$bh7f@k1^v=ma+^2-rf02b1h#h7bnxumz=yt'

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


