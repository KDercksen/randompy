#!/usr/bin/env python3

from io import StringIO
from random import randint
import argparse
import configparser
import json
import os
import requests
import string
import sys


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


KEYS = {
    'integers': ('min', 'max', 'replacement', 'base'),
    'decimals': ('decimalPlaces', 'replacement'),
    'gaussians': ('mean', 'standardDeviation', 'significantDigits'),
    'strings': ('length', 'characters', 'replacement'),
    'uuids': (),
    'blobs': ('size', 'format'),
    'verify': ('random', 'signature'),
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

BLOB_FORMATS = [
    'base64',
    'hex',
]


def build_request(key, **kwargs):
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

    return rid, json.dumps(r)


def verify(config, data, sign):
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
    data = resp['result']['random']['data']
    msg = StringIO()
    msg.write('\n'.join(map(str, data)))
    output = msg.getvalue()
    msg.close()
    return output


def handle_response(resp, errorfunc, successfunc):
    if 'error' in resp:
        output = errorfunc(resp)
    else:
        output = successfunc(resp)
    return output


def handle(config, **kwargs):
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


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('defaults.ini')
    try:
        config.read(os.path.expanduser(config['config']['path']))
    except:
        raise Exception('No user config found!')

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

    parser.add_argument('-n', '--number', type=int, default=number,
                        help='number of randoms to generate (range 1:1000)')

    # Add integer arguments
    integer = config['integer']
    minimum = int(integer['min'])
    maximum = int(integer['max'])
    replacement = config.getboolean('integer', 'replacement')
    base = int(integer['base'])

    parser_int.add_argument('-m', '--min', type=int, default=minimum,
                            help='minimum of random numbers (range -1e9:1e9)')
    parser_int.add_argument('-M', '--max', type=int, default=maximum,
                            help='maximum of random numbers (range -1e9:1e9)')
    parser_int.add_argument('-r', '--replacement', action='store_false',
                            default=replacement,
                            help='pick without replacement')
    parser_int.add_argument('-b', '--base', type=int, choices=[2, 8, 10, 16],
                            default=base, help='base to display numbers in')
    parser_int.set_defaults(which='integers')

    # Add decimal fraction arguments
    decimal = config['decimal']
    decs = int(decimal['decimalPlaces'])
    replacement = config.getboolean('decimal', 'replacement')

    parser_dec.add_argument('-d', '--decimalPlaces', type=int, default=decs,
                            choices=range(1, 21), metavar='N',
                            help='number of decimal places')
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
                            help='the mean of the distribution')
    parser_gau.add_argument('-s', '--standardDeviation', type=float,
                            help='the standard deviation of the distribution',
                            default=stddev)
    parser_gau.add_argument('-d', '--significantDigits', type=int, metavar='N',
                            default=significant, choices=range(2, 21),
                            help='significant digits',)
    parser_gau.set_defaults(which='gaussians')

    # Add string arguments
    strings = config['string']
    length = int(strings['length'])
    chars = strings['characters']
    replacement = config.getboolean('string', 'replacement')

    parser_str.add_argument('-l', '--length', type=int, choices=range(1, 21),
                            default=length, help='length of strings',
                            metavar='N')
    parser_str.add_argument('-c', '--characters', metavar='string', nargs='+',
                            choices=ABCS.keys(), type=str, default=[chars],
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
                                  (range 1:1048576, must be divisble by 8)')
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
