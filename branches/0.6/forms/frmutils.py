# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Miscellaneous form-related utilities"""

__revision__ = '$Id$'

import os

from const import BASE_DIR

def set_window_icon(window):
    window.set_icon_from_file(os.path.join(BASE_DIR, 'blogger.png'))
