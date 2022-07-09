from .base import *

SECRET_KEY = config("SECRET_KEY")


DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())


DATABASES = {
    'default': {
        'ENGINE': config('ENGINE'),
        'NAME': config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_files')]
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = 'nyc3'
# AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')

# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_LOCATION = 'https://cradsispace.nyc3.digitaloceanspaces.com'
# AWS_DEFAULT_ACL = 'public-read'
# AWS_S3_SIGNATURE_VERSION = 's3v4'

# DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'


# MEDIA_URL =  f'https://{AWS_S3_ENDPOINT_URL}/media/'




# SECURE_SSL_REDIRECT = True

# SESSION_COOKIE_SECURE = True

# CSRF_COOKIE_SECURE = True

# SECURE_BROWSER_XSS_FILTER = True

