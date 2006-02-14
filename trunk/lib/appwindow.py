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

"""Generic application window class prototype"""

__revision__ = '$Id$'

import os.path as op

import gtk
import gtk.glade

import appconst, notifiable

class JPAWindow:
    """
    Generic window class
    """
    
    def __init__(self, windowName):
        self.cfg = appconst.CFG
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, windowName, 'jpa')
        self.window = self.wTree.get_widget(windowName)
        self.window.set_icon_from_file(op.join(appconst.PATHS['img'],
            'darkbeer.xpm'))        
        self.wTree.signal_autoconnect(self)


class ListWindow(JPAWindow, notifiable.Notifiable):
    """
    Generic non-modal window showing a list of items
    """
    
    def __init__(self, windowName, controller):
        JPAWindow.__init__(self, windowName)
        self.controller = controller
        self.menuTree = gtk.glade.XML(appconst.GLADE_PATH, 'pmListEdit', 'jpa')
        self.menuTree.signal_autoconnect(self)
        self.listMenu = self.menuTree.get_widget('pmListEdit')
        self.miAdd = self.menuTree.get_widget('miAdd')
        self.miEdit = self.menuTree.get_widget('miEdit')
        self.miDel = self.menuTree.get_widget('miDel')
        self.miClose = self.menuTree.get_widget('miClose')
    
    def _close(self, *args):
        self.window.destroy()

    # popup menu signals
    def on_miAdd_activate(self, *args):
        self._add(*args)
    
    def on_miEdit_activate(self, *args):
        self._edit(*args)
    
    def on_miDel_activate(self, *args):
        self._del(*args)
    
    def on_miClose_activate(self, *args):
        self._close(*args)


class EditWindow(JPAWindow):
    
    def __init__(self, windowName, parent):
        JPAWindow.__init__(self, windowName)
        self.parent = parent
        if parent:
            self.window.set_transient_for(parent.window)

    def on_btnCancel_clicked(self, *args):
        self.window.destroy()


class EditDialog:
    
    def __init__(self, windowName, parent=None):
        self.cfg = appconst.CFG
        self.parent = parent
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, windowName, 'jpa')
        self.window = self.wTree.get_widget(windowName)
        self.window.set_icon_from_file(op.join(appconst.PATHS['img'],
            'darkbeer.xpm'))        
        self.wTree.signal_autoconnect(self)
