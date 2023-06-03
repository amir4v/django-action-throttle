from django.conf import settings

from rest_framework.throttling import BaseThrottle

from .throttle_settings import ACTION_THROTTLE as _ACTION_THROTTLE
from .throttle import action_throttle, action_throttle_using_cache

ACTION_THROTTLE = getattr(settings, 'ACTION_THROTTLE', _ACTION_THROTTLE)
REST_USING_CACHE = ACTION_THROTTLE.get('REST_USING_CACHE', _ACTION_THROTTLE['REST_USING_CACHE'])


class ActionThrottle(BaseThrottle):
    user_ip_limit = None
    user_limit = None
    ip_limit = None
    raise_exception = False
    
    def allow_request(self, request, view):
        if REST_USING_CACHE:
            return action_throttle_using_cache(request=request,
                               user_ip_limit=self.user_ip_limit,
                               user_limit=self.user_limit,
                               ip_limit=self.ip_limit,
                               raise_exception=self.raise_exception)
        else:
            return action_throttle(request=request,
                                user_ip_limit=self.user_ip_limit,
                                user_limit=self.user_limit,
                                ip_limit=self.ip_limit,
                                raise_exception=self.raise_exception)
