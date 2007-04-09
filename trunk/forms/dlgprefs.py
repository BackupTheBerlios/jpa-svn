# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Preferences dialog"""

__revision__ = '$Id$'

import gtk
import gtk.glade

import forms
import const


def edit_preferences(config):
    dlg = PreferencesWindow(config)


class PreferencesWindow(object):

    def __init__(self, config):
        self.cfg = config
        self.w_tree = gtk.glade.XML(const.GLADE_PATH, 'dlg_prefs', 'jpa')
        self.w_tree.signal_autoconnect(self)
        self.window = self.w_tree.get_widget('dlg_prefs')
        forms.set_window_icon(self.window)
        self.ed_login = self.w_tree.get_widget('ed_login')
        self.tbl_auth_data = self.w_tree.get_widget('tbl_auth_data')
        self.run()

    def run(self):
        while 1:
            ret = self.window.run()
            if ret == gtk.RESPONSE_APPLY:
                pass
            elif ret == gtk.RESPONSE_OK:
                break
            else:
                break
        self.window.destroy()

    # GTK signal handlers
    def on_check_save_auth_toggled(self, *args):
        self.tbl_auth_data.set_sensitive(args[0].get_active())
        self.ed_login.grab_focus()