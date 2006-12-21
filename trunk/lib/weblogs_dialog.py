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

try:
    import louie
except ImportError:
    import louie_local as louie
import gtk, gobject
from sqlobject.sqlbuilder import *

import apputils, datamodel, transport
from appconst import DEBUG
from datamodel import Weblog
from appwindow import ListWindow

class WeblogsDialog(ListWindow):
    
    def __init__(self, controller):
        ListWindow.__init__(self, 'frmWeblogs', controller)
        self.lvBlogs = self.wTree.get_widget('lvBlogs')
        self.ckbOnlyActive = self.wTree.get_widget('ckbOnlyActive')
        self.cbxIdentity = self.wTree.get_widget('cbxIdentity')
        self.btnDiscover = self.wTree.get_widget('btnDiscover')
        self.btnAdd = self.wTree.get_widget('btnAdd')
        self.btnEdit = self.wTree.get_widget('btnEdit')
        self.btnDel = self.wTree.get_widget('btnDel')
        self._connectSignals()
    
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
            identModel = gtk.ListStore(str, gobject.TYPE_PYOBJECT)
            identities = datamodel.Identity.select(orderBy='name')
            identModel.append((_('All identities'), None))
            for identity in identities:
                identModel.append((identity.name, identity))
            self.cbxIdentity.set_model(identModel)
            cell = gtk.CellRendererText()
            self.cbxIdentity.pack_start(cell, True)
            self.cbxIdentity.add_attribute(cell, 'text', 0)
            self.cbxIdentity.set_active(0)
        finally:
            apputils.endWait(self.window)
        self.window.present()
    
    def _connectSignals(self):
        louie.connect(self.onDataChanged, 'discovery-done')
        louie.connect(self.onDataChanged, 'weblog-deleted')
        louie.connect(self.onDataChanged, 'weblog-changed')
    
    def _loadData(self, onlyActive=True, identity=None):
        if identity:
            if onlyActive:
                blogs = Weblog.select(
                    AND(
                        Weblog.q.isActive==True,
                        Weblog.q.identityID==identity.id
                    ),
                    orderBy='name'
                )
            else:
                blogs = Weblog.select(Weblog.q.identityID==identity.id,
                    orderBy='name')
        else:
            if onlyActive:
                blogs = Weblog.select(Weblog.q.isActive==True, orderBy='name')
            else:
                blogs = Weblog.select(orderBy='name')
        for blog in blogs:
            self.model.append((
                blog.name,
                blog.weblogID,
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
        if selected:
            return model.get_value(selected, 3)
    
    def _activateDiscovery(self, identity):
        if identity:
            hasDiscovery = 'discovery' in transport.FEATURES[identity.transportType]
        else:
            hasDiscovery = False
        activate = identity is not None and hasDiscovery
        self.btnDiscover.set_sensitive(activate)
    
    def _add(self, *args):
        self.controller.newWeblog(self)
    
    def _edit(self, *args):
        blog = self._getBlogFromSelection()
        self.controller.editWeblog(blog, self)
    
    def _del(self, *args):
        blog = self._getBlogFromSelection()
        self.controller.deleteWeblog(blog, self)

    ### signal handlers ###
    def on_lvBlogs_button_press_event(self, *args):
        widget, event = args
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            blog = self._getBlogFromSelection()
            self.controller.editWeblog(blog, self)
        elif event.button == 3:
            self.listMenu.popup(None, None, None, event.button, event.time)
    
    def on_ckbOnlyActive_toggled(self, *args):
        apputils.startWait(self.window)
        try:
            button = args[0]
            self.model.clear()
            model = self.cbxIdentity.get_model()
            identity = model.get_value(self.cbxIdentity.get_active_iter(), 1)
            self._loadData(button.get_active(), identity)
        finally:
            apputils.endWait(self.window)
    
    def on_cbxIdentity_changed(self, *args):
        apputils.startWait(self.window)
        try:
            comboBox = args[0]
            self.model.clear()
            model = comboBox.get_model()
            identity = model.get_value(comboBox.get_active_iter(), 1)
            self._activateDiscovery(identity)
            self._loadData(self.ckbOnlyActive.get_active(), identity)
        finally:
            apputils.endWait(self.window)
    
    def on_btnDiscover_clicked(self, *args):
        model = self.cbxIdentity.get_model()
        identity = model.get_value(self.cbxIdentity.get_active_iter(), 1)
        if identity:
            self.controller.discoverWeblogs(identity, self)
            self.model.clear()
            self._loadData(self.ckbOnlyActive.get_active(), identity)
    
    # custom signals for louie #
    def onDataChanged(self):
        self.model.clear()
        self._loadData()

