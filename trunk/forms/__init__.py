# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Application dialogs"""

__revision__ = '$Id$'

from frmutils import set_window_icon

from frmmain import MainWindow
from dlgabout import show_dialog as show_about
from dlgentry import edit_new_entry
from dlgprefs import edit_preferences
from dlgbloglist import show_blogs_list
from dlgauth import get_auth_data
