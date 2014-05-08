#!/usr/bin/env python

# -*- coding: utf-8 -*-

# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Copyright (C) 2013 Yahoo! Inc. All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import re

from setuptools import setup


def _path(fn):
    return os.path.join(os.path.dirname(__file__), fn)


def _has_all(text, search_for):
    matches = 0
    for s in search_for:
        if text.find(s) != -1:
            matches += 1
    return matches == len(search_for)


def _readme():
    # Filter out screenshots...
    lines = []
    with open(_path("README.rst"), "rb") as handle:
        contents = handle.read().decode('utf-8')
        for line in contents.splitlines():
            screenshot = False
            if _has_all(line, ['screenshots', '.png']):
                if re.match(r"^..(\s+)image::(.*)$", line, re.I):
                    screenshot = True
            if not screenshot:
                lines.append(line)
    return "\n".join(lines)


setup(name='gerrit-view',
      version='0.3.4',
      description='Gerrit viewer tools',
      author="Joshua Harlow",
      author_email='harlowja@yahoo-inc.com',
      url='http://github.com/harlowja/gerrit_view/',
      scripts=[
          _path(os.path.join('scripts', 'cgerrit')),
          _path(os.path.join('scripts', 'qgerrit')),
          _path(os.path.join('scripts', 'czuul')),
      ],
      license="ASL 2.0",
      install_requires=[
          'gerritlib',
          'prettytable',
          'requests',
          'six',
          'urwid',
          # Used for czuul detailing mode.
          'GitPython>=0.3.2.RC1',
      ],
      classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
      ],
      keywords="gerrit curses urwid console",
      long_description=_readme(),
     )
