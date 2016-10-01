import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = [
    "ec2-52-88-19-175.us-west-2.compute.amazonaws.com", "localhost"
    ]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
