# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Preferences dialog"""

__revision__ = '$Id$'

import os
from ConfigParser import NoSectionError

import gtk

import forms
from forms.gladehelper import GladeWindow
import const


def edit_preferences(config=None):
    if config is None:
        config = const.CONFIG
    dlg = PreferencesWindow(config)


class PreferencesWindow(GladeWindow):

    def __init__(self, config):
        self.cfg = config
        self.create_ui(const.GLADE_PATH, 'dlg_prefs', domain='jpa')
        self.window = self.ui.dlg_prefs
        forms.set_window_icon(self.window)
        self._set_widgets()
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

    def _set_widgets(self):
        model = gtk.ListStore(str)
        for markup_type in const.MARKUP_TYPES:
            model.append((markup_type, ))
        self.ui.combo_texttype.set_model(model)

    def _load_config(self):
        # Blogger authorization data
        try:
            auth = dict(self.cfg.items('auth'))
        except NoSectionError:
            auth = {}
        save_auth = (auth.get('save_auth', '1') == '1')
        self.ui.ed_login.set_text(auth.get('login', ''))
        self.ui.ed_password.set_text(auth.get('password', ''))
        self.ui.check_save_auth.set_active(save_auth)
        self.ui.tbl_auth_data.set_sensitive(save_auth)
        # misc
        try:
            misc = dict(self.cfg.items('misc'))
        except NoSectionError:
            misc = {}
        content_type = misc.get('content_type', 'markdown')
        self.ui.combo_texttype.set_active(const.MARKUP_TYPES.index(content_type))
        # fonts
        try:
            fonts = dict(self.cfg.items('fonts'))
        except NoSectionError:
            fonts = {}
        self.ui.font_button_entry_view.set_font_name(fonts.get('entry',
            'Sans 12'))
        self.ui.font_button_entry_editor.set_font_name(fonts.get('editor',
            'Monospace 10'))
        self.ui.font_button_log.set_font_name(fonts.get('log', 'Monospace 10'))
        # network
        try:
            newtwork = dict(self.cfg.items('networks'))
        except NoSectionError:
            network = {}
        use_proxy = (network.get('use_proxy', '0') == '1')
        self.ui.check_use_proxy.set_active(use_proxy)
        self.ui.ed_proxy_host.set_text(network.get('proxy_host', ''))
        self.ui.spin_proxy_port.set_value(int(network.get('proxy_port', 8080)))
        self.ui.ed_proxy_login.set_text(network.get('proxy_login', ''))
        self.ui.ed_proxy_password.set_text(network.get('proxy_password', ''))
        self.ui.tbl_proxy_settings.set_sensitive(use_proxy)

    # GTK signal handlers
    def on_check_save_auth_toggled(self, *args):
        self.ui.tbl_auth_data.set_sensitive(args[0].get_active())

    def on_check_use_proxy_toggled(self, *args):
        self.ui.tbl_proxy_settings.set_sensitive(args[0].get_active())

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
        # misc - miscellanea
        if not self.cfg.has_section('misc'):
            self.cfg.add_section('misc')
        model = self.ui.combo_texttype.get_model()
        active = self.ui.combo_texttype.get_active()
        if active < 0:
            content_type = 'markdown'
        else:
            content_type = model[active][0]
        self.cfg.set('misc', 'content_type', content_type)
        # fonts
        if not self.cfg.has_section('fonts'):
            self.cfg.add_section('fonts')
        self.cfg.set('fonts', 'entry',
            self.ui.font_button_entry_view.get_font_name())
        self.cfg.set('fonts', 'editor',
            self.ui.font_button_entry_editor.get_font_name())
        self.cfg.set('fonts', 'log',
            self.ui.font_button_log.get_font_name())
        # network
        if not self.cfg.has_section('network'):
            self.cfg.add_section('network')
        use_proxy = self.ui.check_use_proxy.get_active()
        if use_proxy:
            proxy_host = self.ui.ed_proxy_host.get_text()
            proxy_port = str(self.ui.spin_proxy_port.get_value_as_int())
            proxy_login = self.ui.ed_proxy_login.get_text()
            proxy_passwd = self.ui.ed_proxy_password.get_text()
        else:
            proxy_host = ''
            proxy_port = '0'
            proxy_login = ''
            proxy_passwd = ''
        if use_proxy:
            value = '1'
        else:
            value = '0'
        self.cfg.set('network', 'use_proxy', value)
        self.cfg.set('network', 'proxy_host', proxy_host)
        self.cfg.set('network', 'proxy_port', proxy_port)
        self.cfg.set('network', 'proxy_login', proxy_login)
        self.cfg.set('network', 'proxy_password', proxy_passwd)
        # now, save configuration file
        config_file = os.path.join(const.USER_DIR, 'config')
        fp = open(config_file, 'w')
        try:
            self.cfg.write(fp)
        finally:
            fp.close()
