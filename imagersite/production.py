import dj_database_url
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = [
    "ec2-52-88-19-175.us-west-2.compute.amazonaws.com", "localhost"
    ]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SECRET_KEY = os.environ.get("SECRET_KEY")

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://{}@localhost:5432/imager_site'
        .format(os.environ.get('USER')))
}
