# -*- coding: utf-8 -*-
#
# This file is part of Flask-Sitemap
# Copyright (C) 2014 CERN.
#
# Flask-Sitemap is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""The details of the application settings that can be customized.


SITEMAP_URL_METHOD
------------------

Default: ``http``.

SITEMAP_BLUEPRINT
-----------------

If ``None`` or ``False`` then the Blueprint is not registered.

Default: ``flask_sitemap``.

SITEMAP_BLUEPRINT_URL_PREFIX
----------------------------

Default: ``/``.

SITEMAP_ENDPOINT_URL
--------------------

Default: ``/sitemap.xml``.

SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS
------------------------------------

Default: ``False``.

SITEMAP_IGNORE_ENDPOINTS
------------------------

Default: ``None``.

SITEMAP_VIEW_DECORAROS
----------------------

Default: ``[]``.
"""

SITEMAP_BLUEPRINT = 'flask_sitemap'

SITEMAP_BLUEPRINT_URL_PREFIX = '/'

SITEMAP_ENDPOINT_URL = 'sitemap.xml'

SITEMAP_URL_SCHEME = 'http'

SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS = False

SITEMAP_IGNORE_ENDPOINTS = None

SITEMAP_VIEW_DECORATORS = []
