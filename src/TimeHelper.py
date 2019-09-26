import pytz
from datetime import datetime

utc = pytz.UTC


def utc_now_localized():
    return utc.localize(datetime.utcnow())


def utc_now():
    return datetime.utcnow()
