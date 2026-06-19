import math as _math

pi = _math.pi
e = _math.e
tau = _math.tau
inf = _math.inf
nan = _math.nan


def sqrt(x):
    return _math.sqrt(x)


def sin(x):
    return _math.sin(x)


def cos(x):
    return _math.cos(x)


def tan(x):
    return _math.tan(x)


builtins_abs = abs
builtins_max = max
builtins_min = min
builtins_round = round


def abs(x):
    return _math.fabs(x) if isinstance(x, float) else builtins_abs(x)


def max(a, *args):
    return builtins_max(a, *args)


def min(a, *args):
    return builtins_min(a, *args)


def floor(x):
    return _math.floor(x)


def ceil(x):
    return _math.ceil(x)


def round(x, ndigits=0):
    return builtins_round(x, ndigits)


def pow(x, y):
    return x ** y


def log(x, base=_math.e):
    return _math.log(x, base)


def log10(x):
    return _math.log10(x)


def exp(x):
    return _math.exp(x)


def degrees(x):
    return _math.degrees(x)


def radians(x):
    return _math.radians(x)


def is_nan(x):
    return _math.isnan(x)


def is_inf(x):
    return _math.isinf(x)
