from django.conf import settings

from .throttle_settings import DEFAULT_THROTTLE_RATE as _DEFAULT_THROTTLE_RATE
from .throttle import action_throttle, action_throttle_with_cache
from .models import Limit, Condition

DEFAULT_THROTTLE_RATE = getattr(settings, 'DEFAULT_THROTTLE_RATE', None) \
                        or \
                        _DEFAULT_THROTTLE_RATE


class ThrottleMiddleware:
    def __init__(self, get_response):
        self.ip_limit = Limit.objects.get_or_create(name='DEFAULT_IP_THROTTLE_RATE')[0]
        self.ip_limit.condition_set.all().delete()
        Condition(condition=DEFAULT_THROTTLE_RATE.get('ip'), limit=self.ip_limit).save()
        self.ip_limit = self.ip_limit.name
        #
        self.user_limit = Limit.objects.get_or_create(name='DEFAULT_USER_THROTTLE_RATE')[0]
        self.user_limit.condition_set.all().delete()
        Condition(condition=DEFAULT_THROTTLE_RATE.get('user'), limit=self.user_limit).save()
        self.user_limit = self.user_limit.name
        #
        self.get_response = get_response
    
    def __call__(self, request):
        action_throttle(request, user_limit=self.user_limit, ip_limit=self.ip_limit, raise_exception=True)
        action_throttle_with_cache(request, user_limit=self.user_limit, ip_limit=self.ip_limit, raise_exception=True)
        #
        response = self.get_response(request)
        return response
