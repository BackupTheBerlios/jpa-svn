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

import os, os.path as op
import datetime

import gtk, pango, gobject
import gtk.glade, gtk.gdk

import appconst, version, notifiable, datamodel, apputils

class MainWindow(notifiable.Notifiable):
    
    registeredEvents = (
        'entry-changed',
        'entry-added',
        'entry-deleted',
        'filter-changed',
        'publish-entry',
        )
    
    def __init__(self, controller):
        self.controller = controller
        self.curEntry = None
        self.cfg = appconst.CFG
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, 'frmMain', 'jpa')
        self.wTree.signal_autoconnect(self)
        self.window = self.wTree.get_widget('frmMain')
        listMenuTree = gtk.glade.XML(appconst.GLADE_PATH, 'pmEntryList', 'jpa')
        listMenuTree.signal_autoconnect(self)
        self.pmEntryList = listMenuTree.get_widget('pmEntryList')
        self.window.set_title(version.PROGRAM)
        self.logPanel = self.wTree.get_widget('pnLog')
        self.logView = self.wTree.get_widget('txLog')
        self.lbCreated = self.wTree.get_widget('lbCreated')
        self.lbSent = self.wTree.get_widget('lbSent')
        self.lbTitle = self.wTree.get_widget('lbTitle')
        self.txEntry = self.wTree.get_widget('txEntry')
        self.miFileEdit = self.wTree.get_widget('miFileEdit')
        self.miFilePublish = self.wTree.get_widget('miFilePublish')
        self.tbrMain = self.wTree.get_widget('tbrMain')
        self.tbnEdit = self.wTree.get_widget('tbnEdit')
        self.tbnSend = self.wTree.get_widget('tbnSend')
        self.lvEntries = self.wTree.get_widget('lvEntries')
        self._setWidgets()
        self.show()
    
    def _setWidgets(self):
        self.window.set_icon_from_file(op.join(appconst.PATHS['img'],
            'darkbeer.xpm'))
        self.lbCreated.set_text('')
        self.lbSent.set_text('')
        self.lbTitle.set_text('')
        viewFontName = self.cfg.getOption('fonts', 'preview', 'Sans 10')
        self.txEntry.modify_font(pango.FontDescription(viewFontName))
        logFontName = self.cfg.getOption('fonts', 'log', 'Monospace 10')
        self.logView.modify_font(pango.FontDescription(logFontName))
        if os.name == 'nt':
            toolbarStyle = self.cfg.getOption('toolbars', 'style', 'icons')
        else:
            toolbarStyle = self.cfg.getOption('toolbars', 'style', 'both')
        if toolbarStyle == 'both':
            gtkStyle = gtk.TOOLBAR_BOTH
        elif toolbarStyle == 'icons':
            gtkStyle = gtk.TOOLBAR_ICONS
        elif toolbarStyle == 'labels':
            gtkStyle = gtk.TOOLBAR_TEXT
        self.tbrMain.set_style(gtkStyle)
        self.activateActions(False)
        self.entriesModel = gtk.ListStore(str, str, gobject.TYPE_PYOBJECT)
        today = datetime.date.today()
        cell0 = gtk.CellRendererText()
        cell1 = gtk.CellRendererText()
        col0 = gtk.TreeViewColumn(_('Created'), cell0, text=0)
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
    
    def show(self):
        self.window.present()
    
    def notify(self, event, *args, **kwargs):
        """
        Inherited from Notifiable.
        Any not registered event is silently ignored.
        """
        if not (event in self.registeredEvents):
            return
        if event == 'entry-changed':
            entry = self.getEntryFromSelection()
            self.displayEntry(entry)
            store, iterator = self.lvEntries.get_selection().get_selected()
            store.set_value(iterator, 1, apputils.ellipsize(entry.title, 30))
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
        elif event == 'publish-entry':
            entry = self.getEntryFromSelection()
            blogs = args[0]
            if len(blogs) > 0:
                self.controller.publishEntry(entry, blogs)

    def loadEntriesList(self, year, month):
        self.entriesModel.clear()
        entries = datamodel.getEntriesList(year, month)
        for entry in entries:
            self.entriesModel.append((
                entry.created.strftime('%Y-%m-%d'),
                apputils.ellipsize(entry.title, 30),
                entry
            ))
        self.activateActions(len(self.entriesModel) > 0)
    
    def getEntryFromSelection(self):
        store, iterator = self.lvEntries.get_selection().get_selected()
        return store.get_value(iterator, 2)

    def displayEntry(self, entry):
        self.lbCreated.set_label(entry.created.strftime('%Y-%m-%d %H:%M'))
        self.lbSent.set_label('')
        self.lbTitle.set_label(entry.title)
        bf = self.txEntry.get_buffer()
        bf.set_text(entry.body)
    
    def activateActions(self, activate):
        self.miFileEdit.set_sensitive(activate)
        self.miFilePublish.set_sensitive(activate)
        self.tbnEdit.set_sensitive(activate)
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
    
    def _addEntry(self, *args):
        self.controller.newEntry(self)
    
    def _editEntry(self, *args):
        entry = self.getEntryFromSelection()
        self.controller.editEntry(entry, self)
    
    def _publishEntry(self, *args):
        self.controller.getPublishTo(self)
    
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
        self.controller.showAbout(self)

    def on_miToolsCategories_activate(self, *args):
        self.controller.showCategories()
        
    def on_miToolsIdentities_activate(self, *args):
        self.controller.showIdentities()
    
    def on_miToolsWeblogs_activate(self, *args):
        self.controller.showWeblogs()
    
    def on_lvEntries_button_press_event(self, *args):
        widget, event = args
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            entry = self.getEntryFromSelection()
            self.controller.editEntry(entry, self)
        elif event.button == 3:
            self.pmEntryList.popup(None, None, None, event.button, event.time)

    def on_lvEntries_cursor_changed(self, *args):
        entry = self.getEntryFromSelection()
        if entry != self.curEntry:
            self.curEntry = entry
            self.displayEntry(entry)
