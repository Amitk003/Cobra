from datetime import datetime as _datetime
from datetime import date as _date
from datetime import timedelta as _timedelta


def now():
    return _datetime.now().isoformat()


def today():
    return _date.today().isoformat()


def timestamp():
    return _datetime.now().timestamp()


def parse(date_str, fmt="%Y-%m-%d"):
    return _datetime.strptime(date_str, fmt).isoformat()


def format(dt, fmt="%Y-%m-%d %H:%M:%S"):
    return _datetime.fromisoformat(dt).strftime(fmt)


def year(dt=None):
    if dt:
        return _datetime.fromisoformat(dt).year
    return _datetime.now().year


def month(dt=None):
    if dt:
        return _datetime.fromisoformat(dt).month
    return _datetime.now().month


def day(dt=None):
    if dt:
        return _datetime.fromisoformat(dt).day
    return _datetime.now().day


def hour(dt=None):
    if dt:
        return _datetime.fromisoformat(dt).hour
    return _datetime.now().hour


def minute(dt=None):
    if dt:
        return _datetime.fromisoformat(dt).minute
    return _datetime.now().minute


def second(dt=None):
    if dt:
        return _datetime.fromisoformat(dt).second
    return _datetime.now().second


def add_days(dt, days):
    d = _datetime.fromisoformat(dt)
    return (d + _timedelta(days=days)).isoformat()


def add_hours(dt, hours):
    d = _datetime.fromisoformat(dt)
    return (d + _timedelta(hours=hours)).isoformat()


def add_minutes(dt, minutes):
    d = _datetime.fromisoformat(dt)
    return (d + _timedelta(minutes=minutes)).isoformat()


def seconds_between(dt1, dt2):
    d1 = _datetime.fromisoformat(dt1)
    d2 = _datetime.fromisoformat(dt2)
    return abs((d2 - d1).total_seconds())


def days_between(dt1, dt2):
    d1 = _datetime.fromisoformat(dt1)
    d2 = _datetime.fromisoformat(dt2)
    return abs((d2 - d1).days)
