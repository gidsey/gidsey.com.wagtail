from .base import *

# DEBUG = False

try:
    from .local import *
except ImportError:
    pass

SECRET_KEY = os.getenv('CR_SECRET_KEY', ImproperlyConfigured('CR_SECRET_KEY not set'))

hosts = os.getenv('CR_HOSTS', ImproperlyConfigured('CR_HOSTS not set'))
try:
    ALLOWED_HOSTS = str(hosts).split(',')
except Exception as e:
    raise ImproperlyConfigured('CR_HOSTS could not be parsed. {}'.format(e))


# MEDIA_ROOT = f'{AWS_S3_ENDPOINT_URL}/'
MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/'

# DEFAULT_FILE_STORAGE = 'gidsey.storage_backends.ProductionMediaStorage'


# Sentry
sentry_sdk.init(
    dsn="https://2a95237b7cfa43eeb34527e15f7dc8f2@o458905.ingest.sentry.io/6070574",
    integrations=[DjangoIntegration()],
    environment='production',

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Production security settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
