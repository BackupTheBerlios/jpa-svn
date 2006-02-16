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

"""Entry/post deletion dialog"""

__revision__ = '$Id$'

import louie
import gtk, gobject

from appwindow import EditWindow

class EntryDeletionDialog(EditWindow):
    
    def __init__(self, parent, entry):
        EditWindow.__init__(self, 'frmDeleteEntry', parent)
        self.entry = entry
        self.lvBlogs = self.wTree.get_widget('lvBlogs')
    
    def show(self):
        self.model = gtk.ListStore(bool, str, str, gobject.TYPE_PYOBJECT)
        cell0 = gtk.CellRendererToggle()
        cell0.set_property('radio', False)
        cell0.set_property('activatable', True)
        cell0.connect('toggled', self.on_lvBlogs_toggle, self.model)
        cells = (cell0, gtk.CellRendererText(), gtk.CellRendererText())
        columns = (
            gtk.TreeViewColumn(_('Delete'), cells[0], active=0),
            gtk.TreeViewColumn(_('Publication date'), cells[1], text=1),
            gtk.TreeViewColumn(_('Weblog name'), cells[2], text=2),
        )
        for column in columns:
            self.lvBlogs.append_column(column)
        self.lvBlogs.set_model(self.model)
        self._fillList()
        self.window.present()
    
    def _fillList(self):
        self.model.clear()
        for publication in self.entry.publications:
            self.model.append((
                False, 
                publication.published.strftime('%Y-%m-%d %H:%M:%S'),
                publication.weblog.name,
                publication,
            ))
    
    ### event handlers ###
    def on_lvBlogs_toggle(self, cell, path, model=None):
        iter = model.get_iter(path)
        model.set_value(iter, 0, not cell.get_active())
    
    def on_btnOk_clicked(self, *args):
        publications = []
        for (delete, pubDate, blogName, publication) in self.model:
            if delete:
                publications.append(publication)
        louie.send('entry-delete', publications)
        self.window.destroy()