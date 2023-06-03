"""Throttle Settings"""

SECOND = 1
MINUTE = 60  *  SECOND
HOUR   = 60  *  MINUTE
DAY    = 24  *  HOUR
WEEK   = 7   *  DAY
MONTH  = 30  *  DAY
YEAR   = 365 *  DAY

LIMIT_DURATION = {
    's'    : SECOND,
    'min'  : MINUTE,
    'h'    : HOUR,
    'd'    : DAY,
    'w'    : WEEK,
    'month': MONTH,
    'y'    : YEAR,
}

ACTION_THROTTLE = {
    'DEFAULT_RATE': {
        'ip': '500/1:d',
        'user': '1000/1:d',
    },
    'CACHE_TIMEOUT': 60 * 60 * 24, # 1-Day
    'MIDDLEWARE_USING_CACHE': True,
    'REST_USING_CACHE': True,
}
