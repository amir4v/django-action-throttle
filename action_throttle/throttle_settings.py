"""Throttle Settings"""

LIMIT_DURATION_s       = 1
LIMIT_DURATION_min     = 60  *  LIMIT_DURATION_s
LIMIT_DURATION_h       = 60  *  LIMIT_DURATION_min
LIMIT_DURATION_d       = 24  *  LIMIT_DURATION_h
LIMIT_DURATION_w       = 7   *  LIMIT_DURATION_d
LIMIT_DURATION_month   = 30  *  LIMIT_DURATION_d
LIMIT_DURATION_y       = 365 *  LIMIT_DURATION_d

LIMIT_DURATION = {
    's'    : LIMIT_DURATION_s,
    'min'  : LIMIT_DURATION_min,
    'h'    : LIMIT_DURATION_h,
    'd'    : LIMIT_DURATION_d,
    'w'    : LIMIT_DURATION_w,
    'month': LIMIT_DURATION_month,
    'y'    : LIMIT_DURATION_y,
}
