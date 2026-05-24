#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2013-2020 CERN.
# SPDX-License-Identifier: BSD-3-Clause

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

python -m check_manifest --ignore ".*-requirements.txt,.gitmodules,docs/_themes"
git submodule update --init
python -m sphinx.cmd.build -qnNW docs docs/_build/html
python -m pytest
python -m sphinx.cmd.build -qnNW -b doctest docs docs/_build/doctest
