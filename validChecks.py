# Filename: validChecks.py

import os
import sys
import errno
import tempfile

#checking for valids paths
ERROR_INVALID_NAME = 123 #Windows-specific error code indicating an invalid pathname
def is_pathname_valid(pathname: str) -> bool:
    try:
        if not isinstance(pathname, str) or not pathname:
            return False
        _, pathname = os.path.splitdrive(pathname)
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError as exc:
        return False
    else:
        return True

def is_path_sibling_creatable(pathname: str) -> bool:
    dirname = os.path.dirname(pathname) or os.getcwd()
    try:
        with tempfile.TemporaryFile(dir=dirname): pass
        return True
    except EnvironmentError:
        return False

def is_path_exists_or_creatable_portable(pathname: str) -> bool:
    try:
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_sibling_creatable(pathname))
    except OSError:
        return False