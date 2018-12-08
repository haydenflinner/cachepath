=========
CachePath
=========


.. image:: https://img.shields.io/pypi/v/cachepath.svg
        :target: https://pypi.python.org/pypi/cachepath

.. image:: https://img.shields.io/travis/haydenflinner/cachepath.svg
        :target: https://travis-ci.org/haydenflinner/cachepath

.. image:: https://readthedocs.org/projects/cachepath/badge/?version=latest
        :target: https://cachepath.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




A small package for pythonic parameterized cache paths.


* Free software: MIT license
* Documentation: https://cachepath.readthedocs.io.


.. _getting-started:

Getting Started
----------------
**Install:**
    ``pip install cachepath``
**Import:**
    ``from cachepath import CachePath, Path``

**Why?**
    1. Integrates ``pathlib`` with ``tempfile`` and ``shutil``
    2. Wraps ``pathlib`` import for Py2/3 compat. (not in ``six``)

**Why? But longer:**
Just need a temp path to pass to some random tool for its logfile?
Behold, a gaping hole in ``pathlib``::

    def easy_get_tempfile():
        return CachePath()  # Path('/tmp/213kjdsrandom')
    def hard_get_tempfile():
        return Path(tempfile.mkstemp()) # I forgot to call Path the first time

Now, I'm running this tool multiple times, how do I attach some info to the
filename?  ::

    def easy_get_tempfile(param):
        return CachePath(param, suffix='.txt')  # Path('/tmp/param.txt')
    def hard_get_tempfile(param):
        return (Path(tempfile.gettempdir())/param).with_suffix('txt')

Ew. Now, I'm running this tool *a lot*, maybe even over a tree of data that looks
like this! ::

    2018-12-23
        person1
        person2
    2018-12-24
        person1
    2018-12-25
        person1

I want my logs to be structured the same way.  How hard can it be? ::

    2018-12-23/
        person1_output.txt
        person2_output.txt
    2018-12-24/
        person1_output.txt
    2018-12-25/
        person1_output.txt

Let's find out::

    def easy_get_path(date, person):
        return CachePath(date, person, suffix='_output.txt')
    def hard_get_path(date, person):
        personfilename = '{}_output.txt'.format(person)
        returning = Path(tempfile.gettempdir())/date/personfilename
        return returning

Actually, we made a mistake. These aren't equivalent. We may find out when we
pass our path to another tool that it refuses to create the ``date`` folder
if it doesn't already exist. This issue can show itself as a Permission Denied
error on Unix systems rather than the "File/Folder not found" you might think
you would get. Regardless, we figured it out, let's try again::

    def hard_get_path():
        personfilename = '{}_output.txt'.format(person)
        returning = Path(tempfile.gettempdir())/date/personfilename
        # Does this mkdir update the modified timestamp of the folders we're in?
        # Might matter if we're part of a larger toolset...
        returning.parent.mkdir(exist_ok=True, parents=True)
        return returning

Now, how do we clear out some day's results so that we can be sure we're looking
at fresh output of the tool? ::

  def easy_clear_date(date):
      CachePath(date).clear()  # rm -r /tmp/date/*
  def hard_clear_date(date):
      # We happen to know that date is a folder and not a file (at least in our
      # current design), so we know we need some form of .remove rather than
      # .unlink(). Unfortunately, pathlib doesn't offer one for folders with
      # files still in them. If you google how to do it, you will find plenty of
      # answers, one of which is a pure pathlib recursive solution! But we're lazy:
      p = Path(tempfile.gettempdir(), date)
      import shutil
      if p.exists():
          shutil.rmtree(p)
      p.mkdir(exist_ok=True, parents=True)
      # This still isn't exactly equivalent, because we've lost whatever
      # permissions were set on the date folder, or if it were actually a symlink
      # to somewhere else, that's gone now.

And all of this is ignoring the hacky imports you have to do to get ``pathlib``
in Py3 and ``pathlib2`` in Py2::

    from cachepath import Path  # py2/3
    # or
    try:
        from pathlib import Path
    except:
        from pathlib2 import Path


Convinced yet? ``pip install cachepath`` or copy `the source`_ into your local
``utils.py`` (you know you have one.)

`API doc is here`_.


Shameless Promo
----------------
Find yourself working with paths a lot in cmd-line tools? You might like
`invoke`_ and/or `magicinvoke`_!

.. [*] The source for CachePath can be downloaded from the `Github repo`_.

.. _Github repo: https://github.com/haydenflinner/cachepath
.. [*] This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _`the source`: https://github.com/haydenflinner/cachepath/blob/master/cachepath/__init__.py
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`invoke`: https://www.pyinvoke.org
.. _`magicinvoke`: https://magicinvoke.readthedocs.io/en/latest/
.. _`API doc is here`: https://cachepath.readthedocs.io/en/latest/
