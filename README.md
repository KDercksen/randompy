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
59
```

Generate 10 random decimals with 8 decimal places:
```
$ python randompy.py decimals -n 10 -d 8
0.65466723
0.28385892
0.02867834
0.26050413
0.80495891
0.95120194
0.0423827
0.05744396
0.42540818
0.94061231
```

The file contains an API key, but you should replace it with your own; these
keys have a limited use per day, and every user/application should have its
own key according to the random.org [API usage guidelines](https://api.random.org/guidelines).

You can get your own key [here](https://api.random.org/api-keys/beta)!

###Todo
I aim to implement full use of the API (so support for strings, blobs, signed
stuff etc. is coming).
