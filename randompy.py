#!/usr/bin/env python3
# Module to interface with the random.org JSON-RPC interface.

import argparse
import json
import urllib.request as ureq
import sys


# API key to use in the requests (replace with your own)
API = "0af6cd33-6cc0-4939-9792-3e2d1f990e51"

# API invocation URL
URL = "https://api.random.org/json-rpc/1/invoke"

# Supported methods and related subparsers
METHODS = {
    "integers": "generateIntegers",
    "decimals": "generateDecimalFractions"
    "gaussians": "generateGaussians",
    "strings": "generateStrings"
    }


def build_request(args):
    """Build a request dictionary that can immediately be dumped to JSON.

    Arguments:
    ----------
    args: namespace object
        The commandline arguments as parsed by the ArgumentParser from the
        argparse module.
    """
    data = {
        "jsonrpc": "2.0",
        "method": METHODS[args.which],
        "id": 1337,
        "params": {
            "apiKey": API,
            "n": args.number
            }
        }
    if args.which == "integers":
        data["params"]["min"] = args.minimum
        data["params"]["max"] = args.maximum
    elif args.which == "decimals":
        data["params"]["decimalPlaces"] = args.decimals
    return data


def query(data):
    """Send a JSON request to the random.org API and return a dict-ified
    response.

    Arguments:
    ----------
    data: dictionary
        Dictionary containing all necessary info. Will be dumped to JSON
        format directly.
    """
    request = ureq.Request(URL)
    request.add_header("Content-Type", "application/json")
    response = ureq.urlopen(request, json.dumps(data).encode("ascii"))
    return json.loads(response.read().decode("utf-8"))


def main(args):
    """Build a JSON request and send it to random.org. The response is parsed
    and the data printed to stdout, separated by newline characters for easy
    piping.

    Arguments:
    ----------
    args: namespace object
        The commandline arguments as parsed by the ArgumentParser from the
        argparse module.
    """
    data = query(build_request(args))
    result = list(data["result"]["random"]["data"])
    print("\n".join(map(str, result)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get random numbers!")
    subparsers = parser.add_subparsers()

    # Add subparsers for the different methods.
    parser_int = subparsers.add_parser("integers")
    parser_dec = subparsers.add_parser("decimals")
    parser_gau = subparsers.add_parser("gaussians")
    parser_str = subparsers.add_parser("strings")

    # Every subparser needs this argument so it's for the parent parser.
    parser.add_argument("-n", "--number", type=int, choices=range(1, 1001),
                        default=1, help="number of randoms to generate")

    # Add integer arguments
    parser_int.add_argument("-m", "--minimum", type=int, required=True,
                            choices=range(-1000000000, 1000000000),
                            help="minimum of random numbers")
    parser_int.add_argument("-M", "--maximum", type=int, required=True,
                            choices=range(-1000000000, 1000000000),
                            help="maximum of random numbers")
    parser_int.add_argument("-r", "--replacement", action="store_false",
                            default=True, help="pick without replacement")
    parser_int.add_argument("-b", "--base", type=int, default=10,
                            help="base to display numbers in")
    parser_int.set_defaults(which="integers")

    # Add decimal fraction arguments
    parser_dec.add_argument("-d", "--decimals", type=int, default=2,
                            choices=range(1, 21),
                            help="number of decimal places")
    parser_dec.add_argument("-r", "--replacement", action="store_false",
                            default=True, help="pick without replacement")
    parser_dec.set_defaults(which="decimals")

    # Add gaussian arguments
    parser_gau.add_argument("-m", "--mean", type=float, required=True,
                            help="the mean of the distribution")
    parser_gau.add_argument("-s", "--stddev", type=float, required=True,
                            help="the standard deviation of the distribution")
    parser_gau.add_argument("-d", "--significant", type=int, required=True,
                            choices=range(2, 21), help="significant digits")
    parser_gau.set_defaults(which="gaussians")

    # Add string arguments
    parser_str.add_argument("-l", "--length", type=int, choices=range(1, 21),
                            required=True, help="length of strings")
    parser_str.add_argument("-c", "--characters", required=True, type=str,
                            help="allowed alphabet (max length 80)")
    parser_str.add_argument("-r", "--replacement", action="store_false",
                            default=True, help="pick without replacement")
    parser_str.set_defaults(which="strings")

    args = parser.parse_args()

    # If subparser was not supplied, print help; else call main
    if any(k in sys.argv for k in METHODS.keys()):
        main(args)
    else:
        parser.print_help()
        sys.exit(2)
