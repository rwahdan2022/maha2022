AWS_ACCESS_KEY_ID = 'AKIAV6AB5EJOASMYI555'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'mahahabib2022'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
DEFAULT_FILE_STORAGE = 'asset_manager.custom_storages.MediaStorage'
#DEFAULT_FILE_STORAGE = '{appname}.settings.aws.storage_backends.MediaStorage'
#DEFAULT_FILE_STORAGE = 'mysite.storage_backends.MediaStorage' 