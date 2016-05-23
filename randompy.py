#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from io import StringIO
from random import randint
import argparse
import configparser
import json
import os
import requests
import string
import sys


__version__ = '1.0.0'


# Supported methods and related subparsers
METHODS = {
    'integers': 'generateSignedIntegers',
    'decimals': 'generateSignedDecimalFractions',
    'gaussians': 'generateSignedGaussians',
    'strings': 'generateSignedStrings',
    'uuids': 'generateSignedUUIDs',
    'blobs': 'generateSignedBlobs',
    'verify': 'verifySignature',
}


# Request keys
KEYS = {
    'integers': ('min', 'max', 'replacement', 'base'),
    'decimals': ('decimalPlaces', 'replacement'),
    'gaussians': ('mean', 'standardDeviation', 'significantDigits'),
    'strings': ('length', 'characters', 'replacement'),
    'uuids': (),
    'blobs': ('size', 'format'),
    'verify': ('random', 'signature'),
}


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


# Allowed blob format types
BLOB_FORMATS = [
    'base64',
    'hex',
]


def check_constraints(method, req):
    '''Check if all values in req satisfy the method constraints.'''
    funcs = CONSTRAINTS[method]
    params = req['params']
    return all(funcs[p](params[p]) for p in params if p in funcs)


def build_request(key, **kwargs):
    '''Build a request for random.org.

    Arguments:
        key: API key
        kwargs: should contain method and corresponding necessary values
                (see KEYS global var). When method != verify, 'number' should
                also be supplied.
    '''
    rid = randint(0, 99999)
    r = {
        'jsonrpc': 2.0,
        'id': rid,
        'method': METHODS[kwargs['which']],
        'params': {},
    }
    if r['method'] != METHODS['verify']:
        r['params']['apiKey'] = key
        r['params']['n'] = kwargs['number']

    for k in KEYS[kwargs['which']]:
        r['params'][k] = kwargs[k]

    # fix character field in case of strings
    if kwargs['which'] == 'strings':
        s = ''.join(ABCS[c] for c in kwargs['characters'])
        r['params']['characters'] = s

    # check request constraints
    if kwargs['which'] != 'verify':
        valid = check_constraints(kwargs['which'], r)
        if not valid:
            raise Exception('One or more argument constraints violated!')

    return rid, json.dumps(r)


def verify(config, data, sign):
    '''Verify a random.org response given its random field (data) and
    signature.
    '''
    key = config['config']['key']
    url = config['config']['url']
    rid, req = build_request(key, which='verify', random=data, signature=sign)
    h = {'Content-Type': 'application/json'}
    resp = requests.post(url, headers=h, data=req).json()

    def errorfunc(resp):
        return False

    def successfunc(resp):
        return resp['result']['authenticity']

    return handle_response(resp, errorfunc, successfunc)


def handle_error(resp):
    '''Default CLI error output.'''
    error = resp['error']
    msg = StringIO()
    msg.write('Error code: {}\n'.format(error['code']))
    msg.write('Message: {}\n'.format(error['message']))
    if error['data'] is None:
        msg.write('No remaining data.\n')
    else:
        msg.write('Remaining data:\n')
        msg.write('\n'.join(map(str, error['data'])))
    output = msg.getvalue()
    msg.close()
    return output


def handle_result(resp):
    '''Default CLI succesful result output.'''
    data = resp['result']['random']['data']
    msg = StringIO()
    msg.write('\n'.join(map(str, data)))
    output = msg.getvalue()
    msg.close()
    return output


def handle_response(resp, errorfunc, successfunc):
    '''Call error/success function according to response content.'''
    if 'error' in resp:
        output = errorfunc(resp)
    else:
        output = successfunc(resp)
    return output


def handle(config, **kwargs):
    '''Handle CLI request.'''
    if 'key' not in config['config']:
        raise Exception('No API key found in config!')

    key = config['config']['key']
    rid, req = build_request(key, **kwargs)
    url = config['config']['url']
    h = {'Content-Type': 'application/json'}
    resp = requests.post(url, headers=h, data=req).json()

    if not rid == resp['id']:
        raise Exception('Response id did not match request id!')

    data = resp['result']['random']
    sign = resp['result']['signature']
    if not verify(config, data, sign):
        raise Exception('Response could not be verified!')

    output = handle_response(resp, handle_error, handle_result)
    print(output)


def get_config():
    '''Load default + user configurations.'''
    config = configparser.ConfigParser()
    config.read('defaults.ini')
    try:
        config.read(os.path.expanduser(config['config']['path']))
    except:
        raise Exception('No user config found!')
    return config


def main():
    '''Console script entrypoint.'''
    config = get_config()
    parser = argparse.ArgumentParser(description='Get random numbers!')
    subparsers = parser.add_subparsers()

    # Add subparsers for the different methods.
    parser_int = subparsers.add_parser('integers')
    parser_dec = subparsers.add_parser('decimals')
    parser_gau = subparsers.add_parser('gaussians')
    parser_str = subparsers.add_parser('strings')
    parser_uui = subparsers.add_parser('uuids')
    parser_blo = subparsers.add_parser('blobs')

    # Every subparser needs this argument so it's for the parent parser.
    number = int(config['root']['number'])

    parser.add_argument('--version', action='version', version='randompy {}'
                        .format(__version__))
    parser.add_argument('-n', '--number', type=int, default=number,
                        help='number of randoms to generate')

    # Add integer arguments
    integer = config['integer']
    minimum = int(integer['min'])
    maximum = int(integer['max'])
    replacement = config.getboolean('integer', 'replacement')
    base = int(integer['base'])

    parser_int.add_argument('-m', '--min', type=int, default=minimum,
                            help='minimum of random numbers (-1e9-1e9)')
    parser_int.add_argument('-M', '--max', type=int, default=maximum,
                            help='maximum of random numbers (-1e9-1e9)')
    parser_int.add_argument('-r', '--replacement', action='store_false',
                            help='pick without replacement',
                            default=replacement)
    parser_int.add_argument('-b', '--base', type=int, default=base,
                            help='base to display numbers in (2, 8, 10, 12)')
    parser_int.set_defaults(which='integers')

    # Add decimal fraction arguments
    decimal = config['decimal']
    decs = int(decimal['decimalPlaces'])
    replacement = config.getboolean('decimal', 'replacement')

    parser_dec.add_argument('-d', '--decimalPlaces', type=int, default=decs,
                            help='number of decimal places (1-20)',
                            metavar='N')
    parser_dec.add_argument('-r', '--replacement', action='store_false',
                            default=replacement,
                            help='pick without replacement')
    parser_dec.set_defaults(which='decimals')

    # Add gaussian arguments
    gaussian = config['gaussian']
    mean = float(gaussian['mean'])
    stddev = float(gaussian['standardDeviation'])
    significant = int(gaussian['significantDigits'])

    parser_gau.add_argument('-m', '--mean', type=float, default=mean,
                            help='the mean of the distribution (-1e6-1e6)')
    parser_gau.add_argument('-s', '--standardDeviation', type=float,
                            help='the standard deviation of the distribution \
                                  (-1e6-1e6)',
                            default=stddev)
    parser_gau.add_argument('-d', '--significantDigits', type=int, metavar='N',
                            help='significant digits (2-20)',
                            default=significant)
    parser_gau.set_defaults(which='gaussians')

    # Add string arguments
    strings = config['string']
    length = int(strings['length'])
    chars = strings['characters']
    replacement = config.getboolean('string', 'replacement')

    parser_str.add_argument('-l', '--length', type=int, default=length,
                            help='length of strings (1-20)', metavar='N')
    parser_str.add_argument('-c', '--characters', metavar='string', nargs='+',
                            type=str, default=[chars], choices=ABCS.keys(),
                            help='allowed alphabet (max length 80)')
    parser_str.add_argument('-r', '--replacement', action='store_false',
                            default=replacement,
                            help='pick without replacement')
    parser_str.set_defaults(which='strings')

    # Add uuids arguments
    parser_uui.set_defaults(which='uuids')

    # Add blobs arguments
    size = int(config['blob']['size'])
    form = config['blob']['format']

    parser_blo.add_argument('-s', '--size', type=int, default=size,
                            help='size of each blob measured in bits \
                                  (1-1048576, must be divisble by 8)')
    parser_blo.add_argument('-f', '--format', type=str, default=form,
                            choices=BLOB_FORMATS, help='specifies blob return \
                            format')
    parser_blo.set_defaults(which='blobs')

    args = parser.parse_args()

    # If subparser was not supplied, print help; else call main
    if any(k in sys.argv for k in subparsers.choices.keys()):
        handle(config, **vars(args))
        sys.exit()
    else:
        parser.print_help()
        sys.exit(2)
