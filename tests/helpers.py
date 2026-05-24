# SPDX-FileCopyrightText: 2014 CERN.
# SPDX-License-Identifier: BSD-3-Clause

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
