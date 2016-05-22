RandomPy
========
*RandomPy* is a commandline interface to the random.org JSON Signed API.  The
signature of every request is verified to make sure it comes from `random.org`.
It is designed for use as a small utility and its output can easily piped into
other applications or files.


### Examples
First you should get yourself an API key and put it in `~/.randompy.ini`.

Example config file (yeah... that easy):

    [config]
    key = abcdef01-2345-6789-abcd-ef0123456789


These API keys have a limited use per day, and every user/application should
have its own key according to the random.org
[API usage guidelines](https://api.random.org/guidelines).

You can get your own key [here!](https://api.random.org/api-keys/beta)

### Todo
- Rewrite examples/arguments in README
- Explain config file usage in README
- Implement full API
