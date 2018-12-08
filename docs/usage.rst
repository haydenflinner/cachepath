=====
Usage
=====

To use CachePath in a project::

    from cachepath import CachePath, Path

Changing Storage Location
-------------------------
::

    import cachepath
    cachepath.location = './cache'  # Once, anywhere. Default is tempfile.gettempdir()

    # The order that you import / assign to .location doesn't matter yet
    from cachepath import CachePath, Path

Indepth Example
----------------
Lets hack together a cache for a website scraper. This could be
useful if you were working on your parsing logic or want
the files used in the process to to be available on disk for later debugging
instead of just staying in memory until a crash.

If this seems like a lot, try reading :doc:`Getting Started <readme>` first.

::

    from cachepath import CachePath, Path
    from itertools import takewhile

    def get_scraped_ebay_stats(user, product_id):
        # '/tmp/ebay/user/product_id.html'
        return dumb_parser(CachePath('ebay', user, product_id, suffix='html'))

    def clear_cache(user=None, product_id=None):
        args = takewhile(lambda x: x != None, ('ebay', user, product_id))
        return CachePath(*args).clear()

    def get_tempfile():
        return CachePath()


    # Without cachepath
    try:
       from pathlib import Path
    except:  # py2
       from pathlib2 import Path

    # If we don't put everything under a folder, we'll try to rm -rf /tmp/ later..
    import tempfile
    ebay = Path(tempfile.gettempdir())/'ebay'

    import shutil  # Needed to remove a folder recursively

    def get_scraped_ebay_stats(user, product_id):
        p = Path(ebay, user, product_id).with_suffix('html')
        p.parent.mkdir(exist_ok=True, parents=True) # Does this update timestamp
        # and thus break Make-like tools? Turns out no (on Linux at least),
        # but who would have known?
        dumb_parser(p)

    def clear_cache(user=None, product_id=None):
        if product_id:
            # if product_id ever starts pointing to a folder, this will break
            return (ebay/user/product_id).unlink()
        p = ebay/user if user else ebay
        # Not exactly equivalent: cachepath.clear() just removes the contents of
        # a folder, it doesn't remove and recreate. Helpful to avoid messing up
        # permissions or requiring a personal folder to place things.
        shutil.rmtree(p)  # No rm  -rf for folder paths in pathlib

    def get_tempfile():
        return tempfile.mkstemp()

    def dumb_parser(html_path):
        if not p.exists():
            sh('wget {}'.format(p))
        return myprocess(p.read_text())
