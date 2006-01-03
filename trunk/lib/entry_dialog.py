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

import gtk, gobject, pango
import gtk.glade

import appconst, datamodel, apputils

class EntryDialog:
    
    def __init__(self, parent, entry=None):
        self.cfg = appconst.CFG
        self.modified = False
        self.entry = entry
        self.parent = parent
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, 'frmEntry', 'jpa')
        self.window = self.wTree.get_widget('frmEntry')
        self.window.set_icon_from_file(op.join(appconst.PATHS['img'],
            'darkbeer.xpm'))
        self.spnVisLevel = self.wTree.get_widget('spnVisLevel')
        self.lbVisLevelDesc = self.wTree.get_widget('lbVisLevelDesc')
        self.edTitle = self.wTree.get_widget('edTitle')
        self.txBody = self.wTree.get_widget('txBody')
        self.cbxContentType = self.wTree.get_widget('cbxContentType')
        self.ckbIsDraft = self.wTree.get_widget('ckbIsDraft')
        self.wTree.signal_autoconnect(self)
    
    def show(self):
        self._setWidgetProperties()
        self._loadCategories()
        if not self.entry:
            self.lbVisLevelDesc.set_label(_('public'))
        self.window.present()
    
    ### "private" methods ###
    def _setWidgetProperties(self):
        editorFontName = self.cfg.getOption('fonts', 'editor', 'Monospace 10')
        self.txBody.modify_font(pango.FontDescription(editorFontName))
        if self.entry:
            title = self.entry.title.encode('utf-8')
            self.window.set_title(_('Editing entry "%s"') % title)
            self.edTitle.set_text(title)
            bf = self.txBody.get_buffer()
            bf.set_text(self.entry.body.encode('utf-8'))
        else:
            self.window.set_title(_('Editing new entry'))
        expAdvanced = self.wTree.get_widget('expAdvanced')
        expAdvanced.set_expanded(False)
        self.cbxContentType.set_active(0)

    def _loadCategories(self):
        categoryList = self.wTree.get_widget('lvCategory')
        model = gtk.ListStore(bool, str)
        self.categories = datamodel.Category.select(orderBy='name')
        for category in self.categories:
            model.append((False, category.name.encode('utf-8')))
        cell0 = gtk.CellRendererToggle()
        cell0.set_property('radio', False)
        cell0.set_property('activatable', True)
        cell0.connect('toggled', self.on_lvCategory_toggle, model)
        column0 = gtk.TreeViewColumn('use', cell0, active=0)
        cell1 = gtk.CellRendererText()
        column1 = gtk.TreeViewColumn('name', cell1, text=1)
        categoryList.append_column(column0)
        categoryList.append_column(column1)
        categoryList.set_model(model)

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
        if self.parent:
            if self.entry:
                event = 'entry-changed'
            else:
                event = 'entry-added'
            self.parent.notify(event, self.entry)

    ### signal handlers ###
    def on_lvCategory_toggle(self, cell, path, model=None):
        iter = model.get_iter(path)
        model.set_value(iter, 0, not cell.get_active())
    
    def on_spnVisLevel_value_changed(self, *args):
        visLevel = self.spnVisLevel.get_value_as_int()
        if visLevel > 0:
            self.lbVisLevelDesc.set_label(_('private level %d') % visLevel)
        else:
            self.lbVisLevelDesc.set_label(_('public'))

    def on_btnCancel_clicked(self, *args):
        if self.modified:
            if apputils.question(_('Entry has been modified, do you want to save it?')):
                self._saveEntry()
            self.window.destroy()
        else:
            self.window.destroy()
    
    def on_btnOk_clicked(self, *args):
        self._saveEntry()
        self.window.destroy()
