.. highlight:: shell

============
Contributing
============

Have an idea to contribute, or hungry to fix bugs? https://github.com/haydenflinner/cachepath/issues.


Setting Up for Development
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: shell

Here's how to set up `cachepath` for local development.

1. Fork the `cachepath` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/cachepath.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv cachepath
    $ cd cachepath/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ py.test
    $ tox

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Tips
~~~~

To run a subset of tests::

$ py.test tests.test_cachepath


Deploying
~~~~~~~~~

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bumpversion patch # possible: major / minor / patch
$ git push
$ git push --tags

Travis will then deploy to PyPI if tests pass.
