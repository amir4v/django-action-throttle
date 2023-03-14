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
