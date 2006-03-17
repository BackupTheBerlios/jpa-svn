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

import louie
import gtk, pango, gobject
import gtk.glade, gtk.gdk

import appconst, version, datamodel, apputils, blogoper, transport
from appconst import DEBUG



class MainWindow:
    
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
        self.logPanel = self.wTree.get_widget('pnLog')
        self.txLog = self.wTree.get_widget('txLog')
        self.logBuffer = self.txLog.get_buffer()
        self.lbCreated = self.wTree.get_widget('lbCreated')
        self.lbSent = self.wTree.get_widget('lbSent')
        self.lbTitle = self.wTree.get_widget('lbTitle')
        self.txEntry = self.wTree.get_widget('txEntry')
        self.miFileEdit = self.wTree.get_widget('miFileEdit')
        self.miFilePublish = self.wTree.get_widget('miFilePublish')
        self.miViewLog = self.wTree.get_widget('miViewLog')
        self.tbrMain = self.wTree.get_widget('tbrMain')
        self.tbnEdit = self.wTree.get_widget('tbnEdit')
        self.tbnSend = self.wTree.get_widget('tbnSend')
        self.lvEntries = self.wTree.get_widget('lvEntries')
        self.splVert = self.wTree.get_widget('splVert')
        self._setWidgets()
        self._setDisplaySettings()
        self._connectSignals()
        self.show()
    
    def _setWidgets(self):
        self.window.set_title(version.PROGRAM)
        self.window.set_icon_from_file(op.join(appconst.PATHS['img'],
            'darkbeer.xpm'))
        self.lbCreated.set_text('')
        self.lbSent.set_text('')
        self.lbTitle.set_text('')
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
        if (self.cfg.getOption('windows', 'save_sizes', '1') == '1'):
            pos = int(self.cfg.getOption('main', 'vsplit_pos', -1))
            if pos > 0:
                self.splVert.set_position(pos)
    
    def _setDisplaySettings(self):
        viewFontName = self.cfg.getOption('fonts', 'preview', 'Sans 10')
        self.txEntry.modify_font(pango.FontDescription(viewFontName))
        logFontName = self.cfg.getOption('fonts', 'log', 'Monospace 10')
        self.txLog.modify_font(pango.FontDescription(logFontName))
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

    def _connectSignals(self):
        louie.connect(self.onSettingsChanged, 'settings-changed')
        louie.connect(self.onEntryListChanged, 'entry-added')
        louie.connect(self.onEntryChanged, 'entry-changed')
        louie.connect(self.onEntryListChanged, 'entry-deleted')
        louie.connect(self.onEntryListChanged, 'filter-changed')
        louie.connect(self.updateStatus, 'update-status')
        louie.connect(self.onEntryPublish, 'entry-publish')
        louie.connect(self.onEntryRepublish, 'entry-republish')
    
    def show(self):
        self.window.present()
    
    def _refreshEntriesList(self, *args):
        self.loadEntriesList(self.entryFilter['year'],
            self.entryFilter['month'])
        if len(self.entriesModel) > 0:
            sel = self.lvEntries.get_selection()
            sel.select_path(0)
            self.displayEntry(self.getEntryFromSelection())

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
        if len(entry.publications) > 0:
            published = entry.publications[0].published.strftime('%Y-%m-%d %H:%M')
        else:
            published = ''
        self.lbSent.set_label(published)
        self.lbTitle.set_label(entry.title)
        bf = self.txEntry.get_buffer()
        bf.set_text(entry.body.encode('utf-8'))
    
    def activateActions(self, activate):
        self.miFileEdit.set_sensitive(activate)
        self.miFilePublish.set_sensitive(activate)
        self.tbnEdit.set_sensitive(activate)
        self.tbnSend.set_sensitive(activate)
    
    ### update entry ###
    def updateEntry(self, entry, blog, pubDate, assignedId):
        gobject.idle_add(self._updatePublishedEntry, entry, blog, pubDate, assignedId)
    
    def _updatePublishedEntry(self, entry, blog, pubDate, assignedId):
        entry.updatePublication(blog, pubDate, assignedId)
        return False

    ### update log window with status message ###
    def updateStatus(self, message):
        gobject.idle_add(self._addLogMessage, message)
    
    def _addLogMessage(self, message):
        buf = self.txLog.get_buffer()
        buf.insert(buf.get_end_iter(), message)
        buf.insert(buf.get_end_iter(), '\n')
        showLog = (self.cfg.getOption('views', 'show_log', '1') == '1')
        if showLog:
            self.logPanel.show_all()
            self.miViewLog.set_active(showLog)
        return False
    
    ### signal handlers ###
    def on_miFileQuit_activate(self, *args):
        self.on_frmMain_delete(args)
    
    def on_frmMain_delete(self, *args):
        rect = self.window.get_size()
        self.cfg.setWindowSize('main', rect)
        self.on_frmMain_destroy(args)

    def on_frmMain_destroy(self, *args):
        if (self.cfg.getOption('windows', 'save_sizes', '1') == '1'):
            pos = self.splVert.get_position()
            self.cfg.setOption('main', 'vsplit_pos', str(pos))
        self.cfg.saveConfig()
        gtk.main_quit()
    
    def _addEntry(self, *args):
        self.controller.newEntry()
    
    def _editEntry(self, *args):
        entry = self.getEntryFromSelection()
        self.controller.editEntry(entry)
    
    def _publishEntry(self, *args):
        self.controller.getPublishTo(self)
    
    def _republishEntry(self, *args):
        entry = self.getEntryFromSelection()
        self.controller.getRepublishTo(entry, self)
    
    def _deleteEntry(self, *args):
        entry = self.getEntryFromSelection()
        self.controller.deleteEntry(entry, self)
    
    def _showPubHistory(self, *args):
        entry = self.getEntryFromSelection()
        self.controller.showPubHistory(entry)
    
    def _saveEntry(self, *args):
        entry = self.getEntryFromSelection()
        self.controller.saveEntry(entry, self)
    
    def on_miEditPrefs_activate(self, *args):
        self.controller.showPreferences(self)
        
    def on_miViewFilter_activate(self, *args):
        self.controller.getEntryFilter(self)
    
    def on_miViewPreview_activate(self, *args):
        entry = self.getEntryFromSelection()
        self.controller.previewEntry(entry)
    
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
        self.controller.showCategories(self)
        
    def on_miToolsIdentities_activate(self, *args):
        self.controller.showIdentities()
    
    def on_miToolsWeblogs_activate(self, *args):
        self.controller.showWeblogs()
    
    def on_lvEntries_button_press_event(self, *args):
        widget, event = args
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            entry = self.getEntryFromSelection()
            self.controller.editEntry(entry)
        elif event.button == 3:
            self.pmEntryList.popup(None, None, None, event.button, event.time)

    def on_lvEntries_cursor_changed(self, *args):
        entry = self.getEntryFromSelection()
        if entry != self.curEntry:
            self.curEntry = entry
            self.displayEntry(entry)
    
    # custom signals for louie dispatcher #
    def onSettingsChanged(self):
        if DEBUG:
            print 'settings changed'
        self._setDisplaySettings()
    
    def onEntryListChanged(self):
        self._refreshEntriesList()
    
    def onEntryChanged(self):
        entry = self.getEntryFromSelection()
        self.displayEntry(entry)
        store, iterator = self.lvEntries.get_selection().get_selected()
        store.set_value(iterator, 1, apputils.ellipsize(entry.title, 30))
    
    def onEntryPublish(self, weblogs):
        if DEBUG:
            print 'publishing entry'
        entry = self.getEntryFromSelection()
        for blog in weblogs:
            service = blog.identity.transportType
            if (len(entry.categories) > 1) and \
                    ('category' in transport.FEATURES[service]):
                if DEBUG:
                    print 'too much categories, need to change this'
                self.controller.selectCategories(entry, service, self)
            else:
                categories = entry.categories
                sender = blogoper.BlogSenderThread(blog, entry, categories, self)
                if DEBUG:
                    print 'thread', sender.getName(), 'created'
                sender.start()
    
    def onEntryRepublish(self, weblogs):
        if DEBUG:
            print 'republishing entry'
        entry = self.getEntryFromSelection()
        for blog in weblogs:
            for publication in entry.publications:
                if publication.weblog.weblogID == blog.weblogID:
                    service = blog.identity.transportType
                    if (len(entry.categories) > 1) and \
                            ('category' in transport.FEATURES[service]):
                        controller.selectCategories(entry, service, self)
                    categories = entry.categories
                    thread = blogoper.EntryUpdaterThread(blog,
                        publication.assignedId, entry, categories, self)
                    if DEBUG:
                        print 'thread', thread.getName(), 'created'
                    thread.start()

