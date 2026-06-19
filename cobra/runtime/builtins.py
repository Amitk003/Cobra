def cobra_print(*args, sep=" ", end="\n"):
    print(*args, sep=sep, end=end)


def cobra_input(prompt=""):
    return input(prompt)


def cobra_str(x):
    return str(x)


def cobra_int(x):
    return int(x)


def cobra_bool(x):
    return bool(x)


def cobra_float(x):
    return float(x)


def cobra_len(x):
    return len(x)


def cobra_type(x):
    t = type(x).__name__
    return {"str": "string", "int": "int", "float": "float", "bool": "bool", "list": "list"}.get(t, t)


def cobra_range(start, end):
    return list(range(start, end))
