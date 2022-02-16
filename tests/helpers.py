# -*- coding: utf-8 -*-
#
# This file is part of Flask-Sitemap
# Copyright (C) 2014 CERN.
#
# Flask-Sitemap is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Test helpers."""

from unittest import TestCase

from flask import Flask


class FlaskTestCase(TestCase):
    """Mix-in class for creating the Flask application."""

    def setUp(self):
        """Test setup."""
        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.logger.disabled = True
        self.app = app


def dummy_decorator(dummy):
    """Dummy decorator."""
    return lambda *args, **kwargs: 'dummy'
