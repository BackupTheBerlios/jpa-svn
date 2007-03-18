# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""About program dialog"""

__revision__ = '$Id$'

import os

import gtk
import gnome

def open_url(dialog, url, user_data):
    gnome.url_show(url)

def show_dialog(base_dir):
    dlg = gtk.AboutDialog()
    try:
        gtk.about_dialog_set_url_hook(open_url, None)
        dlg.set_name('JPA')
        dlg.set_version('0.6.0')
        dlg.set_comments(_('Blogger publishing assistant'))
        dlg.set_website('http://jpa.berlios.de')
        dlg.set_authors(['Jarek Zgoda <jzgoda@o2.pl>'])
        dlg.set_copyright(_('Copyright: (c) 2007, Jarek Zgoda <jzgoda@o2.pl>'))
        fp = open(os.path.join(base_dir, 'COPYING'))
        try:
            dlg.set_license(fp.read().strip())
        finally:
            fp.close()
        dlg.run()
    finally:
        dlg.destroy()
