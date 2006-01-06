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

import datamodel
from appwindow import EditWindow

class IdentityDialog(EditWindow):
    
    def __init__(self, parent, identity=None):
        EditWindow.__init__(self, 'frmIdentity', parent)
        self.identity = identity
        self.edName = self.wTree.get_widget('edName')
        self.cbxType = self.wTree.get_widget('cbxType')
        self.cbxProtocol = self.wTree.get_widget('cbxProtocol')
        self.edUri = self.wTree.get_widget('edUri')
        self.edPort = self.wTree.get_widget('edPort')
        self.edLogin = self.wTree.get_widget('edLogin')
        self.edPassword = self.wTree.get_widget('edPassword')
    
    def show(self):
        if self.identity:
            pass
        self.window.present()
