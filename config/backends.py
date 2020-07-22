from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    file_overwrite = False
    location = settings.STATIC_URL


class MediaStorage(S3Boto3Storage):
    file_overwrite = False
    location = settings.MEDIA_URL
