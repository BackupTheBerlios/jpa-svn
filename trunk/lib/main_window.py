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

"""Main window of application."""

__revision__ = '$Id$'

import gtk
import gtk.glade

import appconst

class MainWindow:
    
    def __init__(self, controller):
        self.controller = controller
        self.cfg = appconst.CFG
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, 'frmMain')
        self.wTree.signal_autoconnect(self)
    
    def on_miFileQuit_activate(self, *args):
        self.on_frmMain_delete(args)
    
    def on_frmMain_delete(self, *args):
        window = self.wTree.get_widget('frmMain')
        rect = window.get_size()
        self.cfg.setWindowSize('main', rect)
        self.on_frmMain_destroy(args)

    def on_frmMain_destroy(self, *args):
        gtk.main_quit()

    def on_miLicense_activate(self, *args):
        self.controller.showLicense()
