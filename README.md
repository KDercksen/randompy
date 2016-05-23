RandomPy
========

*RandomPy* is a commandline interface to the random.org JSON Signed API.  The
signature of every request is verified to make sure it comes from `random.org`.
It is designed for use as a small utility and its output can easily piped into
other applications or files.

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

Now simply run `python setup.py install` and you're set. Some examples:

    $ randompy.py -n 5 integers

    47
    97
    56
    63
    45

    $ randompy.py strings

    kneknvhy

    $ randompy.py blobs -s 64 -f hex

    a2dcd5575d838933

#### Available options

- `-n, --number N`: number of random objects to generate. This should be
                    specified before any subparser. The maximum allowed numbers
                    for `uuids` and `blobs` are 1e3 and 1e2 respectively; for
                    the rest of the types, 1e4 numbers can be generated in a
                    single request. 
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

#### Configuration file

Default values for all available arguments can be specified in
`~/.randompy.ini`. See `default.ini` as an example:

```INI
[config]
path = ~/.randompy.ini
url = https://api.random.org/json-rpc/1/invoke

[root]
number = 1

[integer]
min = 0
max = 100
replacement = yes
base = 10

[decimal]
decimalPlaces = 2
replacement = yes

[gaussian]
mean = 20.0
standardDeviation = 2.0
significantDigits = 2

[string]
length = 8
characters = lower
replacement = yes

[blob]
size = 128
format = base64
```

You should not override the `url` and `path` values. All other values can be
overridden in the userconfig.

### TODO

- Implement StdLib `random` port for use as library
