RandomPy
========

RandomPy is an interface to the `random.org` JSON API. It offers a CLI and a
Python object that you can use to query the API.

![build status](https://travis-ci.org/KDercksen/randompy.svg)

- [Usage](#usage)
- [Configuration file](#configuration file)
- [Available CLI options](#available-cli-options)
- [TODO](#todo)

### Usage

The [API key](https://api.random.org/api-keys/beta) should be placed in
`~/.randompy.ini`.

These API keys have a limited use per day, and every user/application should
have its own key according to the random.org
[API usage guidelines](https://api.random.org/guidelines).

Example `.randompy.ini`:

```INI
[config]
key = abcdef01-2345-6789-abcd-ef0123456789
```

Only the `key` value is required; all optional configuration values can be
found below.

Now simply run `python setup.py install` and you're set. Some CLI examples:

    $ randompy -n 5 integers

    47
    97
    56
    63
    45

    $ randompy strings

    kneknvhy

    $ randompy blobs -s 64 -f hex

    a2dcd5575d838933

And some use in Python code:

```python
from randompy import RandomPy

# Use the signed API with response verification
randSigned = RandomPy()

# The below function returns the whole result JSON object by default.
# You can specify keyword args `errorfunc` and `successfunc` with functions
# that should handle the response as you want.
result = randSigned.integers(10)

# Use non-signed API
rand = RandomPy(signed=False)

def successfunc(resp):
    return resp['random']['data']

# Use default error handling (return error JSON object) and custom successfunc
some_strings = rand.strings(20, successfunc=successfunc)
```

For further details, see the documentation.

#### Configuration file

Default values for all available arguments can be specified in
`~/.randompy.ini`. See `defaults.ini` as an example:

```INI
[config]
path = ~/.randompy.ini
url = https://api.random.org/json-rpc/1/invoke

[root]
number = 1

[integers]
min = 0
max = 100
replacement = yes
base = 10

[decimals]
decimalPlaces = 2
replacement = yes

[gaussians]
mean = 20.0
standardDeviation = 2.0
significantDigits = 2

[strings]
length = 8
characters = lower
replacement = yes

[uuids]

[blobs]
size = 128
format = base64
```

You should not override the `url` and `path` values. All other values can be
overridden in the userconfig.

#### Available CLI options

- `-h, --help`: display help string.
- `--version`: display installation version.
- `-n, --number N`: number of random objects to generate. This should be
                    specified before any subparser. The maximum allowed numbers
                    for `uuids` and `blobs` are 1e3 and 1e2 respectively; for
                    the rest of the types, 1e4 numbers can be generated in a
                    single request. 
- `-S, --signed`: use the signed API (verify response signatures).
- `integers`
    - `-m, --min N`: minimum integer (between -1e9 and 1e9).
    - `-M, --max N`: maximum integer (between -1e9 and 1e9).
    - `-r, --replacement`: if specified, pick random integers without
                           replacement.
    - `-b, --base N`: base of random integers (2, 8, 10 or 12).
- `decimals`
    - `-d, --decimalPlaces N`: number of decimal places (between 1 and 20).
    - `-r, --replacement`: if specified, pick random decimal numbers without
                           replacement.
- `gaussians`
    - `-m, --mean N`: mean of Gaussian distribution (between -1e6 and 1e6).
    - `-s, --standardDeviation N`: standard deviation of Gaussian distribution
                                 (between -1e6 and 1e6).
    - `-d, --significantDigits N`: number of significant digits (between 2 and
                                 20).
- `strings`
    - `-l, --length N`: length of random strings (between 1 and 20).
    - `-c, --characters N [N [..]]`: character set(s) allowed in random strings
                                     (choices are `lower, upper, letters,
                                     digits, hexdigits, octdigits, punctuation,
                                     printable, whitespace`, resulting
                                     character set may not be longer than 80
                                     characters).
    - `-r, --replacement`: if specified, pick random strings without
                           replacement.
- `uuids` (no extra arguments)
- `blobs`
    - `-s, --size N`: size of blobs in bits (between 1 and 1048576, must be
                    divisible by 8).
    - `-f, --format N`: blob output format (`base64` or `hex`).

### TODO

- Write module documentation
- Implement requests for more than the max number allowed per API call
- Write more (more robust) tests
