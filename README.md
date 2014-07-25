
Pyclassif
=====

Pyclassif is web-server based on Django, which allows users to create, train and use their own classifiers (mostly for images recognition).

At this stage it is rather a toy than something serious, but it is just the beginning.

Data are stored in MongoDB, so corresponding packages are required.

The repository includes files for integration with uWSGI and nginx.
To run uWSGI:
```
uwsgi --socket mysite.sock --module pyclassif.wsgi --chmod-socket=666
```

Version:
-------
0.1

Requirements:
-------------
* Python 2.7
* Django
* numpy, scipy
* MongoDB server
* mongoengine
* cairosvg

