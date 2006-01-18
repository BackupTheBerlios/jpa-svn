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

import os, os.path as op

import gtk
import gtk.glade

import appconst, datamodel

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
        self.rbnUseSysDefBrowser = self.wTree.get_widget('rbnUseSysDef')
        self.rbnUseGnomeDefBrowser = self.wTree.get_widget('rbnUseGnomeDef')
        self.rbnUseKdeDefBrowser = self.wTree.get_widget('rbnUseKdeDef')
        self.rbnUseCustomBrowser = self.wTree.get_widget('rbnUseCustom')
        self.edBrowserCmd = self.wTree.get_widget('edBrowserCmd')
        self.fcbSelectBrowser = self.wTree.get_widget('fcbSelectBrowser')
        self.ckbUseProxy = self.wTree.get_widget('ckbUseProxy')
        self.edProxyHost = self.wTree.get_widget('edProxyHost')
        self.edProxyPort = self.wTree.get_widget('edProxyPort')
        self.cbxDefBodyType = self.wTree.get_widget('cbxDefBodyType')
        self.rbnIconsAndLabels = self.wTree.get_widget('rbnIconsAndLabels')
        self.rbnIconsOnly = self.wTree.get_widget('rbnIconsOnly')
        self.rbnLabelsOnly = self.wTree.get_widget('rbnLabelsOnly')
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
        browser = self.cfg.getOption('features', 'browser', 'system')
        if browser == 'system':
            self.rbnUseSysDefBrowser.set_active(True)
        elif browser == 'gnome':
            self.rbnUseGnomeDefBrowser.set_active(True)
        elif browser == 'kde':
            self.rbnUseKdeDefBrowser.set_active(True)
        else:
            self.rbnUseCustomBrowser.set_active(True)
        if browser == 'custom':
            browserCmd = self.cfg.getOption('features', 'browser_cmd', '')
            self.edBrowserCmd.set_text(browserCmd)
            self._enableCustomBrowserSelection(True)
        else:
            self._enableCustomBrowserSelection(False)
        if os.name == 'nt':
            # disable linux-specific buttons
            self.rbnUseGnomeDefBrowser.set_sensitive(False)
            self.rbnUseKdeDefBrowser.set_sensitive(False)
        useProxy = (self.cfg.getOption('network', 'use_proxy', '0') == '1')
        proxyHost = self.cfg.getOption('network', 'proxy_host', '')
        proxyPort = self.cfg.getOption('network', 'proxy_port', '0')
        self.ckbUseProxy.set_active(useProxy)
        self.edProxyHost.set_text(proxyHost)
        self.edProxyPort.set_text(proxyPort)
        bodyType = self.cfg.getOption('editing', 'def_body_type', 'textile')
        self.cbxDefBodyType.set_active(
            datamodel.BODY_TYPES.index(bodyType)
        )
        toolbarView = self.cfg.getOption('toolbars', 'style', 'both')
        if toolbarView == 'both':
            self.rbnIconsAndLabels.set_active(True)
        elif toolbarView == 'icons':
            self.rbnIconsOnly.set_active(True)
        elif toolbarView == 'labels':
            self.rbnLabelsOnly.set_active(True)
        self.window.present()
    
    ### "private" methods ###
    def _enableCustomBrowserSelection(self, enable):
        self.edBrowserCmd.set_sensitive(enable)
        self.fcbSelectBrowser.set_sensitive(enable)
    
    def _savePrefs(self):
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
        if self.rbnUseSysDefBrowser.get_active():
            browser = 'system'
        elif self.rbnUseKdeDefBrowser.get_active():
            browser = 'kde'
        elif self.rbnUseGnomeDefBrowser.get_active():
            browser = 'gnome'
        else:
            browser = 'custom'
        self.cfg.setOption('features', 'browser', browser)
        self.cfg.setOption('features', 'browser_cmd',
            self.edBrowserCmd.get_text())
        if self.ckbUseProxy.get_active():
            value = '1'
        else:
            value = '0'
        self.cfg.setOption('network', 'use_proxy', value)
        self.cfg.setOption('network', 'proxy_host',
            self.edProxyHost.get_text())
        self.cfg.setOption('network', 'proxy_port',
            self.edProxyPort.get_text())
        bodyType = datamodel.BODY_TYPES[self.cbxDefBodyType.get_active()]
        self.cfg.setOption('editing', 'def_body_type', bodyType)
        if self.rbnLabelsOnly.get_active():
            toolbarView = 'labels'
        elif self.rbnIconsOnly.get_active():
            toolbarView = 'icons'
        else:
            toolbarView = 'both'
        self.cfg.setOption('toolbars', 'style', toolbarView)

    ### signal handlers ###
    def on_ckbEnableAutosave_toggled(self, *args):
        isActive = self.ckbEnableAutosave.get_active()
        self.spnAutosaveInterval.set_sensitive(isActive)
    
    def on_ckbUseProxy_toggled(self, *args):
        isActive = self.ckbUseProxy.get_active()
        self.edProxyPort.set_sensitive(isActive)
        self.edProxyHost.set_sensitive(isActive)
    
    def on_rbnUseSysDef_toggled(self, *args):
        self._enableCustomBrowserSelection(False)
    
    def on_rbnUseGnomeDef_toggled(self, *args):
        self._enableCustomBrowserSelection(False)
    
    def on_rbnUseKdeDef_toggled(self, *args):
        self._enableCustomBrowserSelection(False)
    
    def on_rbnUseCustom_toggled(self, *args):
        self._enableCustomBrowserSelection(True)
        
    def on_fcbSelectBrowser_selection_changed(self, *args):
        self.edBrowserCmd.set_text(self.fcbSelectBrowser.get_filename())

    def on_btnCancel_clicked(self, *args):
        self.window.destroy()
    
    def on_btnOk_clicked(self, *args):
        self._savePrefs()
        self.window.destroy()
