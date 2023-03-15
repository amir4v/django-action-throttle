from time import time

from django.core.exceptions import BadRequest

from .models import Memory, Limit
from .utils import get_client_ip


def action_throttle(request,
                    user_ip_limit=None, user_limit=None, ip_limit=None,
                    raise_exception=False):
    """Limit Throttle function for an action"""
    
    now = int(time())
    
    user = request.user
    if str(user) == 'AnonymousUser':
        USER_IP = 'ip'
        ip = get_client_ip(request)
    else:
        USER_IP = 'user'
    
    if user_ip_limit and (not (user_limit and ip_limit)):
        the_limit = user_ip_limit
    elif user_limit and ip_limit:
        if USER_IP == 'ip':
            the_limit = ip_limit
        else:
            the_limit = user_limit
    elif user_limit and (not ip_limit):
        if USER_IP == 'ip':
            raise Exception('There is no User! (User is Anonymous)')
        the_limit = user_limit
    elif (not user_limit) and ip_limit:
        the_limit = ip_limit
    else:
        raise Exception('At least one of these must be initiate: user_ip_limit or user_limit or ip_limit')
    
    limit = Limit.objects.get(name=the_limit)
    
    conditions = limit.get_conditions()
    """
    Getting conditions sorted descending.
    Because when you break a bigger Condition, That means you broke the whole limitation
    and smaller conditions.
    """
    
    for condition in conditions:
        """When you break a bigger Condition, You broke the whole limitation."""
        
        """We need to remember the number of requests per User/IP for each Condition."""
        if USER_IP == 'ip':
            memory, created = Memory.objects.get_or_create(ip=ip, condition=condition)
        else:
            memory, created = Memory.objects.get_or_create(user=user, condition=condition)
        if created:
                memory.hit = 1
                memory.From = now
                memory.save()
                continue
        
        hit, duration = condition.hit_duration
        """
        Until means a User must have a limited number of requests from
        the time of them first request to that limited and conditioned time period.
        """
        until = memory.From + duration
        
        if (now < until) and (memory.hit >= hit):
            """If the User crossed the limit condition in a shorter time than we determined."""
            if raise_exception:
                raise BadRequest("You've reached the limit.")
            else:
                return False
        elif now >= until:
            """If the user passes the time limit, it will be refreshed(like the first request)."""
            memory.hit = 1
            memory.From = now
            memory.save()
        else:
            """Here, the User is in the allowed range of time and number of requests,
            So the number of request will be +1 and continuation."""
            memory.hit += 1
            memory.save()
    
    """If the User passes every Limit Conditions, The User will be allowed to do the action."""
    return True
