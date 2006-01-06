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

import appconst, datamodel, apputils, notifiable
from appwindow import ListWindow

class CategoriesDialog(ListWindow):
    
    def __init__(self, controller):
        ListWindow.__init__(self, 'frmCategories', controller)
        self.categoryList = self.wTree.get_widget('lvCategory')
        self.listMenuTree = gtk.glade.XML(appconst.GLADE_PATH, 'pmListEdit',
            'jpa')
        self.btnAdd = self.wTree.get_widget('btnAdd')
        self.btnEdit = self.wTree.get_widget('btnEdit')
        self.btnDel = self.wTree.get_widget('btnDel')

    def show(self):
        apputils.startWait(self.window)
        try:
            self.model = gtk.ListStore(str, str, gobject.TYPE_PYOBJECT)
            cells = (gtk.CellRendererText(), gtk.CellRendererText())
            column0 = gtk.TreeViewColumn(_('Name'), cells[0], text=0)
            column1 = gtk.TreeViewColumn(_('Description'), cells[1], text=1)
            self.categoryList.append_column(column0)
            self.categoryList.append_column(column1)
            self.categoryList.set_model(self.model)
            self._loadData()
            if len(self.model) > 0:
                sel = self.categoryList.get_selection()
                sel.select_path(0)
            self._enableActions()
        finally:
            apputils.endWait(self.window)
        self.window.present()
    
    def notify(self, event):
        if event == 'data-changed':
            apputils.startWait(self.window)
            try:
                self.model.clear()
                self._loadData()
            finally:
                apputils.endWait(self.window)
    
    ### "private" methods ###
    def _loadData(self):
        categories = datamodel.Category.select(orderBy='name')
        for category in categories:
            name = category.name
            desc = apputils.ellipsize(category.description, 80)
            self.model.append((name.encode('utf-8'), desc.encode('utf-8'),
                category))
    
    def _getCategoryFromSelection(self):
        selection = self.categoryList.get_selection()
        model, selected = selection.get_selected()
        return model.get_value(selected, 2)
    
    def _enableActions(self):
        if len(self.model) == 0:
            enableAction = False
        else:
            category = self._getCategoryFromSelection()
            enableAction = (category.id > 1)
        self.miEdit.set_sensitive(enableAction)
        self.btnEdit.set_sensitive(enableAction)
        self.miDel.set_sensitive(enableAction)
        self.btnDel.set_sensitive(enableAction)
    
    def _add(self, *args):
        self.controller.newCategory(self)
    
    def _edit(self, *args):
        category = self._getCategoryFromSelection()
        self.controller.editCategory(category, self)
    
    def _del(self, *args):
        category = self._getCategoryFromSelection()
    
    ### signal handlers ###
    def on_lvCategory_button_press_event(self, *args):
        widget, event = args
        if event.button == 3:
            self.listMenu.popup(None, None, None, event.button, event.time)
    
    def on_lvCategory_cursor_changed(self, *args):
        self._enableActions()