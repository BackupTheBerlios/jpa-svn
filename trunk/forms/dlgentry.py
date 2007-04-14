# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Entry editing dialog"""

__revision__ = '$Id$'

import os

import gtk, pango
import gtk.glade

import forms
from forms.gladehelper import GladeWindow
import const

def edit_new_entry():
    dlg = EntryWindow()

class EntryWindow(GladeWindow):

    def __init__(self, entry_dict={}):
        self.create_ui(const.GLADE_PATH, 'dlg_entry', domain='jpa')
        self.window = self.ui.dlg_entry
        forms.set_window_icon(self.window)
        self.ui.tv_text.modify_font(pango.FontDescription('Monospace'))
        self.window.present()
