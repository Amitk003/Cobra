def upper(s):
    return s.upper()


def lower(s):
    return s.lower()


def split(s, sep=None):
    return s.split(sep)


def join(parts, glue=""):
    return glue.join(parts)


def replace(s, old, new, count=-1):
    return s.replace(old, new, count)


def contains(s, substr):
    return substr in s


def starts_with(s, prefix):
    return s.startswith(prefix)


def ends_with(s, suffix):
    return s.endswith(suffix)


def trim(s):
    return s.strip()


def trim_left(s):
    return s.lstrip()


def trim_right(s):
    return s.rstrip()


def length(s):
    return len(s)


def substring(s, start, end=None):
    return s[start:end] if end else s[start:]


def index_of(s, substr):
    return s.find(substr)


def to_chars(s):
    return list(s)


def capitalize(s):
    return s.capitalize()


def reverse(s):
    return s[::-1]


def is_digit(s):
    return s.isdigit()


def is_alpha(s):
    return s.isalpha()


def is_alnum(s):
    return s.isalnum()


def is_space(s):
    return s.isspace()


def pad_left(s, width, char=" "):
    return s.rjust(width, char)


def pad_right(s, width, char=" "):
    return s.ljust(width, char)


def repeat(s, count):
    return s * count
