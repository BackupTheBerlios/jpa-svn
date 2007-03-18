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

"""List of published media files"""

__revision__ = '$Id$'

import gtk, gobject

from datamodel import Media
from appwindow import ListWindow

class MediafilesDialog(ListWindow):

    def __init__(self, controller):
        ListWindow.__init__(self, 'frmMedia', controller)
        self.lvMedia = self.wTree.get_widget('lvMedia')

    def show(self):
        self.model = gtk.ListStore(str, str, str, gobject.TYPE_PYOBJECT)
        cells = (gtk.CellRendererText(),
            gtk.CellRendererText(),
            gtk.CellRendererText())
        columns = (
            gtk.TreeViewColumn(_('Name'), cells[0], text=0),
            gtk.TreeViewColumn(_('MIME Type'), cells[1], text=1),
            gtk.TreeViewColumn(_('URL'), cells[2], text=2),
        )
        for column in columns:
            self.lvMedia.append_column(column)
        self.lvMedia.set_model(self.model)
        self._loadData()
        if len(self.model) > 0:
            sel = self.lvMedia.get_selection()
            sel.select_path(0)
        self.window.present()

    def _loadData(self):
        mediaObjs = Media.select(orderBy='name')
        for media in mediaObjs:
            self.model.append((
                media.name,
                media.mime,
                media.URI,
                media
            ))

