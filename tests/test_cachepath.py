#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cachepath` package."""

import pytest


from cachepath import cachepath


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    cachepath/'xyz'.open('w').writelines('hi')
    assert 'hi' in cachepath/'xyz'.read_text()
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
