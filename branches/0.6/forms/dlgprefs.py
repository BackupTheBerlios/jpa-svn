# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Preferences dialog"""

__revision__ = '$Id$'

import os
from ConfigParser import NoSectionError, NoOptionError

import gtk
import gtk.glade

import forms
from forms.gladehelper import GladeWindow
import const


def edit_preferences(config):
    dlg = PreferencesWindow(config)


class PreferencesWindow(GladeWindow):

    def __init__(self, config):
        self.cfg = config
        self.create_ui(const.GLADE_PATH, 'dlg_prefs', domain='jpa')
        self.window = self.ui.dlg_prefs
        forms.set_window_icon(self.window)
        self._load_config()
        self.run()

    def run(self):
        while 1:
            ret = self.window.run()
            if ret == gtk.RESPONSE_APPLY:
                self.save_config()
            elif ret == gtk.RESPONSE_OK:
                self.save_config()
                break
            else:
                break
        self.window.destroy()

    def _load_config(self):
        try:
            auth = dict(self.cfg.items('auth'))
        except NoSectionError:
            auth = {}
        save_auth = (auth.get('save_auth', '1') == '1')
        self.ui.ed_login.set_text(auth.get('login', ''))
        self.ui.ed_password.set_text(auth.get('password', ''))
        self.ui.check_save_auth.set_active(save_auth)

    # GTK signal handlers
    def on_check_save_auth_toggled(self, *args):
        self.ui.tbl_auth_data.set_sensitive(args[0].get_active())
        self.ui.ed_login.grab_focus()

    # miscellaneous
    def save_config(self):
        # save configuration by sections
        # Blogger authorization data
        if not self.cfg.has_section('auth'):
            self.cfg.add_section('auth')
        save_auth = self.ui.check_save_auth.get_active()
        if save_auth:
            login = self.ui.ed_login.get_text()
            password = self.ui.ed_password.get_text()
        else:
            login = ''
            password = ''
        self.cfg.set('auth', 'login', login)
        self.cfg.set('auth', 'password', password)
        if save_auth:
            value = '1'
        else:
            value = '0'
        self.cfg.set('auth', 'save_auth', value)
        # save configuration file
        config_file = os.path.join(const.USER_DIR, 'config')
        fp = open(config_file, 'w')
        try:
            self.cfg.write(fp)
        finally:
            fp.close()
