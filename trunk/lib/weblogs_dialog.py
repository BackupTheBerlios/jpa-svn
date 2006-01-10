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

"""List of user weblogs"""

__revision__ = '$Id$'

import gtk, gobject

import apputils, datamodel
from datamodel import Weblog
from appwindow import ListWindow

class WeblogsDialog(ListWindow):
    
    def __init__(self, controller):
        ListWindow.__init__(self, 'frmWeblogs', controller)
        self.lvBlogs = self.wTree.get_widget('lvBlogs')
        self.ckbOnlyActive = self.wTree.get_widget('ckbOnlyActive')
        self.btnAdd = self.wTree.get_widget('btnAdd')
        self.btnEdit = self.wTree.get_widget('btnEdit')
        self.btnDel = self.wTree.get_widget('btnDel')
    
    def show(self):
        apputils.startWait(self.window)
        try:
            self.model = gtk.ListStore(str, str, str, gobject.TYPE_PYOBJECT)
            cells = (gtk.CellRendererText(), 
                gtk.CellRendererText(), 
                gtk.CellRendererText())
            columns = (
                gtk.TreeViewColumn(_('Name'), cells[0], text=0),
                gtk.TreeViewColumn(_('BlogID'), cells[1], text=1),
                gtk.TreeViewColumn(_('Active'), cells[2], text=2),
            )
            for column in columns:
                self.lvBlogs.append_column(column)
            self.lvBlogs.set_model(self.model)
            self._loadData(onlyActive=True)
            if len(self.model) > 0:
                sel = self.lvBlogs.get_selection()
                sel.select_path(0)
            self._enableActions()
        finally:
            apputils.endWait(self.window)
        self.window.present()
    
    def _loadData(self, onlyActive=True):
        if onlyActive:
            blogs = Weblog.select(Weblog.q.isActive==True, 
                orderBy='name')
        else:
            blogs = Weblog.select(orderBy='name')
        for blog in blogs:
            self.model.append((
                blog.name,
                blog.weblogId,
                str(blog.isActive),
                blog
            ))
    
    def _enableActions(self):
        enableAction = (len(self.model) > 0)
        self.miEdit.set_sensitive(enableAction)
        self.btnEdit.set_sensitive(enableAction)
        self.miDel.set_sensitive(enableAction)
        self.btnDel.set_sensitive(enableAction)

    def _getBlogFromSelection(self):
        selection = self.lvBlogs.get_selection()
        model, selected = selection.get_selected()
        return model.get_value(selected, 3)
    
    def _add(self, *args):
        pass
    
    def _edit(self, *args):
        blog = self._getBlogFromSelection()
    
    def _del(self, *args):
        blog = self._getBlogFromSelection()

    ### signal handlers ###
    def on_lvBlogs_button_press_event(self, *args):
        widget, event = args
        if event.button == 3:
            self.listMenu.popup(None, None, None, event.button, event.time)
    
    def on_ckbOnlyActive_toggled(self, *args):
        apputils.startWait(self.window)
        try:
            self._loadData(self.ckbOnlyActive.get_active())
        finally:
            apputils.endWait(self.window)
