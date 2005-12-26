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

"""Dialog for entry editing"""

__revision__ = '$Id$'

import os.path as op

import gtk, gobject
import gtk.glade

import appconst, datamodel, apputils

class EntryDialog:
    
    def __init__(self, entryId):
        self.modified = False
        self.entry = None
        if entryId:
            self.entry = datamodel.Entry.get(entryId)
        self.entryId = entryId
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, 'frmEntry', 'jpa')
        self.window = self.wTree.get_widget('frmEntry')
        self.window.set_icon_from_file(op.join(appconst.PATHS['img'],
            'darkbeer.xpm'))
        self.wTree.signal_autoconnect(self)
    
    def show(self):
        categoryList = self.wTree.get_widget('lvCategory')
        model = gtk.ListStore(bool, str)
        categories = datamodel.Category.select(orderBy='name')
        for category in categories:
            model.append((False, category.name.encode('utf-8')))
        cell0 = gtk.CellRendererToggle()
        cell0.set_property('radio', False)
        cell0.set_property('activatable', True)
        cell0.connect('toggled', self.on_lvCategory_toggle, model)
        column0 = gtk.TreeViewColumn('use', cell0, active=0)
        cell1 = gtk.CellRendererText()
        column1 = gtk.TreeViewColumn('name', cell1, text=1)
        categoryList.append_column(column0)
        categoryList.append_column(column1)
        categoryList.set_model(model)
        self.window.present()
    
    def on_lvCategory_toggle(self, cell, path, model=None):
        iter = model.get_iter(path)
        model.set_value(iter, 0, not cell.get_active())

    def on_btnCancel_clicked(self, *args):
        """
        if self.modified:
            if apputils.question(_('Entry has been modified, do you want to save it?')):
                self.window.destroy()
        else:
            self.window.destroy()
        """
        print 'btnCancel_clicked'
        self.window.destroy()
        return False
    
    def on_btnOk_clicked(self, *args):
        print 'btnOk_clicked'
        self.window.destroy()
        return False

    def on_frmEntry_delete_event(self, *args):
        print 'delete_event'
