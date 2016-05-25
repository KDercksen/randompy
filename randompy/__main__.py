#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import __version__
from .randompy import RandomPy
from io import StringIO
import argparse
import sys


def cli_error(resp):
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


def cli_success(resp):
    data = resp['result']['random']['data']
    msg = StringIO()
    msg.write('\n'.join(map(str, data)))
    output = msg.getvalue()
    msg.close()
    return output


def cli_usage(resp):
    data = resp['result']
    msg = StringIO()
    msg.write('Status: {}\n'.format(data['status']))
    msg.write('Requests left: {}\n'.format(data['requestsLeft']))
    msg.write('Bits left: {}'.format(data['bitsLeft']))
    output = msg.getvalue()
    msg.close()
    return output


def main():
    '''Console script entrypoint.'''
    parser = argparse.ArgumentParser(description='Get random numbers!')
    subparsers = parser.add_subparsers()

    # Add subparsers for the different methods.
    parser_int = subparsers.add_parser('integers')
    parser_dec = subparsers.add_parser('decimals')
    parser_gau = subparsers.add_parser('gaussians')
    parser_str = subparsers.add_parser('strings')
    parser_uui = subparsers.add_parser('uuids')
    parser_blo = subparsers.add_parser('blobs')
    parser_use = subparsers.add_parser('usage')

    parser.add_argument('--version', action='version', version='randompy {}'
                        .format(__version__))
    parser.add_argument('-S', '--signed', action='store_true', default=False,
                        help='use signed API')
    parser.add_argument('-n', '--number', help='number of randoms to generate',
                        type=int, default=1)

    # Add integer arguments
    parser_int.add_argument('-m', '--min', type=int, action='store',
                            help='minimum of random numbers (-1e9-1e9)')
    parser_int.add_argument('-M', '--max', type=int,
                            help='maximum of random numbers (-1e9-1e9)')
    parser_int.add_argument('-r', '--replacement', action='store_false',
                            help='pick without replacement')
    parser_int.add_argument('-b', '--base', type=int,
                            help='base to display numbers in (2, 8, 10, 12)')
    parser_int.set_defaults(method='integers')

    # Add decimal fraction arguments
    parser_dec.add_argument('-d', '--decimalPlaces', type=int, metavar='N',
                            help='number of decimal places (1-20)')
    parser_dec.add_argument('-r', '--replacement', action='store_false',
                            help='pick without replacement')
    parser_dec.set_defaults(method='decimals')

    # Add gaussian arguments
    parser_gau.add_argument('-m', '--mean', type=float,
                            help='the mean of the distribution (-1e6-1e6)')
    parser_gau.add_argument('-s', '--standardDeviation', type=float,
                            help='the standard deviation of the distribution \
                                  (-1e6-1e6)')
    parser_gau.add_argument('-d', '--significantDigits', type=int, metavar='N',
                            help='significant digits (2-20)')
    parser_gau.set_defaults(method='gaussians')

    # Add string arguments
    parser_str.add_argument('-l', '--length', type=int, metavar='N',
                            help='length of strings (1-20)')
    parser_str.add_argument('-c', '--characters', metavar='string', nargs='+',
                            help='allowed alphabet (max length 80)',
                            type=str)
    parser_str.add_argument('-r', '--replacement', action='store_false',
                            help='pick without replacement')
    parser_str.set_defaults(method='strings')

    # Add uuids arguments
    parser_uui.set_defaults(method='uuids')

    # Add blobs arguments
    parser_blo.add_argument('-s', '--size', type=int, help='size of each blob \
                            measured in bits (1-1048576, \
                            must be divisble by 8)')
    parser_blo.add_argument('-f', '--format', type=str, help='specifies blob \
                            return format')
    parser_blo.set_defaults(method='blobs')

    # Add usage arguments
    parser_use.set_defaults(method='usage')

    args = parser.parse_args()

    # If subparser was not supplied, print help; else call main
    if any(k in sys.argv for k in subparsers.choices.keys()):
        r = RandomPy(signed=args.signed)
        kwargs = {k: v for k, v in vars(args).items() if v is not None}
        if kwargs['method'] == 'usage':
            successfunc = cli_usage
        else:
            successfunc = cli_success

        o = r.generate(errorfunc=cli_error, successfunc=successfunc, **kwargs)
        print(o)
        sys.exit()
    else:
        parser.print_help()
        sys.exit(2)

if __name__ == "__main__":
    main()
