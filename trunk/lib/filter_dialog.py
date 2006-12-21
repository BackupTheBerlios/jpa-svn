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

try:
    import louie
except ImportError:
    import louie_local as louie
import gtk

import datamodel
from appwindow import EditDialog
from appconst import DEBUG

class FilterDialog(EditDialog):

    def __init__(self, parent, curFilter={}):
        EditDialog.__init__(self, 'dlgFilter', parent)
        if DEBUG:
            print 'modal:', self.window.get_modal()
        self.curFilter = curFilter
        self.cbxMonth = self.wTree.get_widget('cbxMonth')
        self.lvCategories = self.wTree.get_widget('lvCategories')
        self.ckbShowAllCategories = self.wTree.get_widget('ckbShowAllCategories')
        self.spnYear = self.wTree.get_widget('spnYear')
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
        if not self.curFilter:
            today = datetime.date.today()
            self.curFilter['month'] = today.month
            self.curFilter['year'] = today.year
            self.curFilter['categories'] = []
        self.cbxMonth.set_active(self.curFilter['month'] - 1)
        self.spnYear.set_value(self.curFilter['year'])
        catStore = gtk.ListStore(bool, str)
        categories = datamodel.Category.select(orderBy='name')
        for category in categories:
            active = category.name in self.curFilter['categories']
            catStore.append((active, category.name))
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
        if ret == gtk.RESPONSE_OK:
            if DEBUG:
                print 'pressed ok, sending signal'
            self.curFilter['month'] = self.cbxMonth.get_active() + 1
            self.curFilter['year'] = int(self.spnYear.get_value())
            if self.ckbShowAllCategories.get_active():
                self.curFilter['categories'] = []
            else:
                for (selected, name) in self.lvCategories.get_model():
                    if selected:
                        self.curFilter['categories'].append(name.decode('utf-8'))
            louie.send('filter-changed')
        self.window.destroy()

    ### signal handlers ###
    def on_lvCategories_toggle(self, cell, path, model=None):
        it = model.get_iter(path)
        model.set_value(it, 0, not cell.get_active())

    def on_ckbShowAllCategories_toggled(self, *args):
        button = args[0]
        self.lvCategories.set_sensitive(not button.get_active())
