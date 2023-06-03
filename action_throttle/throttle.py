from time import time

from django.conf import settings
from django.core.exceptions import BadRequest
from django.core.cache import cache

from .throttle_settings import ACTION_THROTTLE as _ACTION_THROTTLE
from .models import Memory, Limit, Condition
from .utils import get_client_ip

ACTION_THROTTLE = getattr(settings, 'ACTION_THROTTLE', _ACTION_THROTTLE)
timeout = CACHE_TIMEOUT = ACTION_THROTTLE.get('CACHE_TIMEOUT', _ACTION_THROTTLE['CACHE_TIMEOUT'])


def action_throttle(request,
                    user_ip_limit=None, user_limit=None, ip_limit=None,
                    raise_exception=False):
    """Limit Throttle function for an action"""
    # TODO: limit for user or ip, combined together.
    
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
    
    # v-1
    # limit = Limit.objects.get(name=the_limit)
    # conditions = limit.get_conditions()
    #
    # v-2
    conditions = Condition.objects.filter(limit__name=the_limit).order_by('-pot')
    #
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


def action_throttle_using_cache(request,
                    user_ip_limit=None, user_limit=None, ip_limit=None,
                    raise_exception=False):
    """Limit Throttle function for an action"""
    # TODO: limit for user or ip, combined together.
    
    now = int(time())
    
    user = request.user
    if str(user) == 'AnonymousUser':
        USER_IP = 'ip'
        ip = get_client_ip(request)
    else:
        USER_IP = 'user'
    
    if user_ip_limit:
        the_limit = user_ip_limit
    elif user_limit and ip_limit:
        if USER_IP == 'ip':
            the_limit = ip_limit
        else:
            the_limit = user_limit
    elif not (user_ip_limit or user_limit or ip_limit):
        raise Exception('At least one of these must be initiate: user_ip_limit or user_limit or ip_limit')
    else:
        raise Exception('WTF!')
    
    # v-1
    # limit = Limit.objects.get(name=the_limit)
    # conditions = limit.get_conditions()
    #
    # v-2
    conditions = Condition.objects.select_related('limit').filter(limit__name=the_limit).order_by('-pot')
    #
    """
    Getting conditions sorted descending.
    Because when you break a bigger Condition, That means you broke the whole limitation
    and smaller conditions.
    """
    
    for condition in conditions:
        """When you break a bigger Condition, You broke the whole limitation."""
        
        """We need to remember the number of requests per User/IP for each Condition."""
        if USER_IP == 'ip':
            key = f'{ip}_{condition.limit.name}_{condition.condition}'
            memory = cache.get(key, None)
        else:
            if user.USERNAME_FIELD == 'username':
                key = f'{user.username}_{condition.limit.name}_{condition.condition}'
            elif user.USERNAME_FIELD == 'email':
                key = f'{user.email}_{condition.limit.name}_{condition.condition}'
            memory = cache.get(key, None)
        if not memory:
            memory = value = f'1-{now}'
            cache.set(key, value, timeout)
            continue
        
        memory = {
            'hit': int(memory.split('-')[0]),
            'from': int(memory.split('-')[1])
        }
        hit, duration = condition.hit_duration
        """
        Until means a User must have a limited number of requests from
        the time of them first request to that limited and conditioned time period.
        """
        until = memory['from'] + duration
        
        if (now < until) and (memory['hit'] >= hit):
            """If the User crossed the limit condition in a shorter time than we determined."""
            if raise_exception:
                raise BadRequest("You've reached the limit.")
            else:
                return False
        elif now >= until:
            """If the user passes the time limit, it will be refreshed(like the first request)."""
            hit = memory['hit'] = 1
            From = memory['from'] = now
            
            value = f'{hit}-{From}'
            cache.set(key, value, timeout)
        else:
            """Here, the User is in the allowed range of time and number of requests,
            So the number of request will be +1 and continuation."""
            hit = memory['hit'] = memory['hit'] + 1
            From = memory['from']
            
            value = f'{hit}-{From}'
            cache.set(key, value, timeout)
    
    """If the User passes every Limit Conditions, The User will be allowed to do the action."""
    return True
