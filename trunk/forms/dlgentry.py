# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Entry editing dialog"""

__revision__ = '$Id$'

import os

import gtk
import gtk.glade

import const

def edit_new_entry():
    dlg = EntryWindow()

class EntryWindow(object):

    def __init__(self, entry_dict={}):
        self.w_tree = gtk.glade.XML(const.GLADE_PATH, 'dlg_entry', 'jpa')
        self.w_tree.signal_autoconnect(self)
        self.window = self.w_tree.get_widget('dlg_entry')
        self.window.present()
