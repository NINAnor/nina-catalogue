from appconf import AppConf
from django.conf import settings


class MapsConf(AppConf):
    API_PREFIX = "api-1.0.0"
    API_KEY = None
