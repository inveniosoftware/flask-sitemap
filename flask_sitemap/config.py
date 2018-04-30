# -*- coding: utf-8 -*-
#
# This file is part of Flask-Sitemap
# Copyright (C) 2014, 2015 CERN.
#
# Flask-Sitemap is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""The details of the application settings that can be customized.

SITEMAP_URL_SCHEME
------------------

Default: ``http``.

SITEMAP_BLUEPRINT
-----------------

If ``None`` or ``False`` then the Blueprint is not registered.

Default: ``flask_sitemap``.

SITEMAP_GZIP
------------

Default: ``False``.

SITEMAP_BLUEPRINT_URL_PREFIX
----------------------------

Default: ``/``.

SITEMAP_ENDPOINT_URL
--------------------

Return sitemap index or sitemap for pages with less than
``SITEMAP_MAX_URL_COUNT`` urls.

Default: ``/sitemap.xml``.

SITEMAP_ENDPOINT_PAGE_URL
-------------------------

Return GZipped sitemap for given page range of urls.

.. note:: It is strongly recommended to provide caching decorator.

Default: ``/sitemap<int:page>.xml``

SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS
------------------------------------

Default: ``False``.

SITEMAP_IGNORE_ENDPOINTS
------------------------

Default: ``None``.

SITEMAP_VIEW_DECORATORS
-----------------------

Default: ``[]``.

SITEMAP_MAX_URL_COUNT
---------------------

The maximum number of urls per one sitemap file can be up to 50000, however
there is 10MB limitation for the file.

Default: ``10000``.
"""

SITEMAP_BLUEPRINT = 'flask_sitemap'

SITEMAP_BLUEPRINT_URL_PREFIX = '/'

SITEMAP_ENDPOINT_URL = '/sitemap.xml'

SITEMAP_ENDPOINT_PAGE_URL = '/sitemap<int:page>.xml'

SITEMAP_GZIP = False

SITEMAP_URL_SCHEME = 'http'

SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS = False

SITEMAP_IGNORE_ENDPOINTS = None

SITEMAP_VIEW_DECORATORS = []

SITEMAP_MAX_URL_COUNT = 10000
