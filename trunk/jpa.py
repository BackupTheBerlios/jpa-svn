#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Main program startup file"""

__revision__ = '$Id$'

import os, sys
import signal
import fcntl
import ConfigParser

import pygtk
pygtk.require('2.0')
import gtk

import const
import sysutils
import forms


class JPAApp(gtk.StatusIcon):
    """Main application class"""

    def __init__(self):
        gtk.StatusIcon.__init__(self)
        self.cfg = const.CONFIG = self._get_configuration()
        self.set_from_file(os.path.join(const.BASE_DIR, 'blogger.png'))
        self.set_tooltip('JPA v. %s' % const.VERSION_STRING)
        uimgr = self._create_ui()
        self.menu = uimgr.get_widget('/Menubar/Menu/About').props.parent
        self.connect('popup-menu', self._on_popup_menu)
        self.connect('activate', self._on_action_new)
        self.set_visible(True)

    def _get_configuration(self):
        config_file = os.path.join(const.USER_DIR, 'config')
        cfg = ConfigParser.SafeConfigParser()
        try:
            fp = open(config_file)
            try:
                cfg.readfp(fp)
            finally:
                fp.close()
        except IOError:
            # ignore this, the file just does not exist
            # we'll have an empty configuration and use defaults
            sysutils.initialize_config(cfg, **const.CONFIG_DEFAULTS)
        return cfg

    def _create_ui(self):
        ag = gtk.ActionGroup('Actions')
        actions = [
            ('Menu', None, 'Menu'),
            ('New', gtk.STOCK_NEW, _('_New...'), None,
                _('Write new blog entry'), self._on_action_new),
            ('Archive', None, _('A_rchive'), None,
                _('View archive of entries'), self._on_action_archive),
            ('Preferences', gtk.STOCK_PREFERENCES, _('_Preferences...'), None,
                _('Change program preferences'), self._on_action_preferences),
            ('About', gtk.STOCK_ABOUT, _('_About...'), None,
                _('About JPA, the Weblog Assistant'), self._on_action_about),
            ('Quit', gtk.STOCK_QUIT, _('_Quit'), None,
                _('Close the program'), self._on_action_quit),
        ]
        ag.add_actions(actions)
        ui = gtk.UIManager()
        ui.insert_action_group(ag, 0)
        ui.add_ui_from_file(os.path.join(const.BASE_DIR, 'ui',
            'mainmenu.ui.xml'))
        return ui

    def _on_popup_menu(self, status, button, time):
        self.menu.popup(None, None, None, button, time)

    def _on_action_new(self, *args):
        forms.edit_new_entry()

    def _on_action_archive(self, *args):
        pass

    def _on_action_preferences(self, *args):
        forms.edit_preferences(self.cfg)

    def _on_action_about(self, *args):
        forms.show_about()

    def _on_action_quit(self, *args):
        gtk.main_quit()


if __name__ == '__main__':
    pid_file = os.path.join(const.USER_DIR, 'jpa.pid')
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        # another instance is running
        sys.exit(0)
    basedir = os.path.dirname(os.path.realpath(__file__))
    if basedir.endswith('/share/jpa2'):
        sys.path.append(basedir[:-10] + 'lib/jpa2')
    import gettext, locale
    locale.setlocale(locale.LC_ALL, '')
    gtk.glade.bindtextdomain('jpa')
    gtk.glade.textdomain('jpa')
    gettext.install('jpa', unicode=True)
    SIGNALS = [signal.SIGINT, signal.SIGTERM, signal.SIGHUP]
    for sig in SIGNALS:
        signal.signal(sig, gtk.main_quit)
    app = JPAApp()
    gtk.main()
    if os.path.isfile(pid_file):
        os.unlink(pid_file)
