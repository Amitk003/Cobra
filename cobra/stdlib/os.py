import os as _os
import sys as _sys


def exec(cmd):
    return _os.system(cmd)


def env(key, default=None):
    return _os.environ.get(key, default)


def set_env(key, value):
    _os.environ[key] = value


def args():
    return _sys.argv[1:]


def exit(code=0):
    _sys.exit(code)


def pid():
    return _os.getpid()


def name():
    return _os.name


def cpu_count():
    return _os.cpu_count()


def getenv(key, default=None):
    return _os.environ.get(key, default)


def hostname():
    return _os.uname().nodename if hasattr(_os, "uname") else _os.environ.get("COMPUTERNAME", "unknown")


def user():
    return _os.environ.get("USER", _os.environ.get("USERNAME", "unknown"))


def sleep(seconds):
    import time as _time
    _time.sleep(seconds)
