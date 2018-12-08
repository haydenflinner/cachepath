#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cachepath` package."""

import pytest


import cachepath
from cachepath import CachePath
from pathlib import Path


@pytest.fixture
def mod(tmpdir):
    cachepath.location = tmpdir
    return cachepath
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_works(mod):
    p = mod.CachePath('lolfile')
    p.open('w').writelines('hi')
    assert 'hi' == p.read_text()

def test_unique(mod):
    p = mod.CachePath()
    p.clear()
    assert p.read_text() == ''

def test_clear(mod):
    p = mod.CachePath('lolfolder', dir=True)
    # We would get surprising behavior if / created CachePaths given the side
    # effecting constructor, so don't do that!
    (p/'file').touch()
    p.clear()
    assert len(list(p.iterdir())) == 0
    assert not (p/'file').exists()

def test_can_change_location(tmpdir):
    # Old test, now the rest of the tests depend on this to work, but can't hurt.
    cachepath.location = tmpdir
    assert CachePath('dummy').parent == Path(tmpdir)
