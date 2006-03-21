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

import datamodel
from appwindow import EditDialog

class FilterDialog(EditDialog):
    
    def __init__(self, parent, curFilter={}):
        EditDialog.__init__(self, 'dlgFilter', parent)
        self.curFilter = curFilter
        self.cbxMonth = self.wTree.get_widget('cbxMonth')
        self.lvCategories = self.wTree.get_widget('lvCategories')
        self.ckbShowAllCategories = self.wTree.get_widget('ckbShowAllCategories')
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
        catStore = gtk.ListStore(bool, str)
        categories = datamodel.Category.select(orderBy='name')
        for category in categories:
            catStore.append((False, category.name))
        cell0 = gtk.CellRendererToggle()
        cell0.set_property('radio', False)
        cell0.set_property('activatable', True)
        cell0.connect('toggled', self.on_lvCategories_toggle, catStore)
        column0 = gtk.TreeViewColumn('use', cell0, active=0)
        cell1 = gtk.CellRendererText()
        column1 = gtk.TreeViewColumn('name', cell1, text=1)
        self.lvCategories.append_column(column0)
        self.lvCategories.append_column(column1)
        self.lvCategories.set_model(catStore)        
    
    def run(self):
        ret = self.window.run()
        self.window.destroy()
    
    ### signal handlers ###
    def on_lvCategories_toggle(self, cell, path, model=None):
        iter = model.get_iter(path)
        model.set_value(iter, 0, not cell.get_active())

    def on_ckbShowAllCategories_toggled(self, *args):
        self.lvCategories.set_sensitive(not self.ckbShowAllCategories.get_active())