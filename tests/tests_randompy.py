#!/usr/bin/env python
# -*- coding: utf-8 -*-

from randompy import RandomAPI, RandomPy
from unittest.mock import MagicMock, patch


class TestUsage:

    def setup(self):
        self.r = RandomPy(key='key', signed=False)
        self.f = lambda x: x
        self.patcher = patch.object(RandomAPI, '_post', side_effect=self.f)
        self.patcher.start()

    def teardown(self):
        self.r = None
        self.patcher.stop()

    def test_usage(self):
        req = self.r.usage(errorfunc=self.f, successfunc=self.f)
        assert (
            req['method'] == 'getUsage' and
            req['params']['apiKey'] == 'key'
        )


class TestGenerateUnsigned:

    def setup(self):
        self.r = RandomPy(key='key', signed=False)
        self.f = lambda x: x
        self.patcher = patch.object(RandomAPI, '_post', side_effect=self.f)
        self.patcher.start()

    def teardown(self):
        self.r = None
        self.patcher.stop()

    def test_integers(self):
        req = self.r.integers(1, min=3, max=6, replacement=True, base=2,
                              errorfunc=self.f, successfunc=self.f)
        assert (
            req['method'] == 'generateIntegers' and
            req['params']['apiKey'] == 'key' and
            req['params']['n'] == 1 and
            req['params']['min'] == 3 and
            req['params']['max'] == 6 and
            req['params']['replacement'] is True and
            req['params']['base'] == 2
        )

    def test_decimals(self):
        req = self.r.decimals(1, decimalPlaces=5, replacement=True,
                              errorfunc=self.f, successfunc=self.f)
        assert (
            req['method'] == 'generateDecimalFractions' and
            req['params']['apiKey'] == 'key' and
            req['params']['n'] == 1 and
            req['params']['decimalPlaces'] == 5 and
            req['params']['replacement'] is True
        )

    def test_gaussians(self):
        req = self.r.gaussians(1, mean=5, standardDeviation=2,
                               significantDigits=5, errorfunc=self.f,
                               successfunc=self.f)
        assert (
            req['method'] == 'generateGaussians' and
            req['params']['apiKey'] == 'key' and
            req['params']['n'] == 1 and
            req['params']['mean'] == 5 and
            req['params']['standardDeviation'] == 2 and
            req['params']['significantDigits'] == 5
        )

    def test_strings(self):
        req = self.r.strings(1, length=5, characters='lower',
                             errorfunc=self.f, successfunc=self.f)
        assert (
            req['method'] == 'generateStrings' and
            req['params']['apiKey'] == 'key' and
            req['params']['n'] == 1 and
            req['params']['length'] == 5 and
            req['params']['characters'] == 'abcdefghijklmnopqrstuvwxyz'
        )

    def test_uuids(self):
        req = self.r.uuids(1, errorfunc=self.f, successfunc=self.f)
        assert (
            req['method'] == 'generateUUIDs' and
            req['params']['apiKey'] == 'key' and
            req['params']['n'] == 1
        )

    def test_blobs(self):
        req = self.r.blobs(1, size=1024, format='hex', errorfunc=self.f,
                           successfunc=self.f)
        assert (
            req['method'] == 'generateBlobs' and
            req['params']['apiKey'] == 'key' and
            req['params']['n'] == 1 and
            req['params']['size'] == 1024 and
            req['params']['format'] == 'hex'
        )


class TestGenerateSigned:

    def setup(self):
        self.r = RandomPy(key='key')
        self.r._verify_response = MagicMock(return_value=True)
        self.f = lambda x: x
        self.patcher = patch.object(RandomAPI, '_post', side_effect=self.f)
        self.patcher.start()

    def teardown(self):
        self.r = None
        self.patcher.stop()

    def test_integers(self):
        req = self.r.integers(1, min=3, max=6, replacement=True, base=2,
                              errorfunc=self.f, successfunc=self.f)
        assert (
            req['method'] == 'generateSignedIntegers' and
            req['params']['apiKey'] == 'key' and
            req['params']['n'] == 1 and
            req['params']['min'] == 3 and
            req['params']['max'] == 6 and
            req['params']['replacement'] is True and
            req['params']['base'] == 2
        )

    def test_decimals(self):
        req = self.r.decimals(1, decimalPlaces=5, replacement=True,
                              errorfunc=self.f, successfunc=self.f)
        assert (
            req['method'] == 'generateSignedDecimalFractions' and
            req['params']['apiKey'] == 'key' and
            req['params']['n'] == 1 and
            req['params']['decimalPlaces'] == 5 and
            req['params']['replacement'] is True
        )

    def test_gaussians(self):
        req = self.r.gaussians(1, mean=5, standardDeviation=2,
                               significantDigits=5, errorfunc=self.f,
                               successfunc=self.f)
        assert (
            req['method'] == 'generateSignedGaussians' and
            req['params']['apiKey'] == 'key' and
            req['params']['n'] == 1 and
            req['params']['mean'] == 5 and
            req['params']['standardDeviation'] == 2 and
            req['params']['significantDigits'] == 5
        )

    def test_strings(self):
        req = self.r.strings(1, length=5, characters='lower',
                             errorfunc=self.f, successfunc=self.f)
        assert (
            req['method'] == 'generateSignedStrings' and
            req['params']['apiKey'] == 'key' and
            req['params']['n'] == 1 and
            req['params']['length'] == 5 and
            req['params']['characters'] == 'abcdefghijklmnopqrstuvwxyz'
        )

    def test_uuids(self):
        req = self.r.uuids(1, errorfunc=self.f, successfunc=self.f)
        assert (
            req['method'] == 'generateSignedUUIDs' and
            req['params']['apiKey'] == 'key' and
            req['params']['n'] == 1
        )

    def test_blobs(self):
        req = self.r.blobs(1, size=1024, format='hex', errorfunc=self.f,
                           successfunc=self.f)
        assert (
            req['method'] == 'generateSignedBlobs' and
            req['params']['apiKey'] == 'key' and
            req['params']['n'] == 1 and
            req['params']['size'] == 1024 and
            req['params']['format'] == 'hex'
        )


class TestHandleResponse:

    def setup(self):
        self.r = RandomPy(key='key')
        self.success = lambda x: 'success'
        self.error = lambda x: 'error'

    def teardown(self):
        self.r = None

    def test_handle_error(self):
        resp = {'error': 42}
        o = self.r._handle_response(resp, self.error, self.success)
        assert o == 'error'

    def test_handle_success(self):
        resp = {'result': 42}
        o = self.r._handle_response(resp, self.error, self.success)
        assert o == 'success'
