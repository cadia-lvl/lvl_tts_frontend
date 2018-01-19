# -*- coding: utf-8 -*-

from nose.tools import *

def setup():
    print("SETUP!")

def teardown():
    print("TEAR DOWN!")

def test_basic():
    print("basic test passed")