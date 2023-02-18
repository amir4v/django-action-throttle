from django.db import models
from django.contrib.auth import get_user_model

from .throttle_settings import LIMIT_DURATION


User = get_user_model()


class Memory(models.Model):
    """It remembers who made how many requests from when."""
    
    # ip = models.CharField(max_length=100, unique=True, db_index=True, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # group
    
    """Number of requests"""
    hit = models.IntegerField(default=0)
    
    """When the first request was made (in epoch format)"""
    From = models.IntegerField(default=0)
    
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user} - ({self.condition}) - {self.hit}'


class Limit(models.Model):
    """A Limit can have multiple conditions."""
    
    name = models.CharField(max_length=100, unique=True, db_index=True, blank=False, null=False)
    
    def get_conditions(self): # TODO: Refactoring
        conditions = self.condition_set.all()
        conditions = [(condition, condition.hit_duration[1]) for condition in conditions]
        conditions = sorted(conditions, key=lambda c: c[1], reverse=True)
        conditions = [condition[0] for condition in conditions]
        return conditions
    
    def __str__(self):
        return self.name


class Condition(models.Model):
    """
    A Condition with format like: hit/per:duration
    
    Example: 123/1:h
        It means: You can have 123 requests per one hour
    
    Durations: s/min/h/d/w/month/y
        s: Second
        min: Minute
        h: Hour
        d: Day
        w: Week
        month: Month
        y: Year
    """
    
    condition = models.CharField(max_length=100, blank=False, null=False) # TODO: Should be unique?
    limit = models.ForeignKey(Limit, on_delete=models.CASCADE)
    
    @property
    def hit_duration(self):
        """This property converts the 'Condition' to hit, seconds(duration)."""
        
        hit, n_duration = self.condition.split('/')        
        n, duration = n_duration.split(':')
        seconds = int(n) * LIMIT_DURATION.get(duration)
        
        return int(hit), seconds
    
    def __str__(self):
        return f'{self.limit} - {self.condition}'
