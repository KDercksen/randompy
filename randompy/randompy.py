#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .api import RandomAPI
from configparser import ConfigParser
from os.path import expanduser
from random import randint
import string


# Supported methods and related subparsers
METHODS = {
    'integers': 'generate{}Integers',
    'decimals': 'generate{}DecimalFractions',
    'gaussians': 'generate{}Gaussians',
    'strings': 'generate{}Strings',
    'uuids': 'generate{}UUIDs',
    'blobs': 'generate{}Blobs',
    'verify': 'verifySignature',
}


# Request keys
KEYS = {
    'integers': (
        ('min', int),
        ('max', int),
        ('replacement', bool),
        ('base', int),
    ),
    'decimals': (
        ('decimalPlaces', int),
        ('replacement', bool),
    ),
    'gaussians': (
        ('mean', float),
        ('standardDeviation', float),
        ('significantDigits', int),
    ),
    'strings': (
        ('length', int),
        ('characters', int),
        ('replacement', bool),
    ),
    'uuids': (
    ),
    'blobs': (
        ('size', int),
        ('format', str),
    ),
    'verify': (
        ('random', lambda x: x),
        ('signature', str),
    ),
}


# Default alphabets
ABCS = {
    'lower': string.ascii_lowercase,
    'upper': string.ascii_uppercase,
    'letters': string.ascii_letters,
    'digits': string.digits,
    'hexdigits': string.hexdigits,
    'octdigits': string.octdigits,
    'punctuation': string.punctuation,
    'printable': string.printable,
    'whitespace': string.whitespace
}


class RandomPy:

    def __init__(self, signed=True):
        self.config = self._get_config()
        self.key = self.config['config']['key']
        self.signed = signed
        self.fmt = 'Signed' if signed else ''

        url = self.config['config']['url']
        self.api = RandomAPI(url)

    def integers(self, n, **kwargs):
        method = 'integers'
        return self.generate(number=n, method=method, **kwargs)

    def decimals(self, n, **kwargs):
        method = 'decimals'
        return self.generate(number=n, method=method, **kwargs)

    def gaussians(self, n, **kwargs):
        method = 'gaussians'
        return self.generate(number=n, method=method, **kwargs)

    def strings(self, n, **kwargs):
        method = 'strings'
        return self.generate(number=n, method=method, **kwargs)

    def uuids(self, n, **kwargs):
        method = 'uuids'
        return self.generate(number=n, method=method, **kwargs)

    def blobs(self, n, **kwargs):
        method = 'blobs'
        return self.generate(number=n, method=method, **kwargs)

    def generate(self, **kwargs):
        method = kwargs['method']
        keys = (x[0] for x in KEYS[method])
        conf = self.config[method]
        kwargs.update({k: kwargs.get(k, conf[k]) for k in keys})
        rID, req = self._build_request(**kwargs)
        resp = self.api.call(req)

        if not rID == resp['id']:
            raise Exception('Response ID did not match request ID!')

        if self.signed and not self._verify_response(resp):
            raise Exception('Response could not be verified!')

        if 'errorfunc' in kwargs:
            errorfunc = kwargs['errorfunc']
        else:
            def errorfunc(resp):
                return resp['error']

        if 'successfunc' in kwargs:
            successfunc = kwargs['successfunc']
        else:
            def successfunc(resp):
                return resp['result']

        return self._handle_response(resp, errorfunc, successfunc)

    def _get_config(self):
        config = ConfigParser()
        config.read('defaults.ini')
        try:
            config.read(expanduser(config['config']['path']))
        except:
            raise Exception('No user config found!')
        return config

    def _build_request(self, **kwargs):
        rID = randint(0, 999999)
        method = kwargs['method']
        methodfmt = METHODS[method].format(self.fmt)
        req = {
            'jsonrpc': 2.0,
            'id': rID,
            'method': methodfmt,
            'params': {},
        }

        if kwargs['method'] != 'verify':
            req['params']['apiKey'] = self.key
            req['params']['n'] = kwargs['number']
        if method == 'strings':
            s = ''.join(ABCS[c] for c in kwargs['characters'])
            req['params']['characters'] = s
        for k, ktype in KEYS[method]:
            req['params'][k] = ktype(kwargs[k])

        return rID, req

    def _verify_response(self, resp):
        kwargs = {
            'method': 'verify',
            'random': resp['result']['random'],
            'signature': resp['result']['signature'],
        }
        rID, req = self._build_request(**kwargs)
        ver_resp = self.api.call(req)

        def errorfunc(resp):
            return False

        def successfunc(resp):
            return ver_resp['result']['authenticity']

        return self._handle_response(ver_resp, errorfunc, successfunc)

    def _handle_response(self, resp, errorfunc, successfunc):
        return errorfunc(resp) if 'error' in resp else successfunc(resp)
