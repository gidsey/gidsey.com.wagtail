from .base import *
import socket


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', ImproperlyConfigured('SECRET_KEY not set'))

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
]

MIDDLEWARE = MIDDLEWARE + [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Sentry
sentry_sdk.init(
    dsn="https://2a95237b7cfa43eeb34527e15f7dc8f2@o458905.ingest.sentry.io/6070574",
    integrations=[DjangoIntegration()],
    environment='local',

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)



# Debug Toolbar
INTERNAL_IPS = ['127.0.0.1', ]

# tricks to have debug toolbar when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + '1']

try:
    from .local import *
except ImportError:
    pass
