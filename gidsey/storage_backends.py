from abc import ABC

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class MediaStorage(S3Boto3Storage, ABC):
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False


class LocalMediaStorage(MediaStorage, ABC):
    location = 'local/media'


class ProductionMediaStorage(MediaStorage, ABC):
    location = 'prod/media'
