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


class JPAApp(object):
    """Main application class"""

    def __init__(self):
        self.cfg = const.CONFIG = self._get_configuration()
        self.main_window = forms.MainWindow()
        self.main_window.show()

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
