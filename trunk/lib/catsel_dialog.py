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

"""Category selection dialog"""

__revision__ = '$Id$'

from appwindow import EditWindow

class CategorySelectionDialog(EditWindow):
    
    info = _('You selected %(count)d categories, but %(service)s allows specifying only one.')
    
    def __init__(self, parent, entry, service):
        EditWindow.__init__(self, 'frmSelectCat', parent)
        self.lbInfo = self.wTree.get_widget('lbInfo')
        self.entry = entry
        self.service = service
    
    def show(self):
        count = len(self.entry.categories)
        service = self.service
        self.lbInfo.set_text(self.info % locals())
        self.window.present()
