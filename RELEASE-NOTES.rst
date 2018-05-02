======================
 Flask-Sitemap v0.3.0
======================

Flask-Sitemap v0.3.0 was released on May 2, 2018.

About
-----

Flask-Sitemap is a Flask extension helping with sitemap generation.

New features
------------

- Adds integration with Click library for Flask 0.11+.

Improved features
-----------------

- Improves exclusion of specific URLs without parameters
  from to the sitemap.  (closes #24) (closes #25) (closes #26)

Bug fixes
---------

- Reuses exiting request context if it exits. (closes #35)
- Prepends '/' to endpoint urls for compatibility with Flask 1.0.
- Improves documentation about ``SITEMAP_URL_SCHEME``.
- Fixes typo in ``SITEMAP_VIEW_DECORATORS``.

Notes
-----

- Removes support for Python 2.6 and 3.3.

Installation
------------

   $ pip install Flask-Sitemap==0.3.0

Documentation
-------------

   https://flask-sitemap.readthedocs.io/en/v0.3.0

Homepage
--------

   https://github.com/inveniosoftware/flask-sitemap

Good luck and thanks for choosing Flask-Sitemap.

| Invenio Development Team
|   Email: info@inveniosoftware.org
|   IRC: #invenio on irc.freenode.net
|   Twitter: http://twitter.com/inveniosoftware
|   GitHub: http://github.com/inveniosoftware
|   URL: http://inveniosoftware.org
