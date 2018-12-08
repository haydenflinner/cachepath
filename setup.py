#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

import sys
requirements = ["pathlib2"] if sys.version_info[0] == 2 else []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Hayden Flinner",
    author_email='hayden@flinner.me',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Pythonic parameterized cache paths.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_type='txt/x-rst',
    include_package_data=True,
    keywords=['cachepath', 'paths', 'pathlib', 'cache', 'temp'],
    name='cachepath',
    packages=find_packages(include=['cachepath']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/haydenflinner/cachepath',
    version='1.1.0',
    zip_safe=True,
)
