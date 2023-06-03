# Django Action Throttle

## Installation
```
pip install django-action-throttle
```

## How to use:
1-
```
Add 'action_throttle' to INSTALLED_APPS in the settings.py
```

2- Run these commands in your terminal:
```
python manage.py makemigrations action_throttle
python manage.py migrate
```

3- Go to the admin page and create at least one Limit and one or more Conditions for that Limit.

4- Condition formatting is like:
```
hit/per:duration

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
```

5- Then wherever in your project you want to restrict, use the action_throttle or action_throttle_using_cache function:
```
from action_throttle.throttle import action_throttle, action_throttle_using_cache
```

6- And then you can use it like:
```
...
action_throttle(request, 'limit-name', raise_exception=True)
# or
action_throttle_using_cache(request, 'limit-name', raise_exception=True)
...
```

7- Note that if you want use action-throttle using cache, you have to configure CACHE in the settings.py like this:
```
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

## Contributing
If you would like to contribute to this project, please feel free to submit a pull request or submit issues. We welcome all contributions and appreciate your help in improving this project.
