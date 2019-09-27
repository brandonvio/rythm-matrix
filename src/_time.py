import pytz
import time
from datetime import datetime


class _time:
    utc = pytz.UTC

    @staticmethod
    def utc_now_localized():
        return utc.localize(datetime.utcnow())

    @staticmethod
    def utc_now():
        return datetime.utcnow()

    @staticmethod
    def time():
        return time.time()
