import os as _os
import shutil as _shutil


def read(path):
    with open(path, "r") as f:
        return f.read()


def write(path, content):
    with open(path, "w") as f:
        f.write(content)


def read_lines(path):
    with open(path, "r") as f:
        return f.readlines()


def write_lines(path, lines):
    with open(path, "w") as f:
        f.writelines(lines)


def append(path, content):
    with open(path, "a") as f:
        f.write(content)


def exists(path):
    return _os.path.exists(path)


def is_file(path):
    return _os.path.isfile(path)


def is_dir(path):
    return _os.path.isdir(path)


def list_dir(path="."):
    return _os.listdir(path)


def mkdir(path):
    _os.makedirs(path, exist_ok=True)


def remove(path):
    if _os.path.isdir(path):
        _shutil.rmtree(path)
    else:
        _os.remove(path)


def rename(src, dst):
    _os.rename(src, dst)


def copy(src, dst):
    _shutil.copy2(src, dst)


def size(path):
    return _os.path.getsize(path)


def abspath(path):
    return _os.path.abspath(path)


def basename(path):
    return _os.path.basename(path)


def dirname(path):
    return _os.path.dirname(path)


def join_path(*parts):
    return _os.path.join(*parts)


def cwd():
    return _os.getcwd()


def chdir(path):
    _os.chdir(path)
