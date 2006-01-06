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

"""GUI controller/signal dispatcher"""

__revision__ = '$Id$'

import os, tempfile, subprocess
import webbrowser

import gtk
import gtk.glade

import appconst, apputils, renderer
import entry_dialog, categories_dialog, prefs_dialog, category_dialog, \
    about_dialog, identities_dialog

class Controller:
    
    def __init__(self):
        self.__tempFiles = []
        self.cfg = appconst.CFG
    
    def showAbout(self, parent=None):
        dialog = about_dialog.AboutDialog(parent)
        dialog.show()
    
    def newEntry(self, parent=None):
        dialog = entry_dialog.EntryDialog(parent)
        dialog.show()
    
    def editEntry(self, entry, parent=None):
        dialog = entry_dialog.EntryDialog(parent, entry)
        dialog.show()
    
    def showIdentities(self):
        dialog = identities_dialog.IdentitiesDialog(self)
        dialog.show()

    def showCategories(self):
        dialog = categories_dialog.CategoriesDialog(self)
        dialog.show()
    
    def showPreferences(self, parent=None):
        dialog = prefs_dialog.PreferencesDialog(parent)
        dialog.show()
    
    def editCategory(self, category, parent=None):
        dialog = category_dialog.CategoryDialog(parent, category)
        dialog.show()
    
    def newCategory(self, parent=None):
        dialog = category_dialog.CategoryDialog(parent)
        dialog.show()
    
    def previewEntry(self, entry, parent=None):
        fd, fileName = tempfile.mkstemp('.html')
        os.close(fd)
        self.__tempFiles.append(fileName)
        title = entry.title.encode('utf-8')
        text = entry.body.encode('utf-8')
        bodyType = entry.bodyType.encode('utf-8')
        html = renderer.render(title, text, bodyType)
        fp = open(fileName, 'w')
        try:
            fp.write(html)
        finally:
            fp.close()
        # the following code is inspired by Gajim
        uri = 'file://%s' % fileName
        browserType = self.cfg.getOption('features', 'browser', 'system')
        if browserType == 'system':
            browser = webbrowser.get()
            browser.open(uri, 1)
            return
        elif browserType == 'kde':
            command = 'kfmclient exec'
        elif browserType == 'gnome':
            command = 'gnome-open'
        else:
            command = self.cfg.getOption('features', 'browser_cmd', '')
        if os.name != 'nt':
            uri = uri.replace('"', '\\"') # escape " for shell happiness
        command = command + ' "' + uri + '"'
        try: #FIXME: dirty hack
            os.system(command)
        except:
            pass
    
    def __del__(self):
        for fileName in self.__tempFiles:
            os.unlink(fileName)
