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

    # Add initial arguments (TODO: expand upon these)
    parser_int.add_argument("-n", "--number", type=int, default=1,
                            help="number of randoms to generate")
    parser_int.add_argument("-m", "--minimum", type=int, required=True,
                            help="minimum of random numbers")
    parser_int.add_argument("-M", "--maximum", type=int, required=True,
                            help="maximum of random numbers")
    parser_int.set_defaults(which="integers")

    parser_dec.add_argument("-n", "--number", type=int, default=1,
                            help="number of randoms to generate")
    parser_dec.add_argument("-d", "--decimals", type=int, default=2,
                            help="number of decimal places")
    parser_dec.set_defaults(which="decimals")

    args = parser.parse_args()

    # If subparser was supplied, call function; else print help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)
    else:
        main(args)
