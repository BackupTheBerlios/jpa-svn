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
import gtk.glade, gtk.gdk

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
        self.curEntry = None
        self.cfg = appconst.CFG
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, 'frmMain', 'jpa')
        self.wTree.signal_autoconnect(self)
        self.window = self.wTree.get_widget('frmMain')
        self.window.set_icon_from_file(op.join(appconst.PATHS['img'],
            'darkbeer.xpm'))
        self.window.set_title(version.PROGRAM)
        self.logPanel = self.wTree.get_widget('pnLog')
        self.logView = self.wTree.get_widget('txLog')
        self.lbCreated = self.wTree.get_widget('lbCreated')
        self.lbCreated.set_text('')
        self.lbSent = self.wTree.get_widget('lbSent')
        self.lbSent.set_text('')
        self.lbTitle = self.wTree.get_widget('lbTitle')
        self.lbTitle.set_text('')
        self.txEntry = self.wTree.get_widget('txEntry')
        logFontName = self.cfg.getOption('fonts', 'log', 'Monospace 10')
        self.logView.modify_font(pango.FontDescription(logFontName))
        self.miFileOpen = self.wTree.get_widget('miFileOpen')
        self.miFileOpen.set_sensitive(False)
        self.miFileSend = self.wTree.get_widget('miFileSend')
        self.miFileSend.set_sensitive(False)
        self.tbnOpen = self.wTree.get_widget('tbnOpen')
        self.tbnSend = self.wTree.get_widget('tbnSend')
        self.lvEntries = self.wTree.get_widget('lvEntries')
        self.entriesModel = gtk.ListStore(str, str, gobject.TYPE_PYOBJECT)
        today = datetime.date.today()
        cell0 = gtk.CellRendererText()
        cell1 = gtk.CellRendererText()
        col0 = gtk.TreeViewColumn(_('Date'), cell0, text=0)
        col1 = gtk.TreeViewColumn(_('Title'), cell1, text=1)
        self.lvEntries.append_column(col0)
        self.lvEntries.append_column(col1)
        self.lvEntries.set_model(self.entriesModel)
        self.entryFilter={'year': today.year, 'month': today.month}
        self.loadEntriesList(today.year, today.month)
        if len(self.entriesModel) > 0:
            sel = self.lvEntries.get_selection()
            sel.select_path(0)
            self.displayEntry(self.getEntryFromSelection())
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
            if len(self.entriesModel) > 0:
                sel = self.lvEntries.get_selection()
                sel.select_path(0)
                self.displayEntry(self.getEntryFromSelection())
        elif event == 'entry-deleted':
            pass
        elif event == 'filter-changed':
            self.loadEntriesList(self.entryFilter['year'],
                self.entryFilter['month'])

    def loadEntriesList(self, year, month):
        self.entriesModel.clear()
        entries = datamodel.getEntriesList(year, month)
        for entry in entries:
            self.entriesModel.append((
                entry.created.strftime('%Y-%m-%d').encode('utf-8'),
                entry.title.encode('utf-8'),
                entry
            ))
        self.activateActions(len(self.entriesModel) > 0)
    
    def getEntryFromSelection(self):
        store, iterator = self.lvEntries.get_selection().get_selected()
        return store.get_value(iterator, 2)

    def displayEntry(self, entry):
        self.lbCreated.set_label(entry.created.strftime('%Y-%m-%d %H:%M'))
        self.lbSent.set_label('')
        self.lbTitle.set_label(entry.title.encode('utf-8'))
        bf = self.txEntry.get_buffer()
        bf.set_text(entry.body.encode('utf-8'))
    
    def activateActions(self, activate):
        self.miFileOpen.set_sensitive(activate)
        self.miFileSend.set_sensitive(activate)
        self.tbnOpen.set_sensitive(activate)
        self.tbnSend.set_sensitive(activate)
    
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
    
    def on_miFileOpen_activate(self, *args):
        entry = self.getEntryFromSelection()
        self.controller.editEntry(entry)
    
    def on_miEditPrefs_activate(self, *args):
        self.controller.showPreferences(self)
    
    def on_miViewPreview_activate(self, *args):
        entry = self.getEntryFromSelection()
        self.controller.previewEntry(entry, self)
    
    def on_miViewHtml_activate(self, *args):
        entry = self.getEntryFromSelection()
        self.controller.showHtml(entry, self)
    
    def on_miViewLog_activate(self, *args):
        if self.logPanel.get_property('visible'):
            self.logPanel.hide()
        else:
            self.logPanel.show_all()

    def on_miAbout_activate(self, *args):
        self.controller.showAbout()

    def on_miToolsCategories_activate(self, *args):
        self.controller.showCategories()
        
    def on_miToolsIdentities_activate(self, *args):
        self.controller.showIdentities()
    
    def on_lvEntries_button_press_event(self, *args):
        widget, event = args
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            entry = self.getEntryFromSelection()
            self.controller.editEntry(entry)

    def on_lvEntries_cursor_changed(self, *args):
        entry = self.getEntryFromSelection()
        if entry != self.curEntry:
            self.curEntry = entry
            self.displayEntry(entry)
