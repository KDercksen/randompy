RandomPy
========
*RandomPy* is a commandline interface to the random.org JSON-RPC API.
It is designed for use as a small utility and its output can easily piped into
other applications or files.

The most useful thing to do is to put the script in your path and use it
that way.

####Dependencies
* Python 3.x (tested on 3.4)
* no other third parties modules, just standard library stuff

###Examples
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

The file contains an API key, but you should replace it with your own; these
keys have a limited use per day, and every user/application should have its
own key according to the random.org [API usage guidelines](https://api.random.org/guidelines).

You can get your own key [here](https://api.random.org/api-keys/beta)!

###Todo
I aim to implement full use of the API. Currently generation of integers,
decimal fractions, gaussians and strings is supported.
The rest will come! 
