# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Entry editing dialog"""

__revision__ = '$Id$'

import gtk, pango

import forms
from forms.gladehelper import GladeWindow
import const

def edit_new_entry():
    dlg = EntryWindow()

class EntryWindow(GladeWindow):

    def __init__(self, entry_dict={}):
        self.entry = entry_dict
        self.create_ui(const.GLADE_PATH, 'dlg_entry', domain='jpa')
        self.window = self.ui.dlg_entry
        forms.set_window_icon(self.window)
        self._set_widget_properties()
        self.run()

    def run(self):
        while 1:
            ret = self.window.run()
            if ret == gtk.RESPONSE_APPLY:
                self.save()
            elif ret == gtk.RESPONSE_OK:
                self.save()
                break
            else:
                break
        self.window.destroy()

    def save(self):
        if self.entry:
            entry = self.entry
        else:
            entry = {}

    def _set_widget_properties(self):
        try:
            font_name = const.CONFIG.get('fonts', 'editor')
        except:
            font_name = 'Monospace 10'
        self.ui.tv_text.modify_font(pango.FontDescription(font_name))
