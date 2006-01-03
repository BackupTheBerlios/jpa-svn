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

"""Dialog with application preferences"""

__revision__ = '$Id$'

import os.path as op

import gtk
import gtk.glade

import appconst

class PreferencesDialog:
    
    def __init__(self, parent):
        self.cfg = appconst.CFG
        self.wTree = gtk.glade.XML(appconst.GLADE_PATH, 'frmPrefs', 'jpa')
        self.window = self.wTree.get_widget('frmPrefs')
        if parent:
            self.window.set_transient_for(parent.window)
        self.window.set_icon_from_file(op.join(appconst.PATHS['img'],
            'darkbeer.xpm'))
        self.fbEditorFont = self.wTree.get_widget('fbEditorFont')
        self.fbPreviewFont = self.wTree.get_widget('fbPreviewFont')
        self.fbLogFont = self.wTree.get_widget('fbLogFont')
        self.ckbSaveWinSizes = self.wTree.get_widget('ckbSaveWindowSizes')
        self.ckbEnableAutosave = self.wTree.get_widget('ckbEnableAutosave')
        self.spnAutosaveInterval = self.wTree.get_widget('spnAutosaveInterval')
        self.wTree.signal_autoconnect(self)
    
    def show(self):
        self.fbEditorFont.set_font_name(self.cfg.getOption('fonts', 'editor',
            'Monospace 10'))
        self.fbPreviewFont.set_font_name(self.cfg.getOption('fonts', 'preview',
            'Sans 12'))
        self.fbLogFont.set_font_name(self.cfg.getOption('fonts', 'log',
            'Monospace 10'))
        self.ckbSaveWinSizes.set_active(self.cfg.getOption('windows',
            'save_sizes', '1') == '1')
        enableAutosave = (self.cfg.getOption('features',
            'enable_autosave', '1') == '1')
        self.ckbEnableAutosave.set_active(enableAutosave)
        self.spnAutosaveInterval.set_sensitive(enableAutosave)
        self.spnAutosaveInterval.set_value(int(self.cfg.getOption('features',
            'autosave_interval', '5')))
        self.window.present()
    
    ### signal handlers ###
    def on_ckbEnableAutosave_toggled(self, *args):
        isActive = self.ckbEnableAutosave.get_active()
        self.spnAutosaveInterval.set_sensitive(isActive)

    def on_btnCancel_clicked(self, *args):
        self.window.destroy()
    
    def on_btnOk_clicked(self, *args):
        self.cfg.setOption('fonts', 'editor',
            self.fbEditorFont.get_font_name())
        self.cfg.setOption('fonts', 'preview',
            self.fbPreviewFont.get_font_name())
        self.cfg.setOption('fonts', 'log',
            self.fbLogFont.get_font_name())
        if self.ckbSaveWinSizes.get_active():
            value = '1'
        else:
            value = '0'
        self.cfg.setOption('windows', 'save_sizes', value)
        if self.ckbEnableAutosave.get_active():
            value = '1'
        else:
            value = '0'
        self.cfg.setOption('features', 'enable_autosave', value)
        value = str(self.spnAutosaveInterval.get_value_as_int())
        self.cfg.setOption('features', 'autosave_interval', value)
        self.window.destroy()
