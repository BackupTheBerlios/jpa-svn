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

"""List of known entry categories"""

__revision__ = '$Id$'

import os.path as op

import gobject, gtk, gtk.glade, gtk.gdk

import appconst, datamodel, apputils

class CategoriesDialog:
    
    def __init__(self):
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, 'frmCategories', 'jpa')
        self.window = self.wTree.get_widget('frmCategories')
        self.window.set_icon_from_file(op.join(appconst.PATHS['img'],
            'darkbeer.xpm'))
        self.wTree.signal_autoconnect(self)

    def show(self):
        apputils.startWait(self.window)
        try:
            categoryList = self.wTree.get_widget('lvCategory')
            model = gtk.ListStore(str, str, gobject.TYPE_PYOBJECT)
            categories = datamodel.Category.select(orderBy='name')
            for category in categories:
                model.append((category.name.encode('utf-8'),
                    category.description.encode('utf-8'), category))
            cells = (gtk.CellRendererText(), gtk.CellRendererText())
            column0 = gtk.TreeViewColumn(_('Name'), cells[0], text=0)
            column1 = gtk.TreeViewColumn(_('Description'), cells[1], text=1)
            categoryList.append_column(column0)
            categoryList.append_column(column1)
            categoryList.set_model(model)
        finally:
            apputils.endWait(self.window)
        self.window.present()
    
    def on_btnClose_clicked(self, *args):
        self.window.destroy()