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

"""Blog data discovery"""

__revision__ = '$Id$'

import threading, Queue

import gtk, gobject
from sqlobject import SQLObjectNotFound

import transport, appconst
from datamodel import Weblog
from appwindow import EditWindow
from appconst import DEBUG

class DiscovererThread(threading.Thread):
    
    def __init__(self, transportObject, evtQueue):
        self.transport = transportObject
        self.queue = evtQueue
        threading.Thread.__init__(self)
    
    def run(self):
        blogs = self.transport.getBlogList()
        self.queue.put_nowait(blogs)


class WeblogDiscoveryDialog(EditWindow):
    
    def __init__(self, parent, identity):
        EditWindow.__init__(self, 'frmBlogDiscoDialog', parent)
        self.lvBlogs = self.wTree.get_widget('lvBlogs')
        self.identity = identity
        self.weblogs = {}
        self.queue = Queue.Queue()
        self.pbDisco = self.wTree.get_widget('pbDisco')
        self.idleTimer = gobject.idle_add(self._pulse)
    
    def show(self):
        self.model = gtk.ListStore(bool, str, str)
        cell0 = gtk.CellRendererToggle()
        cell0.set_property('radio', False)
        cell0.set_property('activatable', True)
        cell0.connect('toggled', self.on_lvBlogs_toggle, self.model)
        cells = (cell0, gtk.CellRendererText(), gtk.CellRendererText())
        columns = (
            gtk.TreeViewColumn(_('Update'), cells[0], active=0),
            gtk.TreeViewColumn(_('Name'), cells[1], text=1),
            gtk.TreeViewColumn(_('BlogID'), cells[2], text=2),
        )
        for column in columns:
            self.lvBlogs.append_column(column)
        self.lvBlogs.set_model(self.model)
        self.window.present()
        transClass = transport.TRANSPORTS[self.identity.transportType]
        login = self.identity.login
        passwd = self.identity.password
        proxy = self.cfg.getProxy()
        uri = self.identity.serviceURI
        transObj = transClass(login, passwd, proxy, uri)
        self.discoverer = DiscovererThread(transObj, self.queue)
        self.discoverer.start()
    
    def _pulse(self):
        try:
            self.weblogs = self.queue.get_nowait()
            if DEBUG:
                print self.weblogs
            self.pbDisco.set_fraction(0.0)
            self._fillList()
        except Queue.Empty:
            # ignore empty queue error
            pass
        if len(self.weblogs) == 0:
            self.pbDisco.pulse()
            return True
        return False
    
    def _fillList(self):
        self.model.clear()
        for (name, data) in self.weblogs.iteritems():
            self.model.append((True, name, data['blogID']))
    
    def _updateBlogData(self, blogName, blogID):
        try:
            blog = Weblog.byName(blogName)
            blog.weblogID = blogID
        except SQLObjectNotFound:
            blog = Weblog(name=blogName, identity=self.identity,
                weblogID=blogID)

    def on_lvBlogs_toggle(self, cell, path, model=None):
        iter = model.get_iter(path)
        model.set_value(iter, 0, not cell.get_active())
    
    def on_frmBlogDiscoDialog_delete_event(self, *args):
        gobject.source_remove(self.idleTimer)
    
    def on_btnCancel_clicked(self, *args):
        gobject.source_remove(self.idleTimer)
        EditWindow.on_btnCancel_clicked(self, *args)
    
    def on_btnOk_clicked(self, *args):
        gobject.source_remove(self.idleTimer)
        for (update, blogName, blogID) in self.model:
            if update:
                self._updateBlogData(blogName, blogID)
        self.window.destroy()
