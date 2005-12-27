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

"""Category item editor"""

__revision__ = '$Id$'

import gtk
import gtk.glade

import appconst

class CategoryDialog:
    
    def __init__(self, category=None):
        self.category = category
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, 'frmCategory', 'jpa')
        self.window = self.wTree.get_widget('frmCategory')
        self.edName = self.wTree.get_widget('edName')
        self.edDescription = self.wTree.get_widget('edDescription')
        self.wTree.signal_autoconnect(self)
    
    def show(self):
        if self.category:
            name = self.category.name.encode('utf-8')
            description = self.category.description.encode('utf-8')
            self.edName.set_text(name)
            self.edDescription.set_text(description)
        self.window.present()
    
    ### signal handlers ###
    def on_btnOk_clicked(self, *args):
        name = self.edName.get_text().decode('utf-8')
        description = self.edDescription.get_text().decode('utf-8')
        if self.category:
            self.category.name = name
            self.category.description = description
        else:
            datamodel.EntryCategory(name, description)
        self.window.destroy()
    
    def on_btnCancel_clicked(self, *args):
        self.window.destroy()
