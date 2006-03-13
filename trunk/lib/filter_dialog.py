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

import datetime

import gtk

from appwindow import EditDialog

class FilterDialog(EditDialog):
    
    def __init__(self, parent):
        EditDialog.__init__(self, 'dlgFilter', parent)
        self._initGui()
    
    def _initGui(self):
        monthStore = gtk.ListStore(str)
        # stupid hack
        for i in range(12):
            monthStore.append((datetime.date(2005, i + 1, 1).strftime('%B'), ))
    
    def run(self):
        ret = self.window.run()
        self.window.destroy()