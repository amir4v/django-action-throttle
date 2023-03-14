"""
Django Action Throttle
"""

__title__ = 'Django Action Throttle'
__version__ = '0.0.1'
__author__ = 'Amirhosein Ghorbani'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022-'

# Version synonym
VERSION = __version__

from .throttle_settings import LIMIT_DURATION
from .throttle import action_throttle
