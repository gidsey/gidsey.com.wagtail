from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class PublicMediaStorage(S3Boto3Storage):
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = 'public-read'



