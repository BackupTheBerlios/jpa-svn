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

"""Dialog with license information"""

__revision__ = '$Id$'

import os.path as op

import gtk, pango
import gtk.glade

import appconst

class LicenseDialog:
    """
    Window with license text.
    """
    
    def __init__(self):
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, 'frmLicense', 'jpa')
        self.wTree.signal_autoconnect(self)
        self.window = self.wTree.get_widget('frmLicense')
        self.window.set_icon_from_file(op.join(appconst.PATHS['img'],
            'darkbeer.xpm'))
        self.licenseView = self.wTree.get_widget('tvLicense')

    def show(self):
        self.loadLicenseText()
        self.window.present()
    
    def loadLicenseText(self):
        licFile = op.join(appconst.PATHS['doc'], 'COPYING')
        fp = open(licFile)
        try:
            data = fp.read()
        finally:
            fp.close()
        bf = gtk.TextBuffer(None)
        self.licenseView.set_buffer(bf)
        bf.insert_at_cursor(data, len(data))
    
    def on_btnClose_clicked(self, *args):
        self.window.destroy()
