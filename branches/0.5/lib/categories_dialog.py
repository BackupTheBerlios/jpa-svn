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

import louie
import gobject, gtk, gtk.glade, gtk.gdk

import appconst, datamodel, apputils, blogoper
from datamodel import Weblog
from appwindow import ListWindow
from appconst import DEBUG

class CategoriesDialog(ListWindow):
    
    def __init__(self, controller):
        ListWindow.__init__(self, 'frmCategories', controller)
        self.categoryList = self.wTree.get_widget('lvCategory')
        self.listMenuTree = gtk.glade.XML(appconst.GLADE_PATH, 'pmCatListEdit',
            'jpa')
        self.listMenuTree.signal_autoconnect(self)
        self.listMenu = self.listMenuTree.get_widget('pmCatListEdit')
        self.miSync = self.listMenuTree.get_widget('miSync')
        self.miAdd = self.listMenuTree.get_widget('miAdd')
        self.miEdit = self.listMenuTree.get_widget('miEdit')
        self.miDel = self.listMenuTree.get_widget('miDel')
        self.miClose = self.listMenuTree.get_widget('miClose')
        self.btnAdd = self.wTree.get_widget('btnAdd')
        self.btnEdit = self.wTree.get_widget('btnEdit')
        self.btnDel = self.wTree.get_widget('btnDel')
        self.ckbOnlyActive = self.wTree.get_widget('ckbOnlyActive')
        self._connectSignals()

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
    
    def updateStatus(self, message):
        louie.send('update-status', louie.Anonymous, message)
    
    def addCategories(self, categories):
        gobject.idle_add(self._addCategories, categories)
    
    def _connectSignals(self):
        louie.connect(self.onDataChanged, 'category-changed')
        louie.connect(self.onDataChanged, 'category-deleted')
    
    def _addCategories(self, categories):
        msg = _('Downloaded %d categories, do you want to update list?') \
            % len(categories)
        if apputils.question(msg):
            for remoteCat in categories:
                remoteCat['updated'] = False
                for (name, desc, category) in self.model:
                    if name.decode('utf-8') == remoteCat['name']:
                        category.description = remoteCat['description']
                        remoteCat['updated'] = True
            for remoteCat in categories:
                if not remoteCat['updated']:
                    name = remoteCat['name']
                    description = remoteCat['description']
                    category = datamodel.Category(name=name,
                        description=description)
                    self.model.append((name,\
                        apputils.ellipsize(description, 80), category))
        return False
    
    ### "private" methods ###
    def _loadData(self):
        categories = datamodel.Category.select(orderBy='name')
        onlyActive = self.ckbOnlyActive.get_active()
        for category in categories:
            if onlyActive and not category.isActive:
                continue
            name = category.name
            desc = apputils.ellipsize(category.description, 80)
            self.model.append((name, desc, category))
    
    def _getCategoryFromSelection(self):
        selection = self.categoryList.get_selection()
        model, selected = selection.get_selected()
        return model.get_value(selected, 2)
    
    def _enableActions(self):
        enableAction = len(self.model) > 0
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
        entryCount = len(category.entries)
        if entryCount == 0:
            self.controller.deleteCategory(category, self)
        else:
            apputils.error(_("There are %d entries related to this category,\n"
                "cann't delete.") % entryCount)
    
    ### signal handlers ###
    def _toggleShowActive(self, *args):
        self.model.clear()
        self._loadData()

    def on_lvCategory_button_press_event(self, *args):
        widget, event = args
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            category = self._getCategoryFromSelection()
            self.controller.editCategory(category, self)
        elif event.button == 3:
            self.listMenu.popup(None, None, None, event.button, event.time)
    
    def on_lvCategory_cursor_changed(self, *args):
        self._enableActions()
    
    def _synchronize(self, *args):
        blogs = datamodel.Weblog.select(datamodel.Weblog.q.isActive==True)
        for blog in blogs:
            thread = blogoper.CategorySynchronizerThread(blog, \
                blog.identity, self)
            thread.start()
    
    # custom signals for louie #
    def onDataChanged(self):
        self.model.clear()
        self._loadData()
