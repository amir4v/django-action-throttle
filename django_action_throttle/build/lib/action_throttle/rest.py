from rest_framework.throttling import BaseThrottle

from .throttle import action_throttle


class ActionThrottle(BaseThrottle):
    user_ip_limit = None
    user_limit = None
    ip_limit = None
    raise_exception = False
    
    def allow_request(self, request, view):
        return action_throttle(request=request,
                               user_ip_limit=self.user_ip_limit,
                               user_limit=self.user_limit,
                               ip_limit=self.ip_limit,
                               raise_exception=self.raise_exception)
