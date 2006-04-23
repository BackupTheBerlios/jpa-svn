# -*- coding: UTF-8 -*-

# This file is part of JPA.
# Copyright: (C) 2003 - 2005 Jarek Zgoda <jzgoda@o2.pl>
#
# JPA is free software; you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 2 of the License.
#
# JPA is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details.
#
# You should have received a copy of the GNU General Public License along with 
# JPA; if not, write to the Free Software Foundation, Inc., 
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""Informations about program"""

__revision__ = '$Id$'

import os.path as op

import gtk

import appconst, version
from appwindow import EditDialog

class AboutDialog(EditDialog):
    
    def __init__(self, parent):
        EditDialog.__init__(self, 'dlgAbout', parent)
        self.txLicense = self.wTree.get_widget('txLicense')
        self.lbVersion = self.wTree.get_widget('lbVersion')
        self._initGui()
    
    def _initGui(self):
        self.lbVersion.set_text(_('version: %s') % version.PROGVER)
        licFile = op.join(appconst.PATHS['doc'], 'COPYING')
        fp = open(licFile)
        try:
            data = fp.read()
        finally:
            fp.close()
        bf = gtk.TextBuffer(None)
        self.txLicense.set_buffer(bf)
        bf.set_text(data.decode('utf-8'))
    
    def run(self):
        self.window.run()
        self.window.destroy()
    
    def on_btnHomePage_clicked(self, *args):
        url = appconst.HOME_URL