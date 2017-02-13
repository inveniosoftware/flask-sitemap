# -*- coding: utf-8 -*-
#
# This file is part of Flask-Sitemap
# Copyright (C) 2014, 2015 CERN.
# Copyright (C) 2018 ETH Zurich, Swiss Data Science Center, Jiri Kuncar.
#
# Flask-Sitemap is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

import os
import re
import sys

from setuptools import setup

needs_pytest = set(['pytest', 'test', 'ptr']).intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

# Get the version string. Cannot be done with import!
with open(os.path.join('flask_sitemap', 'version.py'), 'rt') as f:
    version = re.search(
        '__version__\s*=\s*"(?P<version>.*)"\n',
        f.read()
    ).group('version')

extras_require = {
    'docs': ['sphinx'],
    'cli': ['Flask-Script'],
}

tests_require = [
    'pytest-cache>=1.0',
    'pytest-cov>=2.2.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.5',
    'coverage',
]

# Extend dependencies with extra packages
for key, extra in extras_require.items():
    if key != 'docs':
        tests_require += extra
        extras_require['docs'] += extra

setup(
    name='Flask-Sitemap',
    version=version,
    url='http://github.com/inveniosoftware/flask-sitemap/',
    license='BSD',
    author='Invenio collaboration',
    author_email='info@inveniosoftware.org',
    description='Flask extension that helps with sitemap generation.',
    long_description=open('README.rst').read(),
    packages=['flask_sitemap'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    setup_requires=pytest_runner,
    install_requires=[
        'Flask',
        'blinker',
    ],
    extras_require=extras_require,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 5 - Production/Stable'
    ],
)
