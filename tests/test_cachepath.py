#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cachepath` package."""

import pytest


from cachepath import CachePath, Path


@pytest.fixture
def cachepath(tmpdir):
    import cachepath
    cachepath.location = tmpdir
    return cachepath
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_works(cachepath):
    p = cachepath.CachePath('lolfile')
    p.open('w').writelines([u'hi'])
    assert 'hi' == p.read_text()

def test_rm_clear_file(cachepath):
    p = cachepath.CachePath()
    p.write_text(u'lol')
    p.clear()
    assert p.read_text() == ''
    p.rm()
    assert not p.exists()

def test_clear_folder(cachepath):
    p = cachepath.CachePath('lolfolder', dir=True)
    # We would get surprising behavior if / created CachePaths given the side
    # effecting constructor, so don't do that!
    (p/'file').touch()
    p.clear()
    assert len(list(p.iterdir())) == 0
    assert not (p/'file').exists()
    p.rm()
    assert not p.exists()

def test_tmp(cachepath, tmpdir):
    p = cachepath.TempPath('folder/path/here')
    p.touch()
    assert str(tmpdir) in str(p.parent)

def test_can_change_location():
    # Old test, now the rest of the tests depend on this to work, but can't hurt.
    import cachepath
    cachepath.location = './dummy'
    assert cachepath.CachePath('innerfile') == Path('./dummy/innerfile')

@pytest.mark.xfail
def test_tmp_removes_self(cachepath, tmpdir):
    # TODO
    p = cachepath.TempPath('hi', delete=True)
    with p:
        pass
    assert not p.exists()  # Might throw?
