# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Authentication/login dialog"""

__revision__ = '$Id$'

import os

import gtk

import const
import forms
from forms.gladehelper import GladeWindow

def get_auth_data(captcha=None):
    dlg = AuthenticationDialog(captcha)
    return dlg.run()


class AuthenticationDialog(GladeWindow):

    def __init__(self, captcha):
        self.captcha = captcha
        self.create_ui(const.GLADE_PATH, 'dlg_auth', domain='jpa')
        self.window = self.ui.dlg_auth
        forms.set_window_icon(self.window)
        self._set_widgets()

    def run(self):
        result = [None, None, None]
        while 1:
            ret = self.window.run()
            if ret == gtk.RESPONSE_OK:
                result = [self.ui.ed_login.get_text().decode('utf-8'),
                    self.ui.ed_password.get_text().decode('utf-8')]
                if self.captcha:
                    result.append(self.ui.ed_captcha_text.get_text().decode('utf-8'))
                else:
                    result.append(None)
                if self.ui.check_save_auth.get_active():
                    self._save_auth_data()
            break
        return result

    def _set_widgets(self):
        if self.captcha:
            self.ui.box_captcha.show_all()
        else:
            self.ui.box_captcha.hide_all()

    def _save_auth_data(self):
        cfg = const.CONFIG
        if not cfg.has_section('auth'):
            cfg.add_section('auth')
        cfg.set('auth', 'login', self.ui.ed_login.get_text())
        cfg.set('auth', 'password', self.ui.ed_password.get_text())
        config_file = os.path.join(const.USER_DIR, 'config')
        fp = open(config_file, 'w')
        try:
            cfg.write(fp)
        finally:
            fp.close()
