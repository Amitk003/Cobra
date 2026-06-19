# Cobra Runtime — built-in functions available to all Cobra programs


def cobra_print(*args, sep=" ", end="\n"):
    """print() built-in"""
    print(*args, sep=sep, end=end)


def cobra_input(prompt=""):
    """input() built-in"""
    return input(prompt)


def cobra_str(x):
    """str() type conversion"""
    return str(x)


def cobra_int(x):
    """int() type conversion"""
    return int(x)


def cobra_bool(x):
    """bool() type conversion"""
    return bool(x)


def cobra_float(x):
    """float() type conversion"""
    return float(x)


def cobra_len(x):
    """len() built-in"""
    return len(x)


def cobra_type(x):
    """type() built-in — returns type name as string"""
    t = type(x).__name__
    return {"str": "string", "int": "int", "float": "float", "bool": "bool", "list": "list"}.get(t, t)


def cobra_range(start, end):
    """range() built-in"""
    return list(range(start, end))
