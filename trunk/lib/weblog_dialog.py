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

"""Weblog item editor"""

__revision__ = '$Id$'

import gtk, gobject

import datamodel, transport
from appwindow import EditWindow

class WeblogDialog(EditWindow):
    
    def __init__(self, parent, weblog=None):
        EditWindow.__init__(self, 'frmWeblog', parent)
        self.weblog = weblog
        self.edWeblogName = self.wTree.get_widget('edWeblogName')
        self.cbxIdentity = self.wTree.get_widget('cbxIdentity')
        self.edWeblogID = self.wTree.get_widget('edWeblogID')
        self.ckbActive = self.wTree.get_widget('ckbActive')
    
    def show(self):
        identModel = gtk.ListStore(str, gobject.TYPE_PYOBJECT)
        identities = datamodel.Identity.select(orderBy='name')
        self.identities = []
        for identity in identities:
            self.identities.append(identity.name)
            identModel.append((identity.name, identity))
        self.cbxIdentity.set_model(identModel)
        cell = gtk.CellRendererText()
        self.cbxIdentity.pack_start(cell, True)
        self.cbxIdentity.add_attribute(cell, 'text', 0)
        if len(identModel) > 0:
            self.cbxIdentity.set_active(0)
        if self.weblog:
            self.edWeblogName.set_text(self.weblog.name)
            self.cbxIdentity.set_active(self.identities.index(self.weblog.identity.name))
            self.edWeblogID.set_text(self.weblog.weblogID)
            self.ckbActive.set_active(self.weblog.isActive)
        self._activateFeatures()
        self.window.present()
    
    def _activateFeatures(self):
        model = self.cbxIdentity.get_model()
        identity = model.get_value(self.cbxIdentity.get_active_iter(), 1)
        features = transport.FEATURES[identity.transportType]
        self.edWeblogID.set_sensitive('blogID' in features)
    
    ### signal handlers ###
    def on_cbxIdentity_changed(self, *args):
        self._activateFeatures()
    
    def on_btnOk_clicked(self, *args):
        name = self.edWeblogName.get_text().decode('utf-8')
        model = self.cbxIdentity.get_model()
        identity = model.get_value(self.cbxIdentity.get_active_iter(), 1)
        blogID = self.edWeblogID.get_text().decode('utf-8')
        isActive = self.ckbActive.get_active()
        if self.weblog:
            self.weblog.name = name
            self.weblog.identity = identity
            self.weblog.weblogID = blogID
            self.weblog.isActive = isActive
        else:
            datamodel.Weblog(name=name, identity=identity, weblogID=blogID,
                isActive=isActive)
        self.parent.notify('data-changed')
        self.window.destroy()
