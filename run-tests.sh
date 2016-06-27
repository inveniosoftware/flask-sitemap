#!/bin/sh
#
# This file is part of Flask-Sitemap
# Copyright (C) 2013, 2014 CERN.
#
# Flask-Sitemap is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

pydocstyle flask_sitemap && \
sphinx-build -qnNW docs docs/_build/html && \
python setup.py test
