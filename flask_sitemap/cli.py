# -*- coding: utf-8 -*-
#
# This file is part of Flask-Sitemap
# Copyright (C) 2018 ETH Zurich, Swiss Data Science Center, Jiri Kuncar.
#
# Flask-Sitemap is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Simple command line interface for sitemap generation.

.. versionadded:: 0.3.0
   Integration with Flask 0.11+ using Click library.
"""

from __future__ import absolute_import

import os
import codecs
import warnings

import click
from flask import current_app, url_for
try:
    from flask.cli import with_appcontext
except ImportError:  # pragma: no cover
    from flask_cli import with_appcontext

from flask_sitemap import sitemap_page_needed


@click.command()
@click.option(
    '--output-directory', '-o', default='.',
    help='Output directory for sitemap files.'
)
@click.option('--verbose', '-v', is_flag=True)
@with_appcontext
def sitemap(output_directory, verbose):
    """Generate static sitemap to given directory."""
    sitemap = current_app.extensions['sitemap']

    @sitemap_page_needed.connect
    def generate_page(app, page=1, urlset=None):
        filename = url_for('flask_sitemap.page', page=page).split('/')[-1]
        with codecs.open(os.path.join(output_directory, filename), 'w',
                         'utf-8') as f:
            f.write(sitemap.render_page(urlset=urlset))
            if verbose:
                click.echo(filename)

    filename = url_for('flask_sitemap.sitemap').split('/')[-1]
    with codecs.open(os.path.join(output_directory, filename), 'w',
                     'utf-8') as f:
        f.write(sitemap.sitemap())
        if verbose:
            click.echo(filename)
