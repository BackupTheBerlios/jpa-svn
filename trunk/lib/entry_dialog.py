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

import gtk
import gtk.glade

import appconst

class EntryDialog:
    
    def __init__(self, entryId):
        self.entryId = entryId
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, 'frmEntry')
        self.window = self.wTree.get_widget('frmEntry')
        self.wTree.signal_autoconnect(self)
        self.menuTree = gtk.glade.XML(appconst.GLADE_PATH, 'pmListEdit')
        self.catListPopup = self.menuTree.get_widget('pmListEdit')
    
    def show(self):
        if self.entryId:
            # load entry data
            pass
        self.window.show()
    
    def on_lvCategory_button_press(self, *args):
        widget, event = args
        if event.button == 3:
            self.catListPopup.popup(None, None, None, event.button, event.time)
