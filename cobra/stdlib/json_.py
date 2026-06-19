import json as _json


def parse(s):
    return _json.loads(s)


def stringify(obj, pretty=False):
    if pretty:
        return _json.dumps(obj, indent=2)
    return _json.dumps(obj)


def read_file(path):
    with open(path, "r") as f:
        return _json.load(f)


def write_file(path, obj, pretty=False):
    with open(path, "w") as f:
        if pretty:
            _json.dump(obj, f, indent=2)
        else:
            _json.dump(obj, f)
