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
import datetime

import gtk, pango, gobject
import gtk.glade

import appconst, version, notifiable, datamodel

class MainWindow(notifiable.Notifiable):
    
    registeredEvents = (
        'entry-changed',
        'entry-added',
        'entry-deleted',
        'filter-changed',
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
        self.logPanel = self.wTree.get_widget('pnLog')
        self.logView = self.wTree.get_widget('txLog')
        logFontName = self.cfg.getOption('fonts', 'log', 'Monospace 10')
        self.logView.modify_font(pango.FontDescription(logFontName))
        self.lvEntries = self.wTree.get_widget('lvEntries')
        self.entriesModel = gtk.ListStore(str, str, gobject.TYPE_PYOBJECT)
        today = datetime.date.today()
        cell0 = gtk.CellRendererText()
        cell1 = gtk.CellRendererText()
        col0 = gtk.TreeViewColumn('date', cell0, text=0)
        col1 = gtk.TreeViewColumn('title', cell1, text=1)
        self.lvEntries.append_column(col0)
        self.lvEntries.append_column(col1)
        self.lvEntries.set_model(self.entriesModel)
        self.entryFilter={'year': today.year, 'month': today.month}
        self.loadEntriesList(today.year, today.month)
        self.window.present()
    
    def notify(self, event, *args, **kwargs):
        """
        Inherited from Notifiable.
        Any not registered event is silently ignored.
        """
        if not (event in self.registeredEvents):
            return
        if event == 'entry-changed':
            pass
        elif event == 'entry-added':
            self.loadEntriesList(self.entryFilter['year'],
                self.entryFilter['month'])
        elif event == 'entry-deleted':
            pass
        elif event == 'filter-changed':
            pass

    def loadEntriesList(self, year, month):
        self.entriesModel.clear()
        entries = datamodel.getEntriesList(year, month)
        for entry in entries:
            self.entriesModel.append((
                entry.created.strftime('%Y-%m-%d').encode('utf-8'),
                entry.title.encode('utf-8'),
                entry
            ))
    
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
        if self.logPanel.get_property('visible'):
            self.logPanel.hide()
        else:
            self.logPanel.show_all()

    def on_miAbout_activate(self, *args):
        self.controller.showAbout()

    def on_miToolsCategories_activate(self, *args):
        self.controller.showCategories()
