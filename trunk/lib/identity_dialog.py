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

"""Identity item editor"""

__revision__ = '$Id$'

import gtk

import datamodel, transport
from appwindow import EditDialog

PROTOCOLS = [
    'HTTP',
    'HTTPS',
    'XML-RPC',
    'XMPP/Jabber',
]

class IdentityDialog(EditDialog):
    
    def __init__(self, parent, identity=None):
        EditDialog.__init__(self, 'dlgIdentity', parent)
        self.identity = identity
        self.edName = self.wTree.get_widget('edName')
        self.cbxType = self.wTree.get_widget('cbxType')
        self.cbxProtocol = self.wTree.get_widget('cbxProtocol')
        self.edUri = self.wTree.get_widget('edUri')
        self.edPort = self.wTree.get_widget('edPort')
        self.ckbUseDefPort = self.wTree.get_widget('ckbUseDefPort')
        self.edLogin = self.wTree.get_widget('edLogin')
        self.edPassword = self.wTree.get_widget('edPassword')
        self.expAdvanced = self.wTree.get_widget('expAdvanced')
        self._initGui()
    
    def _initGui(self):
        typeModel = gtk.ListStore(str)
        for transportName in transport.AVAILABLE:
            typeModel.append([transportName])
        self.cbxType.set_model(typeModel)
        cell = gtk.CellRendererText()
        self.cbxType.pack_start(cell, True)
        self.cbxType.add_attribute(cell, 'text', 0)
        if self.identity:
            self.edName.set_text(self.identity.name)
            self.cbxType.set_active(transport.AVAILABLE.index(self.identity.transportType))
            self.cbxProtocol.set_active(PROTOCOLS.index(self.identity.serviceProtocol))
            self.edUri.set_text(self.identity.serviceURI)
            port = self.identity.servicePort
            self.ckbUseDefPort.set_active(port == 0)
            self.edPort.set_text(str(port))
            self.edLogin.set_text(self.identity.login)
            self.edPassword.set_text(self.identity.password)
            windowTitle = _('Editing identity "%s"') % self.identity.name
        else:
            windowTitle = _('Editing new identity')
        self.window.set_title(windowTitle)

    def run(self):
        ret = self.window.run()
        if ret == gtk.RESPONSE_OK:
            name = self.edName.get_text().decode('utf-8')
            model = self.cbxType.get_model()
            it = self.cbxType.get_active_iter()
            transportType = model.get_value(it, 0)
            model = self.cbxProtocol.get_model()
            it = self.cbxProtocol.get_active_iter()
            proto = model.get_value(it, 0)
            uri = self.edUri.get_text().decode('utf-8')
            useDefPort = self.ckbUseDefPort.get_active()
            if useDefPort:
                port = 0
            else:
                port = int(self.edPort.get_text())
            login = self.edLogin.get_text().decode('utf-8')
            password = self.edPassword.get_text().decode('utf-8')
            if self.identity:
                identity = self.identity
                identity.name = name
                identity.transportType = transportType
                identity.login = login
                identity.password = password
                identity.serviceProtocol = proto
                identity.serviceURI = uri
                identity.servicePort = port
            else:
                identity = datamodel.Identity(name=name,
                    transportType=transportType, login=login,
                    password=password, serviceURI = uri,
                    serviceProtocol=proto, servicePort=port)
            self.parent.notify('data-changed')
        self.window.destroy()
    
    ### signal handlers ###
    def on_cbxType_changed(self, *args):
        model = self.cbxType.get_model()
        transportName = model.get_value(self.cbxType.get_active_iter(), 0)
        if transportName in transport.AVAILABLE:
            transportClass = transport.TRANSPORTS[transportName]
            meta = transportClass.getMetadata()
            self.cbxProtocol.set_active(PROTOCOLS.index(meta['proto']))
            if meta['uri']:
                self.edUri.set_text(meta['uri'])
        features = transport.FEATURES[transportName]
        self.edLogin.set_sensitive('auth' in features)
        self.edPassword.set_sensitive('auth' in features)
    
    def on_ckbUseDefPort_toggled(self, *args):
        self.edPort.set_sensitive(not self.ckbUseDefPort.get_active())
