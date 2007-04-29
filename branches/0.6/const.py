# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""The whole-application constants"""

__revision__ = '$Id$'

import os

# program directories and file paths
USER_DIR = os.path.expanduser('~/.jpa')
if not os.path.isdir(USER_DIR):
    os.makedirs(USER_DIR)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
GLADE_PATH = os.path.join(BASE_DIR, 'glade', 'jpa.glade')

# configuration defaults
CONFIG_DEFAULTS = {
    'blogger': {
        'login': '',
        'password': '',
        'save_credentials': '0',
    },
}

DEBUG = True

VERSION = ('0', '6', '0')
VERSION_STRING = '.'.join(VERSION)
