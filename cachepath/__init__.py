# -*- coding: utf-8 -*-

"""
Package that provides CachePath, as well as exporting a Python2/3 compatible Path.
"""

__author__ = """Hayden Flinner"""
__email__ = 'hayden@flinner.me'
__version__ = '1.1.1'

try:
    from pathlib import Path, WindowsPath, PosixPath
except ImportError:  # py2
    from pathlib2 import Path, WindowsPath, PosixPath

import os
import shutil
import tempfile
__all__ = [
    'CachePath',
    'TempPath',
    'Path',  # Helpful re-export for those who want Py2 compatibility
    'clear',
    'rm',
]

location = tempfile.gettempdir()


def clear(path):
    """Clear the file/dir, leaving it empty (dir) or 0 length (file).

    Monkey-patched onto all Paths on import.
    Creates file if path doesn't exist."""
    if len(list(path.parents)) == 0 and '/' in str(path):
        # We let through the case of .location == '.', because if you
        # really insist on doing that, more power to ya.
        raise ValueError("Shouldn't be able to happen, stop clownin")
    if path.is_dir():
        for sub in path.iterdir():
            if sub.is_dir():
                shutil.rmtree(sub)
            else:
                sub.unlink()
    else:
        with path.open('w'):
            pass


def rm(path):
    """Delete the file/dir, even if it's a dir with files in it.

    Monkey-patched onto all Paths on import.
    Does nothing if path doesn't exist."""
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(str(path))
    else:
        path.unlink()


Path.rm = rm
Path.clear = clear


class CachePath(Path):
    """Construct a CachePath from one or several strings/Paths.

    Constructing a CachePath automatically creates the preceding folders necessary
    for the file to exist, if they're not already there.

    CachePaths also have a few helper methods:

        :func:`CachePath().clear() <cachepath.clear>`

        :func:`CachePath().rm() <cachepath.rm>`

        By accident, these methods are also attached to regular Paths after
        constructing a CachePath, but it's not recommended to depend on this
        behavior.

    Examples
    --------
    Basic Usage::

        CachePath() == '/tmp/xyz123randomfile'
        CachePath('myfilename') == '/tmp/myfilename'
        CachePath('myfolder', dir=True) == '/tmp/myfolder/'
        TempPath('myfolder') == '/tmp/myfolder/zsdskjrandom'

    Multi-component Paths::

        p = CachePath('date/processed_data', dir=True)
        # Or, Alternate constructor to avoid {}/{}.format()
        p = CachePath('date', 'processed_data', dir=True)

    For an example of real usage, here's a quick cache for an arbitrary
    function/arg combo ::

        def get_scraped_ebay_stats(product_id):
            p = CachePath('ebay_results/{}'.format(product_id))
            if not p.exists():
               sh('wget {}'.format(p))
            return parser.parse(p.read_text())

    Parameters
    ----------
    args : [str], optional
        List of strings to join for Path. If None, ``getempfile`` is used.

    dir : bool, optional
        Is the path intended to be a directory? Useful when you just need a
        tempdir for lots of files, and you don't want to make a CachePath
        out of each. ::

            d = CachePath(date, dir=True)
            (d/'tool1results').touch()
            (d/'tool2results').touch()
            list(d.iterdir()) == ['tool1results', 'tool2results']

    suffix : str, optional
        Appended to the last path in \\*args, i.e.
        CachePath('a', 'b', suffix='_long_suff.txt') == '/tmp/a/b_long_suff.txt'

    mode : int, optional, default=0o777
        Mode to create folder with, if it doesn't already exist.
    """

    def __new__(cls, *args, **kwargs):
        dir = kwargs.pop('dir', False)  # Py2 concessions :'(
        suffix = kwargs.pop('suffix', '')

        if cls is CachePath:  # Copy-pasted from pathlib.py
            cls = WindowsPath if os.name == 'nt' else PosixPath

        # CachePath() == TempPath() == Path(tempfile.mkstemp(location)[1])
        if not args:
            fd, loc = tempfile.mkstemp(dir=str(location), suffix=suffix)
            os.close(fd)
            args = [loc]
        else:
            # Attach the suffix
            args = list(args)
            args[-1] = str(args[-1]) + suffix

        # Construct the Path. Prepend the /tmp location
        real_args = [str(location)]
        real_args.extend(args)
        returning = cls._from_parts(real_args)

        # Create all of the dirs leading to the path, if they don't exist.
        # If the path is supposed to be a directory, make that too.
        dirp = returning if dir else returning.parent
        mkdir_kwargs = {'mode': kwargs['mode']} if 'mode' in kwargs else {}
        dirp.mkdir(exist_ok=True, parents=True, **mkdir_kwargs)

        return returning


def TempPath(cls, *args, **kwargs):
    """
    See CachePath for more details::

        TempPath('x', 'y', suffix='.z')
        # Is safer, easier, and explains your intent to always have a new file better than
        CachePath('x', 'y', 'randomstringhere', suffix='.z')

        # However,
        TempPath() == CachePath()  # for convenience

    .. TODO Remove on __exit__?
    """
    suffix = kwargs.pop('suffix', '')
    real_args = list(args)
    real_args.append(tempfile.mktemp(dir=str(location), suffix=suffix))
    return CachePath(*args, **kwargs)
