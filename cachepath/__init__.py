# -*- coding: utf-8 -*-

"""Top-level package for CachePath."""

__author__ = """Hayden Flinner"""
__email__ = 'hayden@flinner.me'
__version__ = '0.1.0'

try:
    from pathlib import Path, WindowsPath, PosixPath, _windows_flavour, _posix_flavour
except:  # py2
    from pathlib2 import Path, WindowsPath, PosixPath, _windows_flavour, _posix_flavour

import os
import shutil

sep = _windows_flavour.sep if os.name == 'nt' else _posix_flavour.sep

import tempfile
location = tempfile.gettempdir()

def clear_contents(path):
    """Clear the cached file/folder, leaving it empty (dir) or 0 length (file).
    If path doesn't exist, make it a directory.
    """
    if not path.exists():
        path.mkdir()
        return

    if path.is_dir():
        for sub in path.iterdir():
            if sub.is_dir():
                shutil.rmtree(sub)
            else:
                sub.unlink()
    else:
        with path.open('w'):
            pass


class CachePath(Path):
    #_flavour = _windows_flavour if os.name == 'nt' else _posix_flavour
    def __new__(cls, *args, folder=False, mode=0o666):
        """Construct a CachePath from one or several strings/Paths.

        >>> CachePath() == '/tmp/xyz123randomfile'
        True

        >>> CachePath('myfilename') = '/tmp/myfilename/'
        True

        >>> p = CachePath('date/processed_data', folder=True)
        >>> # or
        >>> p = CachePath('date', 'processed_data', folder=True)
        >>> (p/'tool1results').touch()
        >>> (p/'tool2results').clear()  # touch + remove contents
        >>> list(p.iterdir())
        [['tool1results', 'tool2results']
        """
        if not args:
            args = [tempfile.mktemp(dir=location)]
        if cls is CachePath:
            cls = WindowsPath if os.name == 'nt' else PosixPath
        returning = cls._from_parts([location, *args])
        cls.clear = clear_contents

        # Create all of the folders leading to the path, if they don't exist
        dirp = returning.parent if not folder else returning
        dirp.mkdir(exist_ok=True, parents=True)

        if not folder:
            returning.touch(mode=mode)
        return returning

#def WindowsCachePath
    def clear(self):
        """Clears contents of the cache if it's a folder, otherwise clears file."""
        clear_contents(self)

    def remove(self):
        """rm -r str(self)"""
        if self.is_dir:
            shutil.rmtree(str(self))
        else:
            self.unlink()


#class CachePath(Path):
    #def __init__(self):
'''
class CachePath(Path):
    """Base class for manipulating paths without I/O.
    Path represents a filesystem path and offers operations which
    don't imply any actual filesystem I/O.  Depending on your system,
    instantiating a Path will return either a PosixPath or a
    WindowsPath object.  You can also instantiate either of these classes
    directly, regardless of your system.
    """
    __slots__ = (
        '_drv', '_root', '_parts',
        '_str', '_hash', '_pparts', '_cached_cparts',
    )

    def __new__(cls, *args):
        """Construct a Path from one or several strings and or existing
        Path objects.  The strings and path objects are combined so as
        to yield a canonicalized path, which is incorporated into the
        new Path object.
        """
        print('__new__', cls, args)
        if cls is CachePath:
            cls = WindowsPath if os.name == 'nt' else PosixPath
        return cls._from_parts(args)

'''
