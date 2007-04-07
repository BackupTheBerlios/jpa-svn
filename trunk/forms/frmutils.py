# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Miscellaneous form-related utilities"""

__revision__ = '$Id$'

import os

import const

def set_icon(window):
    window.set_icon_from_file(os.path.join(const.BASE_DIR,
        'blogger0.png'))