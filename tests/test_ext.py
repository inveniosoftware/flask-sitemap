# -*- coding: utf-8 -*-
#
# This file is part of Flask-Sitemap
# Copyright (C) 2014, 2015 CERN.
#
# Flask-Sitemap is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

from __future__ import absolute_import

import os
import shutil
import sys

from contextlib import contextmanager
from datetime import datetime
from tempfile import mkdtemp

from click.testing import CliRunner
from flask import request_started, request, url_for
from flask.cli import ScriptInfo
from flask_script import Manager
from flask_sitemap import Sitemap, config as default_config, \
    script, sitemap_page_needed

from .helpers import FlaskTestCase


class TestSitemap(FlaskTestCase):

    """Test extension creation and functionality."""

    def test_version(self):
        # Assert that version number can be parsed.
        from flask_sitemap import __version__
        from distutils.version import LooseVersion
        LooseVersion(__version__)

    def test_creation(self):
        assert 'sitemap' not in self.app.extensions
        Sitemap(app=self.app)
        assert isinstance(self.app.extensions['sitemap'], Sitemap)

    def test_creation_old_flask(self):
        # Simulate old Flask (pre 0.9)
        del self.app.extensions
        Sitemap(app=self.app)
        assert isinstance(self.app.extensions['sitemap'], Sitemap)

    def test_creation_init(self):
        assert 'sitemap' not in self.app.extensions
        r = Sitemap()
        r.init_app(app=self.app)
        assert isinstance(self.app.extensions['sitemap'], Sitemap)

    def test_double_creation(self):
        Sitemap(app=self.app)
        self.assertRaises(RuntimeError, Sitemap, app=self.app)

    def test_default_config(self):
        Sitemap(app=self.app)
        for k in dir(default_config):
            if k.startswith('SITEMAP_'):
                assert self.app.config.get(k) == getattr(default_config, k)

    def test_empty_generator(self):
        Sitemap(app=self.app)
        with self.app.test_client() as c:
            assert b'loc' not in c.get('/sitemap.xml').data

    def test_url_generator(self):
        self.app.config['SERVER_NAME'] = 'www.example.com'
        sitemap = Sitemap(app=self.app)
        now = datetime.now().isoformat()

        @self.app.route('/')
        def index():
            pass

        @self.app.route('/<username>')
        def user(username):
            pass

        @sitemap.register_generator
        def user():
            yield 'http://www.example.com/first'
            yield {'username': 'second'}
            yield 'user', {'username': 'third'}
            yield 'user', {'username': 'fourth'}, now

        results = sitemap._generate_all_urls()
        assert next(results)['loc'] == 'http://www.example.com/first'
        assert next(results)['loc'] == 'http://www.example.com/second'
        assert next(results)['loc'] == 'http://www.example.com/third'
        assert next(results)['loc'] == 'http://www.example.com/fourth'

        with open(os.path.join(
                os.path.dirname(__file__), 'data', 'sitemap.xml'), 'r') as f:
            out = f.read().format(now=now).strip()
            assert out == sitemap.sitemap()

    def test_endpoints_without_arguments(self):
        self.app.config['SERVER_NAME'] = 'www.example.com'
        self.app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
        sitemap = Sitemap(app=self.app)
        now = datetime.now().isoformat()

        @self.app.route('/')
        def index():
            pass

        @self.app.route('/first')
        def first():
            pass

        @self.app.route('/second')
        def second():
            pass

        @self.app.route('/<username>')
        def user(username):
            pass

        @sitemap.register_generator
        def user():
            yield 'user', {'username': 'third'}
            yield 'user', {'username': 'fourth'}, now

        results = [result['loc'] for result in sitemap._generate_all_urls()]
        assert 'http://www.example.com/' in results
        assert 'http://www.example.com/first' in results
        assert 'http://www.example.com/second' in results
        assert 'http://www.example.com/third' in results
        assert 'http://www.example.com/fourth' in results

    def test_ignore_endpoints(self):
        self.app.config['SERVER_NAME'] = 'www.example.com'
        self.app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
        self.app.config['SITEMAP_IGNORE_ENDPOINTS'] = ['first', 'user']
        sitemap = Sitemap(app=self.app)
        now = datetime.now().isoformat()

        @self.app.route('/')
        def index():
            pass

        @self.app.route('/first')
        def first():
            pass

        @self.app.route('/second')
        def second():
            pass

        @self.app.route('/<username>')
        def user(username):
            pass

        @sitemap.register_generator
        def user():
            yield 'user', {'username': 'third'}
            yield 'user', {'username': 'fourth'}, now

        results = [result['loc'] for result in sitemap._generate_all_urls()]
        assert 'http://www.example.com/' in results
        assert 'http://www.example.com/first' not in results
        assert 'http://www.example.com/second' in results
        assert 'http://www.example.com/third' not in results
        assert 'http://www.example.com/fourth' not in results

    def test_decorators_order(self):
        def first(dummy):
            return lambda *args, **kwargs: 'first'

        def second(dummy):
            return lambda *args, **kwargs: 'second'

        def third(dummy):
            return lambda *args, **kwargs: 'third'

        self.app.config['SITEMAP_VIEW_DECORATORS'] = [
            first, second, 'tests.helpers.dummy_decorator']
        sitemap = Sitemap(app=self.app)

        assert first in sitemap.decorators
        assert second in sitemap.decorators

        with self.app.test_client() as c:
            assert b'dummy' == c.get('/sitemap.xml').data

        sitemap.decorators.append(third)

        with self.app.test_client() as c:
            assert b'third' == c.get('/sitemap.xml').data

    def test_pagination(self):
        self.app.config['SERVER_NAME'] = 'www.example.com'
        self.app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
        self.app.config['SITEMAP_MAX_URL_COUNT'] = 10
        sitemap = Sitemap(app=self.app)
        now = datetime.now().isoformat()

        @self.app.route('/')
        def index():
            pass

        @self.app.route('/first')
        def first():
            pass

        @self.app.route('/second')
        def second():
            pass

        @self.app.route('/<username>')
        def user(username):
            pass

        @sitemap.register_generator
        def user():
            for number in range(20):
                yield 'user', {'username': 'test{0}'.format(number)}

        directory = mkdtemp()
        runner = CliRunner()

        try:
            result = runner.invoke(
                self.app.cli,
                ['sitemap', '-o', directory, '-v'],
                obj=ScriptInfo(create_app=lambda _: self.app),
            )
            assert 'sitemap1.xml\nsitemap2.xml\nsitemap3.xml\nsitemap.xml' \
                in result.output
            # assert result.exit_code == 0

            with self.app.test_client() as c:
                data = c.get('/sitemap.xml').data
                data1 = c.get('/sitemap1.xml').data

                assert b'sitemapindex' in data
                assert len(data1) > 0

                with open(os.path.join(directory, 'sitemap.xml'), 'rb') as f:
                    assert f.read() == data

                with open(os.path.join(directory, 'sitemap1.xml'), 'rb') as f:
                    assert f.read() == data1
        finally:
            shutil.rmtree(directory)

        directory = mkdtemp()
        manager = Manager(self.app)
        manager.add_command('sitemap', script.Sitemap())

        try:
            manager.handle('manage.py', ['sitemap', '-o', directory])

            with self.app.test_client() as c:
                data = c.get('/sitemap.xml').data
                data1 = c.get('/sitemap1.xml').data

                assert b'sitemapindex' in data
                assert len(data1) > 0

                with open(os.path.join(directory, 'sitemap.xml'), 'rb') as f:
                    assert f.read() == data

                with open(os.path.join(directory, 'sitemap1.xml'), 'rb') as f:
                    assert f.read() == data1
        finally:
            shutil.rmtree(directory)

    def test_signals(self):
        now = datetime.now().isoformat()
        cache = {}

        @sitemap_page_needed.connect
        def create_page(app, page, urlset):
            cache[page] = sitemap.render_page(urlset=urlset)

        def load_page(fn):
            from functools import wraps

            @wraps(fn)
            def loader(*args, **kwargs):
                page = kwargs.get('page')
                data = cache.get(page)
                return data if data else fn(*args, **kwargs)
            return loader

        self.app.config['SERVER_NAME'] = 'www.example.com'
        self.app.config['SITEMAP_GZIP'] = True
        self.app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
        self.app.config['SITEMAP_MAX_URL_COUNT'] = 10
        self.app.config['SITEMAP_VIEW_DECORATORS'] = [load_page]
        sitemap = Sitemap(app=self.app)

        @self.app.route('/')
        def index():
            pass

        @self.app.route('/first')
        def first():
            pass

        @self.app.route('/second')
        def second():
            pass

        @self.app.route('/<username>')
        def user(username):
            pass

        @sitemap.register_generator
        def user():
            for number in range(20):
                yield 'user', {'username': 'test{0}'.format(number)}

        with self.app.test_client() as c:
            assert 200 == c.get('/sitemap.xml').status_code
            assert len(cache) == 3
            for page in range(len(cache)):
                assert sitemap.gzip_response(cache[page+1]).data == c.get(
                    '/sitemap{0}.xml'.format(page+1)).data
