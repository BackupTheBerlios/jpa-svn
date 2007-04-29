# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""About program dialog"""

__revision__ = '$Id$'

import os
import ConfigParser

import gtk

import sysutils
import const
import forms

def open_url(dialog, url, user_data):
    system = const.CONFIG.get('misc', 'system')
    browser_cmd = const.CONFIG.get('misc', 'browser_command')
    sysutils.open_url(url, system=system)

def show_dialog():
    dlg = gtk.AboutDialog()
    try:
        gtk.about_dialog_set_url_hook(open_url, None)
        forms.set_window_icon(dlg)
        dlg.set_name('JPA')
        dlg.set_version(const.VERSION_STRING)
        dlg.set_comments(_('Blogger Publishing Assistant'))
        dlg.set_website('http://jpa.berlios.de')
        fp = open(os.path.join(const.BASE_DIR, 'doc', 'AUTHORS'))
        try:
            lines = fp.read().strip().split('\n')
        finally:
            fp.close()
        dlg.set_authors(lines)
        dlg.set_copyright('Copyright: (c) 2007, Jarek Zgoda <jzgoda@o2.pl>')
        fp = open(os.path.join(const.BASE_DIR, 'doc', 'COPYING'))
        try:
            dlg.set_license(fp.read().strip())
        finally:
            fp.close()
        dlg.run()
    finally:
        dlg.destroy()
