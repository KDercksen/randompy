#!/usr/bin/env python

import randompy


def test_check_constraints_integers_correct():
    method = 'integers'
    # correct
    req = {'params': {'n': 100, 'min': 0, 'max': 100, 'base': 10}}
    assert randompy.check_constraints(method, req)


def test_check_constraints_integers_incorrect():
    method = 'integers'
    # correct
    req = {'params': {'n': 100000, 'min': 0, 'max': 100, 'base': 10}}
    assert not randompy.check_constraints(method, req)


def test_check_constraints_decimals_correct():
    method = 'decimals'
    req = {'params': {'n': 100, 'decimalsPlaces': 5}}
    assert randompy.check_constraints(method, req)


def test_check_constraints_decimals_incorrect():
    method = 'decimals'
    req = {'params': {'n': 100, 'decimalsPlaces': 21}}
    assert randompy.check_constraints(method, req)


def test_check_constraints_gaussian_correct():
    method = 'gaussians'
    req = {'params': {'n': 100, 'mean': 20, 'standardDeviation': 0,
                      'significantDigits': 5}}
    assert randompy.check_constraints(method, req)


def test_check_constraints_gaussian_incorrect():
    method = 'gaussians'
    req = {'params': {'n': 100, 'mean': 1e7, 'standardDeviation': 0,
                      'significantDigits': 5}}
    assert not randompy.check_constraints(method, req)


def test_check_constraints_strings_correct():
    method = 'strings'
    req = {'params': {'n': 100, 'length': 10, 'characters': 'abcd987123jkh'}}
    assert randompy.check_constraints(method, req)


def test_check_constraints_strings_incorrect():
    method = 'strings'
    req = {'params': {'n': 100, 'length': 10, 'characters': ''}}
    assert not randompy.check_constraints(method, req)


def test_check_constraints_uuids_correct():
    method = 'uuids'
    req = {'params': {'n': 10}}
    assert randompy.check_constraints(method, req)


def test_check_constraints_uuids_incorrect():
    method = 'uuids'
    req = {'params': {'n': 10000}}
    assert not randompy.check_constraints(method, req)


def test_check_constraints_blobs_correct():
    method = 'blobs'
    req = {'params': {'n': 40, 'size': 1024, 'format': 'hex'}}
    assert randompy.check_constraints(method, req)


def test_check_constraints_blobs_incorrect():
    method = 'blobs'
    req = {'params': {'n': 40, 'size': 68, 'format': 'hex'}}
    assert not randompy.check_constraints(method, req)
