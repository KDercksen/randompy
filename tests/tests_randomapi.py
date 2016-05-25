#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import assert_raises
from randompy import RandomAPI
from unittest.mock import patch


class TestRequestValidCheck:

    def setup(self):
        self.randomapi = RandomAPI('url')

    def teardown(self):
        self.randomapi = None

    def test_valid_integers_correct(self):
        req = {'method': 'generateIntegers',
               'params': {'n': 100, 'min': 0, 'max': 100, 'base': 10}}
        assert self.randomapi.valid(req)[1]

    def test_valid_integers_incorrect(self):
        req = {'method': 'generateIntegers',
               'params': {'n': 100, 'min': 0, 'max': 100, 'base': 7}}
        assert not self.randomapi.valid(req)[1]

    def test_valid_decimals_correct(self):
        req = {'method': 'generateDecimalFractions',
               'params': {'n': 100, 'decimalPlaces': 5}}
        assert self.randomapi.valid(req)[1]

    def test_valid_decimals_incorrect(self):
        req = {'method': 'generateDecimalFractions',
               'params': {'n': 100, 'decimalPlaces': 21}}
        assert not self.randomapi.valid(req)[1]

    def test_valid_gaussian_correct(self):
        req = {'method': 'generateGaussians',
               'params': {'n': 100, 'mean': 20, 'standardDeviation': 0,
                          'significantDigits': 5}}
        assert self.randomapi.valid(req)[1]

    def test_valid_gaussian_incorrect(self):
        req = {'method': 'generateGaussians',
               'params': {'n': 100, 'mean': 1e7, 'standardDeviation': 0,
                          'significantDigits': 5}}
        assert not self.randomapi.valid(req)[1]

    def test_valid_strings_correct(self):
        req = {'method': 'generateStrings',
               'params': {'n': 100, 'length': 10,
                          'characters': 'abcd987123jkh'}}
        assert self.randomapi.valid(req)[1]

    def test_valid_strings_incorrect(self):
        req = {'method': 'generateStrings',
               'params': {'n': 100, 'length': 25,
                          'characters': 'abcd987123jkh'}}
        assert not self.randomapi.valid(req)[1]

    def test_valid_uuids_correct(self):
        req = {'method': 'generateUUIDs', 'params': {'n': 10}}
        assert self.randomapi.valid(req)[1]

    def test_valid_uuids_incorrect(self):
        req = {'method': 'generateUUIDs', 'params': {'n': 1e4}}
        assert not self.randomapi.valid(req)[1]

    def test_valid_blobs_correct(self):
        req = {'method': 'generateBlobs',
               'params': {'n': 40, 'size': 1024, 'format': 'hex'}}
        assert self.randomapi.valid(req)[1]

    def test_valid_blobs_incorrect(self):
        req = {'method': 'generateBlobs',
               'params': {'n': 40, 'size': 68, 'format': 'hex'}}
        assert not self.randomapi.valid(req)[1]


class TestCall:

    def setup(self):
        self.randomapi = RandomAPI('url')

    def teardown(self):
        self.randomapi = None

    def test_exception(self):
        req = {'method': 'generateIntegers', 'params': {'n': -1}}
        assert_raises(Exception, RandomAPI.call, req)

    @patch.object(RandomAPI, '_post', return_value=True)
    def test_correct(self, mock_post):
        req = {'method': 'generateIntegers', 'params': {'n': 1}}
        assert self.randomapi.call(req)
