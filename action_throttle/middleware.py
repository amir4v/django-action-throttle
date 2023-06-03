from django.conf import settings

from .throttle_settings import ACTION_THROTTLE as _ACTION_THROTTLE
from .throttle import action_throttle, action_throttle_using_cache
from .models import Limit, Condition

ACTION_THROTTLE = getattr(settings, 'ACTION_THROTTLE', _ACTION_THROTTLE)
DEFAULT_RATE = ACTION_THROTTLE.get('DEFAULT_RATE', _ACTION_THROTTLE['DEFAULT_RATE'])
MIDDLEWARE_USING_CACHE = ACTION_THROTTLE.get('MIDDLEWARE_USING_CACHE', _ACTION_THROTTLE['MIDDLEWARE_USING_CACHE'])


class ThrottleMiddleware:
    def __init__(self, get_response):
        self.ip_limit = Limit.objects.get_or_create(name='DEFAULT_IP_THROTTLE_RATE')[0]
        self.ip_limit.condition_set.all().delete()
        Condition(condition=DEFAULT_RATE.get('ip'), limit=self.ip_limit).save()
        self.ip_limit = self.ip_limit.name
        #
        self.user_limit = Limit.objects.get_or_create(name='DEFAULT_USER_THROTTLE_RATE')[0]
        self.user_limit.condition_set.all().delete()
        Condition(condition=DEFAULT_RATE.get('user'), limit=self.user_limit).save()
        self.user_limit = self.user_limit.name
        #
        self.get_response = get_response
    
    def __call__(self, request):
        if MIDDLEWARE_USING_CACHE:
            action_throttle_using_cache(request, user_limit=self.user_limit, ip_limit=self.ip_limit, raise_exception=True)
        else:
            action_throttle(request, user_limit=self.user_limit, ip_limit=self.ip_limit, raise_exception=True)
        #
        response = self.get_response(request)
        return response
