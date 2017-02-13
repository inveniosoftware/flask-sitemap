# -*- coding: utf-8 -*-
#
# This file is part of Flask-Sitemap
# Copyright (C) 2015 CERN.
# Copyright (C) 2018 ETH Zurich, Swiss Data Science Center, Jiri Kuncar.
#
# Flask-Sitemap is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Simple command line interface for sitemap generation.

.. deprecated:: 0.3.0
   Use :func:`flask_sitemap.cli:sitemap` instead.
"""

import os
import codecs
import warnings

from flask import current_app, url_for

try:
    from flask_script import Command, Option
except ImportError:  # pragma: no cover
    warnings.warn("Flask-Script package is not installed. "
                  "Please run `pip install flask_sitemap[cli]`.")
    raise

from flask_sitemap import sitemap_page_needed


class Sitemap(Command):
    """Generate static sitemap."""

    option_list = (
        Option('--output-directory', '-o', dest='directory', default='.'),
    )

    def run(self, directory):
        """Generate static sitemap to given directory."""
        sitemap = current_app.extensions['sitemap']

        @sitemap_page_needed.connect
        def generate_page(app, page=1, urlset=None):
            filename = url_for('flask_sitemap.page', page=page).split('/')[-1]
            with codecs.open(os.path.join(directory, filename), 'w',
                             'utf-8') as f:
                f.write(sitemap.render_page(urlset=urlset))

        filename = url_for('flask_sitemap.sitemap').split('/')[-1]
        with codecs.open(os.path.join(directory, filename), 'w', 'utf-8') as f:
            f.write(sitemap.sitemap())
