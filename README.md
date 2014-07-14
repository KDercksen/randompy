RandomPy
========
*RandomPy* is a commandline interface to the random.org JSON-RPC API.
It is designed for use as a small utility and its output can easily piped into
other applications or files.

The most useful thing to do is to put the script in your path and use it that way.

####Dependencies
* Python 3.x (tested on 3.4)
* no other third parties modules, just standard library stuff

###Examples
First you should get yourself an API key and put it in ```~/.randompy``` (on
the first line without extra text). You can alter the config file path inside
*randompy.py*.

Example config file (yeah... that easy):
	XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX

These API keys have a limited use per day, and every user/application should have its
own key according to the random.org [API usage guidelines](https://api.random.org/guidelines).

You can get your own key [here!](https://api.random.org/api-keys/beta)

Note, if you don't want to save your api key on your disk you can also supply
it by command line argument via the ```--api-key``` or ```-a``` option.

Generate a random integer between 0 and 100:
```
$ python randompy.py integers -m 0 -M 100
```

Generate 10 random decimals with 8 decimal places:
```
$ python randompy.py -n 10 decimals -d 8
```

Generate 5 random strings consisting of lowercase ascii characters and digits:
```
$ python randompy.py -n 10 strings -c lower digits
```

Generate 100 numbers from a Gaussian distribution with mean 14 and standard-
deviation 0.5 and 15 significant digits:
```
$ python randompy.py -n 100 gaussians -m 14 -s 0.5 -d 15
```

Get help on the integer subparser:
```
$ python randompy.py integers -h
```

###Todo
- Implement full api
- Command line option for specifying config path
- Installation via distutils
