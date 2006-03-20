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

"""Entry filter selector"""

__revision__ = '$Id$'

import locale
import datetime

import gtk

from appwindow import EditDialog

class FilterDialog(EditDialog):
    
    def __init__(self, parent):
        EditDialog.__init__(self, 'dlgFilter', parent)
        self.cbxMonth = self.wTree.get_widget('cbxMonth')
        self._initGui()
    
    def _initGui(self):
        monthStore = gtk.ListStore(str)
        # stupid hack
        for i in range(12):
            monthStr = datetime.date(2005, i + 1, 1).strftime('%B')
            enc = locale.getdefaultlocale()[1]
            monthStore.append((monthStr.decode(enc), ))
        self.cbxMonth.set_model(monthStore)
        cell = gtk.CellRendererText()
        self.cbxMonth.pack_start(cell, True)
        self.cbxMonth.add_attribute(cell, 'text', 0)
        self.cbxMonth.set_active(0)
    
    def run(self):
        ret = self.window.run()
        self.window.destroy()