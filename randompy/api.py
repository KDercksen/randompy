#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import post


# Value constraints
CONSTRAINTS = {
    'integers': {
        'n': lambda x: x >= 1 and x <= 1e4,
        'min': lambda x: x >= -1e9 and x <= 1e9,
        'max': lambda x: x >= -1e9 and x <= 1e9,
        'base': lambda x: x in [2, 8, 10, 12],
    },
    'decimals': {
        'n': lambda x: x >= 1 and x <= 1e4,
        'decimalPlaces': lambda x: x >= 1 and x <= 20,
    },
    'gaussians': {
        'n': lambda x: x >= 1 and x <= 1e4,
        'mean': lambda x: x >= -1e6 and x <= 1e6,
        'standardDeviation': lambda x: x >= -1e6 and x <= 1e6,
        'significantDigits': lambda x: x >= 2 and x <= 20,
    },
    'strings': {
        'n': lambda x: x >= 1 and x <= 1e4,
        'length': lambda x: x >= 1 and x <= 20,
        'characters': lambda x: len(x) >= 1 and len(x) <= 80,
    },
    'uuids': {
        'n': lambda x: x >= 1 and x <= 1e3,
    },
    'blobs': {
        'n': lambda x: x >= 1 and x <= 100,
        'size': lambda x: x >= 1 and x <= 1048576 and x % 8 == 0,
        'format': lambda x: x in BLOB_FORMATS,
    },
    'verify': {
    },
}


ALIAS = {
    'generateIntegers': 'integers',
    'generateSignedIntegers': 'integers',
    'generateDecimalFractions': 'decimals',
    'generateSignedDecimalFractions': 'decimals',
    'generateGaussians': 'gaussians',
    'generateSignedGaussians': 'gaussians',
    'generateStrings': 'strings',
    'generateSignedStrings': 'strings',
    'generateUUIDs': 'uuids',
    'generateSignedUUIDs': 'uuids',
    'generateBlobs': 'blobs',
    'generateSignedBlobs': 'blobs',
    'verifySignature': 'verify',
}


BLOB_FORMATS = [
    'base64',
    'hex',
]


class RandomAPI:

    def __init__(self, url):
        self.url = url
        self.headers = {'Content-Type': 'application/json'}

    def call(self, req):
        v = self.valid(req)
        if not v[1]:
            raise Exception('Argument constraints violated: {}'.format(
                            ', '.join(k for k in v[0] if v[0][k] is False)))
        else:
            return post(self.url, json=req, headers=self.headers).json()

    def valid(self, req):
        alias = ALIAS[req['method']]
        funcs = CONSTRAINTS[alias]
        params = req['params']
        results = {k: funcs[k](params[k]) for k in params if k in funcs}
        return results, all(results.values())
