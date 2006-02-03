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

"""List of user identities"""

__revision__ = '$Id$'

import gtk, gobject

import apputils, appconst, datamodel, transport
from datamodel import Identity
from appwindow import ListWindow

class IdentitiesDialog(ListWindow):
    
    def __init__(self, controller):
        ListWindow.__init__(self, 'frmIdentities', controller)
        self.menuTree = gtk.glade.XML(appconst.GLADE_PATH, 'pmIdentListEdit', 'jpa')
        self.menuTree.signal_autoconnect(self)
        self.listMenu = self.menuTree.get_widget('pmIdentListEdit')
        self.miDiscover = self.menuTree.get_widget('miDiscover')
        self.lvIdentities = self.wTree.get_widget('lvIdentities')
        self.btnAdd = self.wTree.get_widget('btnAdd')
        self.btnEdit = self.wTree.get_widget('btnEdit')
        self.btnDel = self.wTree.get_widget('btnDel')
    
    def show(self):
        apputils.startWait(self.window)
        try:
            self.model = gtk.ListStore(str, str, gobject.TYPE_PYOBJECT)
            cells = (gtk.CellRendererText(), gtk.CellRendererText())
            columns = (
                gtk.TreeViewColumn(_('Name'), cells[0], text=0),
                gtk.TreeViewColumn(_('Type'), cells[1], text=1)
            )
            for column in columns:
                self.lvIdentities.append_column(column)
            self.lvIdentities.set_model(self.model)
            self._loadData()
            if len(self.model) > 0:
                sel = self.lvIdentities.get_selection()
                sel.select_path(0)
            self._enableActions()
        finally:
            apputils.endWait(self.window)
        self.window.present()
    
    def notify(self, event, *args, **kwargs):
        if event == 'data-changed':
            apputils.startWait(self.window)
            try:
                self.model.clear()
                self._loadData()
            finally:
                apputils.endWait(self.window)
    
    def _loadData(self):
        identities = Identity.select(orderBy='name')
        for identity in identities:
            self.model.append((
                identity.name,
                identity.transportType,
                identity
            ))
    
    def _enableActions(self):
        enableAction = (len(self.model) > 0)
        self.miEdit.set_sensitive(enableAction)
        self.btnEdit.set_sensitive(enableAction)
        self.miDel.set_sensitive(enableAction)
        self.btnDel.set_sensitive(enableAction)
        if enableAction:
            identity = self._getIdentityFromSelection()
            features = transport.FEATURES[identity.transportType]
            self.miDiscover.set_sensitive('discovery' in features)
    
    def _getIdentityFromSelection(self):
        selection = self.lvIdentities.get_selection()
        model, selected = selection.get_selected()
        return model.get_value(selected, 2)
    
    def _add(self, *args):
        self.controller.newIdentity(self)
    
    def _edit(self, *args):
        identity = self._getIdentityFromSelection()
        self.controller.editIdentity(identity, self)

    ### signal handlers ###
    def on_lvIdentities_button_press_event(self, *args):
        widget, event = args
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            identity = self._getIdentityFromSelection()
            self.controller.editIdentity(identity, self)
        elif event.button == 3:
            self.listMenu.popup(None, None, None, event.button, event.time)

    def on_lvIdentities_cursor_changed(self, *args):
        self._enableActions()
    
    def on_miDiscover_activate(self, *args):
        identity = self._getIdentityFromSelection()
        self.controller.discoverWeblogs(identity, self)
