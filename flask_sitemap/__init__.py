# -*- coding: utf-8 -*-
#
# This file is part of Flask-Sitemap
# Copyright (C) 2014, 2015, 2016, 2017 CERN.
# Copyright (C) 2018 ETH Zurich, Swiss Data Science Center, Jiri Kuncar.
#
# Flask-Sitemap is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Flask extension for generating page ``/sitemap.xml``.

Initialization of the extension:

>>> from flask import Flask
>>> from flask_sitemap import Sitemap
>>> app = Flask('myapp')
>>> ext = Sitemap(app=app)

or alternatively using the factory pattern:

>>> app = Flask('myapp')
>>> ext = Sitemap()
>>> ext.init_app(app)
"""

from __future__ import absolute_import

import gzip
import sys

from collections import Mapping
from flask import current_app, request, Blueprint, render_template, url_for, \
    Response, make_response, has_request_context
from flask.signals import Namespace
from functools import wraps
from itertools import islice
from werkzeug.utils import import_string


from . import config
from .version import __version__

# PY2/3 compatibility
if sys.version_info[0] == 3:  # pragma: no cover
    import io
    BytesIO = io.BytesIO
    string_types = str,
    from itertools import zip_longest
else:
    from cStringIO import StringIO as BytesIO
    string_types = basestring,
    from itertools import izip_longest as zip_longest


# Signals
_signals = Namespace()

#: Sent when a sitemap index is generated and given page will need to be
#: generated in the future from already calculated url set.
sitemap_page_needed = _signals.signal('sitemap-page-needed')


class Sitemap(object):
    """Flask extension implementation."""

    def __init__(self, app=None, command_name='sitemap'):
        """Initialize login callback."""
        self.decorators = []
        self.url_generators = [self._routes_without_params]
        self.command_name = command_name

        if app is not None:
            self.init_app(app)

    def init_app(self, app, command_name=None):
        """Initialize a Flask application.

        :param app: Application to register.
        :param command_name: Register a Click command with this name, or
                             skip if ``False``.

        .. versionadded:: 0.3.0
           The *command_name* parameter.
        """
        self.app = app
        # Follow the Flask guidelines on usage of app.extensions
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        if 'sitemap' in app.extensions:
            raise RuntimeError("Flask application already initialized")
        app.extensions['sitemap'] = self

        # Set default configuration
        for k in dir(config):
            if k.startswith('SITEMAP_'):
                self.app.config.setdefault(k, getattr(config, k))

        # Set decorators from configuration
        for decorator in app.config.get('SITEMAP_VIEW_DECORATORS'):
            if isinstance(decorator, string_types):
                decorator = import_string(decorator)
            self.decorators.append(decorator)

        # Create and register Blueprint
        if app.config.get('SITEMAP_BLUEPRINT'):
            # Add custom `template_folder`
            self.blueprint = Blueprint(app.config.get('SITEMAP_BLUEPRINT'),
                                       __name__, template_folder='templates')

            self.blueprint.add_url_rule(
                app.config.get('SITEMAP_ENDPOINT_URL'),
                'sitemap',
                self._decorate(self.sitemap)
            )
            self.blueprint.add_url_rule(
                app.config.get('SITEMAP_ENDPOINT_PAGE_URL'),
                'page',
                self._decorate(self.page)
            )
            app.register_blueprint(
                self.blueprint,
                url_prefix=app.config.get('SITEMAP_BLUEPRINT_URL_PREFIX')
            )

        if (command_name or (command_name is None and self.command_name)) \
                and hasattr(app, 'cli'):
            from .cli import sitemap
            app.cli.add_command(sitemap, command_name or self.command_name)

    def _decorate(self, view):
        """Decorate view with given decorators."""
        response = (self.gzip_response if self.app.config['SITEMAP_GZIP'] else
                    self.xml_response)

        @wraps(view)
        def wrapper(*args, **kwargs):
            new_view = view
            for decorator in self.decorators:
                new_view = decorator(new_view)
            return response(new_view(*args, **kwargs))
        return wrapper

    def sitemap(self):
        """Generate sitemap.xml."""
        size = self.app.config['SITEMAP_MAX_URL_COUNT']
        args = [iter(self._generate_all_urls())] * size
        run = zip_longest(*args)
        try:
            urlset = next(run)
        except StopIteration:
            # Special case with empty list of urls.
            urlset = [None]

        if urlset[-1] is None:
            return render_template('flask_sitemap/sitemap.xml',
                                   urlset=filter(None, urlset))

        def pages():
            kwargs = dict(
                _external=True,
                _scheme=self.app.config.get('SITEMAP_URL_SCHEME')
            )
            kwargs['page'] = 1
            yield {'loc': url_for('flask_sitemap.page', **kwargs)}
            sitemap_page_needed.send(current_app._get_current_object(),
                                     page=1, urlset=urlset)
            for urlset_ in run:
                kwargs['page'] += 1
                yield {'loc': url_for('flask_sitemap.page', **kwargs)}
                sitemap_page_needed.send(current_app._get_current_object(),
                                         page=kwargs['page'], urlset=urlset_)

        return render_template('flask_sitemap/sitemapindex.xml',
                               sitemaps=pages())

    def render_page(self, urlset=None):
        """Render GZipped sitemap template with given url set."""
        return render_template('flask_sitemap/sitemap.xml',
                               urlset=urlset or [])

    def page(self, page):
        """Generate sitemap for given range of urls."""
        size = self.app.config['SITEMAP_MAX_URL_COUNT']
        urlset = islice(self._generate_all_urls(), (page-1)*size, page*size)
        return self.render_page(urlset=urlset)

    def register_generator(self, generator):
        """Register an URL generator.

        The function should return an iterable of URL paths or
        ``(endpoint, values)`` tuples to be used as
        ``url_for(endpoint, **values)``.

        :return: the original generator function
        """
        self.url_generators.append(generator)
        # Allow use as a decorator
        return generator

    def _routes_without_params(self):
        if self.app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS']:
            ignore = set(self.app.config['SITEMAP_IGNORE_ENDPOINTS'] or [])
            for rule in self.app.url_map.iter_rules():
                if rule.endpoint not in ignore and 'GET' in rule.methods and \
                        len(rule.arguments) == 0:
                    yield rule.endpoint, {}

    def _generate_all_urls(self):
        """Run all generators and yield (url, enpoint) tuples."""
        ignore = set(self.app.config['SITEMAP_IGNORE_ENDPOINTS'] or [])
        kwargs = dict(
            _external=True,
            _scheme=self.app.config.get('SITEMAP_URL_SCHEME')
        )

        def generator():
            for generator in self.url_generators:
                for generated in generator():
                    result = {}
                    if isinstance(generated, string_types):
                        result['loc'] = generated
                    else:
                        if isinstance(generated, Mapping):
                            values = generated
                            # The endpoint defaults to the name of the
                            # generator function, just like with Flask views.
                            endpoint = generator.__name__
                        else:
                            # Assume a tuple.
                            endpoint, values = generated[0:2]
                            # Get optional lastmod, changefreq, and priority
                            left = generated[2:]
                            for key in ['lastmod', 'changefreq', 'priority']:
                                if len(left) == 0:
                                    break
                                result[key] = left[0]
                                left = left[1:]

                        # Check if the endpoint should be skipped
                        if endpoint in ignore:
                            continue

                        values.update(kwargs)
                        result['loc'] = url_for(endpoint, **values)
                    yield result

        # A request context is required to use url_for
        if not has_request_context():
            with self.app.test_request_context():
                for result in generator():
                    yield result
        else:
            for result in generator():
                yield result

    def gzip_response(self, data):
        """Gzip response data and create new Response instance."""
        gzip_buffer = BytesIO()
        gzip_file = gzip.GzipFile(mode='wb', compresslevel=6,
                                  fileobj=gzip_buffer)
        gzip_file.write(data.encode('utf-8'))
        gzip_file.close()
        response = Response()
        response.data = gzip_buffer.getvalue()
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = len(response.data)

        return response

    def xml_response(self, data):
        """Return a standard XML response."""
        response = make_response(data)
        response.headers["Content-Type"] = "application/xml"

        return response


__all__ = ('Sitemap', '__version__', 'sitemap_page_needed')
