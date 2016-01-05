===============
 Flask-Sitemap
===============
.. currentmodule:: flask_sitemap


.. raw:: html

    <p style="height:22px; margin:0 0 0 2em; float:right">
        <a href="https://travis-ci.org/inveniosoftware/flask-sitemap">
            <img src="https://travis-ci.org/inveniosoftware/flask-sitemap.png?branch=master"
                 alt="travis-ci badge"/>
        </a>
        <a href="https://coveralls.io/r/inveniosoftware/flask-sitemap">
            <img src="https://coveralls.io/repos/inveniosoftware/flask-sitemap/badge.png?branch=master"
                 alt="coveralls.io badge"/>
        </a>
    </p>


Flask-Sitemap is a Flask extension helping with sitemap generation.

Contents
========

.. contents::
   :local:
   :depth: 1
   :backlinks: none


Installation
============

Flask-Sitemap is on PyPI so all you need is :

.. code-block:: console

    $ pip install flask-sitemap

The development version can be downloaded from `its page at GitHub
<http://github.com/inveniosoftware/flask-sitemap>`_.

.. code-block:: console

    $ git clone https://github.com/inveniosoftware/flask-sitemap.git
    $ cd flask-sitemap
    $ python setup.py develop
    $ ./run-tests.sh

Requirements
------------

Flask-Sitemap has the following dependencies:

* `Flask <https://pypi.python.org/pypi/Flask>`_
* `blinker <https://pypi.python.org/pypi/blinker>`_
* `six <https://pypi.python.org/pypi/six>`_

Flask-Sitemap requires Python version 2.6, 2.7 or 3.3+


Usage
=====

This part of the documentation will show you how to get started in using
Flask-Sitemap with Flask.

This guide assumes you have successfully installed Flask-Sitemap and a working
understanding of Flask. If not, follow the installation steps and read about
Flask at http://flask.pocoo.org/docs/.

Simple Example
--------------

First, let's create the application and initialise the extension:

.. code-block:: python

    from flask import Flask, session, redirect
    from flask_sitemap import Sitemap
    app = Flask("myapp")
    ext = Sitemap(app=app)

    @app.route('/')
    def index():
        pass

    @ext.register_generator
    def index():
        # Not needed if you set SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS=True
        yield 'index', {}

    if __name__ == '__main__':
        app.run(debug=True)

If you save the above as ``app.py``, you can run the example
application using your Python interpreter:

.. code-block:: console

    $ python app.py
     * Running on http://127.0.0.1:5000/

and you can observe generated sitemap on the example pages:

.. code-block:: console

    $ firefox http://127.0.0.1:5000/
    $ firefox http://127.0.0.1:5000/sitemap.xml

You should now be able to emulate this example in your own Flask
applications.  For more information, please read the :ref:`indexpage`
guide, the :ref:`caching` guide, and peruse the :ref:`api`.


.. _indexpage:

Index Page
----------

By default, a sitemap contains set of urls up to
``SITEMAP_MAX_URL_COUNT``. When the limit is reached a sitemap index file
with list of sitemaps is served instead. In order to ease :ref:`caching`
of sitemaps a signal ``sitemap_page_needed`` is fired with current
application object, page number and url generator.


.. _caching:

Caching
-------

Large sites should implement caching or their sitemaps. The following
example shows an basic in-memory cache that can be replaced by
*Flask-Cache*.

.. code-block:: python

        from functools import wraps
        from flask_sitemap import Sitemap, sitemap_page_needed

        cache = {}  # replace by *Flask-Cache* instance or similar

        @sitemap_page_needed.connect
        def create_page(app, page, urlset):
            cache[page] = sitemap.render_page(urlset=urlset)

        def load_page(fn):
            @wraps(fn)
            def loader(*args, **kwargs):
                page = kwargs.get('page')
                data = cache.get(page)
                return data if data else fn(*args, **kwargs)
            return loader

        self.app.config['SITEMAP_MAX_URL_COUNT'] = 10
        self.app.config['SITEMAP_VIEW_DECORATORS'] = [load_page]

        sitemap = Sitemap(app=self.app)


Configuration
=============

.. automodule:: flask_sitemap.config


.. _api:

API
===

This documentation section is automatically generated from Flask-Sitemap's
source code.

Flask-Sitemap
-------------

.. automodule:: flask_sitemap

.. autoclass:: Sitemap
   :members:


.. include:: ../CHANGES

.. include:: ../CONTRIBUTING.rst


License
=======

.. include:: ../LICENSE

.. include:: ../AUTHORS
