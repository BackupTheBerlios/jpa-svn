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

"""History of entry publications"""

__revision__ = '$Id$'

import gtk, gobject

import apputils
from appwindow import ListWindow

class PublicationHistoryDialog(ListWindow):
    
    def __init__(self, controller, entry):
        ListWindow.__init__(self, 'frmPubHistory', controller)
        self.entry = entry
        self.lvHistory = self.wTree.get_widget('lvHistory')
        self._setWidgets()
    
    def show(self):
        apputils.startWait(self.window)
        try:
            self.model = gtk.ListStore(str, str, gobject.TYPE_PYOBJECT)
            cells = (gtk.CellRendererText(), gtk.CellRendererText())
            columns = (gtk.TreeViewColumn(_('Publication date'), cells[0], text=0),
                gtk.TreeViewColumn(_('Weblog'), cells[1], text=1))
            for column in columns:
                self.lvHistory.append_column(column)
            self.lvHistory.set_model(self.model)
            self._loadData()
        finally:
            apputils.endWait(self.window)
        self.window.present()
    
    def _setWidgets(self):
        self.window.set_title(_('Publication history for entry "%s"') %\
            self.entry.title)
    
    def _loadData(self):
        for publication in self.entry.publications:
            self.model.append((
                publication.published.strftime('%Y-%m-%d %H:%M:%S'),
                publication.weblog.name,
                publication
            ))
