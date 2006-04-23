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

"""Dialog for entry editing"""

__revision__ = '$Id$'

import os.path as op

import louie
import gtk, gobject, pango
import gtk.glade

import appconst, datamodel, apputils

class EntryDialog:
    
    def __init__(self, entry=None, parent=None):
        self.cfg = appconst.CFG
        self.modified = False
        self.isNew = (entry is None)
        self.entry = entry
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, 'frmEntry', 'jpa')
        self.window = self.wTree.get_widget('frmEntry')
        self.window.set_icon_from_file(op.join(appconst.PATHS['img'],
            'darkbeer.xpm'))
        if parent:
            self.window.set_transient_for(parent.window)
        self.spnVisLevel = self.wTree.get_widget('spnVisLevel')
        self.lbVisLevelDesc = self.wTree.get_widget('lbVisLevelDesc')
        self.edTitle = self.wTree.get_widget('edTitle')
        self.txBody = self.wTree.get_widget('txBody')
        self.cbxContentType = self.wTree.get_widget('cbxContentType')
        self.ckbIsDraft = self.wTree.get_widget('ckbIsDraft')
        self.lvCategory = self.wTree.get_widget('lvCategory')
        self.wTree.signal_autoconnect(self)
    
    def show(self):
        self._loadCategories()
        self._setWidgetProperties()
        if self.cfg.getOption('features', 'enable_autosave', '1') == '1':
            interval = int(self.cfg.getOption('features', 
                'autosave_interval', '5')) * 60 * 1000
            self.autosaveTimer = gobject.timeout_add(interval, self.autosave)
        self.window.present()
    
    ### "private" methods ###
    def _setWidgetProperties(self):
        editorFontName = self.cfg.getOption('fonts', 'editor', 'Monospace 10')
        self.txBody.modify_font(pango.FontDescription(editorFontName))
        model = gtk.ListStore(str)
        for bodyType in datamodel.BODY_TYPES:
            model.append((bodyType, ))
        self.cbxContentType.set_model(model)
        if self.entry:
            title = self.entry.title
            self.window.set_title(_('Editing entry "%s"') % title)
            self.edTitle.set_text(title)
            bf = self.txBody.get_buffer()
            bf.set_text(self.entry.body)
            self.spnVisLevel.set_value(self.entry.visibilityLevel)
            self.ckbIsDraft.set_active(self.entry.isDraft)
            self.cbxContentType.set_active(datamodel.BODY_TYPES.index(self.entry.bodyType))
            model = self.lvCategory.get_model()
            for categoryItem in model:
                active, name = categoryItem
                for entryCategory in self.entry.categories:
                    if entryCategory.name == name:
                        categoryItem[0] = True
        else:
            self.window.set_title(_('Editing new entry'))
            self.lbVisLevelDesc.set_label(_('public'))
            self.cbxContentType.set_active(0)
            bodyType = self.cfg.getOption('editing', 'def_body_type', 'textile')
            self.cbxContentType.set_active(datamodel.BODY_TYPES.index(bodyType))
            model = self.lvCategory.get_model()
            defaultCats = self.cfg.getOption('editing', 'def_categories', '').split(',')
            for categoryItem in model:
                categoryItem[0] = categoryItem[1] in defaultCats
        expAdvanced = self.wTree.get_widget('expAdvanced')
        expAdvanced.set_expanded(False)

    def _loadCategories(self):
        model = gtk.ListStore(bool, str)
        self.categories = datamodel.Category.select(orderBy='name')
        for category in self.categories:
            model.append((False, category.name))
        cell0 = gtk.CellRendererToggle()
        cell0.set_property('radio', False)
        cell0.set_property('activatable', True)
        cell0.connect('toggled', self.on_lvCategory_toggle, model)
        column0 = gtk.TreeViewColumn('use', cell0, active=0)
        cell1 = gtk.CellRendererText()
        column1 = gtk.TreeViewColumn('name', cell1, text=1)
        self.lvCategory.append_column(column0)
        self.lvCategory.append_column(column1)
        self.lvCategory.set_model(model)

    def _saveEntry(self):
        title = self.edTitle.get_text().decode('utf-8')
        bf = self.txBody.get_buffer()
        body = bf.get_text(bf.get_start_iter(), 
            bf.get_end_iter()).decode('utf-8')
        bodyType = datamodel.BODY_TYPES[self.cbxContentType.get_active()]
        isDraft = self.ckbIsDraft.get_active()
        visibilityLevel = self.spnVisLevel.get_value_as_int()
        categories = []
        categoryList = self.wTree.get_widget('lvCategory')
        model = categoryList.get_model()
        for category in model:
            categories.append((
                category[0], 
                datamodel.Category.byName(category[1].decode('utf-8'))
            ))
        if self.entry:
            entry = self.entry
            entry.title = title
            entry.body = body
        else:
            entry = datamodel.Entry(title=title, body=body)
        for category in categories:
            if category[1] in entry.categories:
                if not category[0]:
                    entry.removeCategory(category[1])
            else:
                if category[0] and (not category[1] in entry.categories):
                    entry.addCategory(category[1])
        entry.bodyType = bodyType
        entry.visibilityLevel = visibilityLevel
        entry.isDraft = isDraft
        self.entry = entry

    ### signal handlers ###
    def autosave(self):
        self._saveEntry()
        return True
    
    def on_edTitle_changed(self, *args):
        widget = args[0]
        title = widget.get_text()
        self.window.set_title(_('Editing entry "%s"') % title)
    
    def on_lvCategory_toggle(self, cell, path, model=None):
        iter = model.get_iter(path)
        model.set_value(iter, 0, not cell.get_active())
    
    def on_spnVisLevel_value_changed(self, *args):
        widget = args[0]
        visLevel = widget.get_value_as_int()
        if visLevel > 0:
            self.lbVisLevelDesc.set_label(_('private level %d') % visLevel)
        else:
            self.lbVisLevelDesc.set_label(_('public'))
    
    def on_frmEntry_delete_event(self, *args):
        gobject.source_remove(self.autosaveTimer)

    def on_btnCancel_clicked(self, *args):
        gobject.source_remove(self.autosaveTimer)
        if self.isNew and self.entry:
            self.entry.destroySelf()
        self.window.destroy()
    
    def on_btnOk_clicked(self, *args):
        gobject.source_remove(self.autosaveTimer)
        self._saveEntry()
        if self.isNew:
            event = 'entry-added'
        else:
            event = 'entry-changed'
        louie.send(event)
        self.window.destroy()
