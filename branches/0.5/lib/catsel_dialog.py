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

import gtk, gobject

from appwindow import EditWindow

class CategorySelectionDialog(EditWindow):
    
    info = _('You selected %(count)d categories, but %(service)s allows specifying only one.')
    
    def __init__(self, parent, entry, service):
        EditWindow.__init__(self, 'frmSelectCat', parent)
        self.lbInfo = self.wTree.get_widget('lbInfo')
        self.lvCategories = self.wTree.get_widget('lvCategories')
        self.entry = entry
        self.service = service
    
    def show(self):
        count = len(self.entry.categories)
        service = self.service
        self.lbInfo.set_text(self.info % locals())
        self.model = gtk.ListStore(bool, str, gobject.TYPE_PYOBJECT)
        cell0 = gtk.CellRendererToggle()
        cell0.set_property('radio', False)
        cell0.set_property('activatable', True)
        cell0.connect('toggled', self.on_lvCategories_toggle, self.model)
        cells = (cell0, gtk.CellRendererText())
        columns = (
            gtk.TreeViewColumn(_('Select'), cells[0], active=0),
            gtk.TreeViewColumn(_('Category name'), cells[1], text=1),
        )
        for column in columns:
            self.lvCategories.append_column(column)
        self.lvCategories.set_model(self.model)
        self._fillList()
        self.window.present()
    
    def _fillList(self):
        self.model.clear()
        for category in self.entry.categories:
            self.model.append((
                True,
                category.name,
                category,
            ))
    
    ### signal handlers ###
    def on_lvCategories_toggle(self, cell, path, model=None):
        iter = model.get_iter(path)
        model.set_value(iter, 0, not cell.get_active())
    
    def on_btnOk_clicked(self, *args):
        for (select, name, category) in self.model:
            if not select:
                self.entry.removeCategory(category)
        self.window.destroy()
