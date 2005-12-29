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

import os.path as op

import gtk, pango
import gtk.glade

import appconst, version, notifiable

class MainWindow(notifiable.Notifiable):
    
    registeredEvents = (
        'entry-changed',
        'entry-added',
        'entry-deleted',
        )
    
    def __init__(self, controller):
        self.controller = controller
        self.cfg = appconst.CFG
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, 'frmMain', 'jpa')
        self.wTree.signal_autoconnect(self)
        self.window = self.wTree.get_widget('frmMain')
        self.window.set_icon_from_file(op.join(appconst.PATHS['img'],
            'darkbeer.xpm'))
        self.window.set_title(version.PROGRAM)
        log = self.wTree.get_widget('txLog')
        logFontName = self.cfg.getOption('fonts', 'log', 'Monospace 10')
        log.modify_font(pango.FontDescription(logFontName))
        self.window.present()
    
    def notify(self, event):
        """
        Inherited from Notifiable.
        Any not registered event is silently ignored.
        """
        if not (event in self.registeredEvents):
            return
        if event == 'entry-changed':
            pass
        elif event == 'entry-added':
            pass
        elif event == 'entry-deleted':
            pass
    
    ### signal handlers ###
    def on_miFileQuit_activate(self, *args):
        self.on_frmMain_delete(args)
    
    def on_frmMain_delete(self, *args):
        rect = self.window.get_size()
        self.cfg.setWindowSize('main', rect)
        self.on_frmMain_destroy(args)

    def on_frmMain_destroy(self, *args):
        self.cfg.saveConfig()
        gtk.main_quit()
    
    def on_miFileNew_activate(self, *args):
        self.controller.newEntry(self)
    
    def on_miEditPrefs_activate(self, *args):
        self.controller.showPreferences(self)
    
    def on_miViewLog_activate(self, *args):
        logWindow = self.wTree.get_widget('pnLog')
        if logWindow.get_property('visible'):
            logWindow.hide()
        else:
            logWindow.show()

    def on_miAbout_activate(self, *args):
        self.controller.showAbout()

    def on_miToolsCategories_activate(self, *args):
        self.controller.showCategories()