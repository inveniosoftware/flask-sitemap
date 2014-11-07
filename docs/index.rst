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
--------

.. contents::
   :local:
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
^^^^^^^^^^^^

Flask-Sitemap has the following dependencies:

* `Flask <https://pypi.python.org/pypi/Flask>`_
* `blinker <https://pypi.python.org/pypi/blinker>`_
* `six <https://pypi.python.org/pypi/six>`_

Flask-Sitemap requires Python version 2.6, 2.7 or 3.3+


Quickstart
==========

This part of the documentation will show you how to get started in using
Flask-Sitemap with Flask.

This guide assumes you have successfully installed Flask-Sitemap and a working
understanding of Flask. If not, follow the installation steps and read about
Flask at http://flask.pocoo.org/docs/.


A Minimal Example
^^^^^^^^^^^^^^^^^

A minimal Flask-Sitemap usage example looks like this.

First, let's create the application and initialise the extension:

.. code-block:: python

    from flask import Flask, session, redirect
    from flask_sitemap import Sitemap
    app = Flask("myapp")
    ext = Sitemap(app=app)


Configuration
=============

.. automodule:: flask_sitemap.config


API
===

This documentation section is automatically generated from Flask-Sitemap's
source code.

Flask-Sitemap
^^^^^^^^^^^^^

.. automodule:: flask_sitemap

.. autoclass:: Sitemap
   :members:


.. include:: ../CHANGES

.. include:: ../CONTRIBUTING.rst


License
=======

.. include:: ../LICENSE

.. include:: ../AUTHORS
