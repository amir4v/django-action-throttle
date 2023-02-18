from time import time

from django.core.exceptions import BadRequest

from .models import User, Memory, Limit, Condition


def action_throttle(user: User, limit_name, raise_exception=True):
    """Limit Throttle function for an action"""
    
    now = int(time())
    
    limit = Limit.objects.get(name=limit_name)
    """
    Getting conditions sorted descending.
    Because when you break a bigger Condition, That means you broke the whole limitation
    and smaller conditions.
    """
    conditions = limit.get_conditions()
    
    for condition in conditions:
        """When you break a bigger Condition, You broke the whole limitation."""
        
        """We need to remember the number of requests per User for each Condition."""
        memory, created = Memory.objects.get_or_create(user=user, condition=condition)
        if created:
                memory.hit = 1
                memory.From = now
                memory.save()
                return True
        
        hit, duration = condition.hit_duration
        """
        Until means a User must have a limited number of requests from
        the time of them first request to that limited and conditioned time period.
        """
        until = memory.From + duration
        
        if (now < until) and (memory.hit >= hit):
            """If the User crossed the limit condition in a shorter time than we determined."""
            if raise_exception:
                raise BadRequest("You've reached the limit.") # TODO: Proper message?
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
