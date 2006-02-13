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
    about_dialog, identities_dialog, identity_dialog, htmlview_dialog, \
    weblogs_dialog, weblog_dialog, weblogdisco_dialog, weblogsel_dialog, \
    pubhistory_dialog

class Controller:
    
    def __init__(self):
        self.__tempFiles = []
        self.cfg = appconst.CFG
    
    def showAbout(self, parent):
        dialog = about_dialog.AboutDialog(parent)
        dialog.show()
    
    def newEntry(self, parent):
        dialog = entry_dialog.EntryDialog(parent)
        dialog.show()
    
    def editEntry(self, entry, parent):
        dialog = entry_dialog.EntryDialog(parent, entry)
        dialog.show()
    
    def deleteEntry(self, entry, parent):
        text = _('Do you really want to delete this entry?')
        if apputils.question(text, parent.window):
            i = 0
            while len(entry.publications) > 0:
                publication = entry.publications[i]
                publication.destroySelf()
                i = i + 1
            entry.destroySelf()
            parent.notify('entry-deleted')
    
    def saveEntry(self, entry, parent):
        dialog = gtk.FileChooserDialog(
            title=_('Save entry to file'),
            parent=parent.window,
            action=gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK),
        )
        try:
            f = gtk.FileFilter()
            f.set_name(_('All files'))
            f.add_pattern('*')
            dialog.add_filter(f)
            f = gtk.FileFilter()
            f.set_name(_('HTML files'))
            f.add_mime_type('text/html')
            dialog.add_filter(f)
            dialog.set_current_folder(os.path.expanduser('~'))
            if dialog.run() == gtk.RESPONSE_OK:
                fileName = dialog.get_filename()
                title = entry.title.encode('utf-8')
                text = entry.body.encode('utf-8')
                bodyType = entry.bodyType.encode('utf-8')
                html = renderer.renderPage(title, text, bodyType)
                fp = open(fileName, 'w')
                try:
                    fp.write(html)
                finally:
                    fp.close()
        finally:
            dialog.destroy()
    
    def showIdentities(self):
        dialog = identities_dialog.IdentitiesDialog(self)
        dialog.show()

    def showCategories(self, parent):
        dialog = categories_dialog.CategoriesDialog(self, parent)
        dialog.show()
    
    def showWeblogs(self):
        dialog = weblogs_dialog.WeblogsDialog(self)
        dialog.show()
    
    def showPreferences(self, parent):
        dialog = prefs_dialog.PreferencesDialog(parent)
        dialog.show()
    
    def showPubHistory(self, entry):
        dialog = pubhistory_dialog.PublicationHistoryDialog(self, entry)
        dialog.show()
    
    def editCategory(self, category, parent):
        dialog = category_dialog.CategoryDialog(parent, category)
        dialog.show()
    
    def newCategory(self, parent):
        dialog = category_dialog.CategoryDialog(parent)
        dialog.show()
    
    def deleteCategory(self, category, parent):
        text = _('Do you really want to delete this category?')
        if apputils.question(text, parent.window):
            category.destroySelf()
            parent.notify('data-changed')
    
    def newIdentity(self, parent):
        dialog = identity_dialog.IdentityDialog(parent)
        dialog.show()
    
    def editIdentity(self, identity, parent):
        dialog = identity_dialog.IdentityDialog(parent, identity)
        dialog.show()
    
    def deleteIdentity(self, identity, parent):
        text = _('Do you really want to delete this identity?')
        if apputils.question(text, parent.window):
            identity.destroySelf()
            parent.notify('data-changed')

    def newWeblog(self, parent):
        dialog = weblog_dialog.WeblogDialog(parent)
        dialog.show()

    def editWeblog(self, weblog, parent):
        dialog = weblog_dialog.WeblogDialog(parent, weblog)
        dialog.show()
    
    def deleteWeblog(self, weblog, parent):
        text = _('Do you really want to delete this weblog?')
        if apputils.question(text, parent.window):
            weblog.destroySelf()
            parent.notify('data-changed')
    
    def discoverWeblogs(self, identity, parent):
        dialog = weblogdisco_dialog.WeblogDiscoveryDialog(parent, identity)
        dialog.show()
    
    def previewEntry(self, entry, parent=None):
        fd, fileName = tempfile.mkstemp('.html')
        self.__tempFiles.append(fileName)
        title = entry.title.encode('utf-8')
        text = entry.body.encode('utf-8')
        bodyType = entry.bodyType.encode('utf-8')
        html = renderer.renderPage(title, text, bodyType)
        fp = os.fdopen(fd, 'w')
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
    
    def showHtml(self, entry, parent=None):
        dialog = htmlview_dialog.HtmlViewDialog(parent, entry)
        dialog.show()
    
    def getPublishTo(self, parent):
        dialog = weblogsel_dialog.WeblogSelectionDialog(parent)
        dialog.show()
    
    def getRepublishTo(self, entry, parent):
        dialog = weblogsel_dialog.WeblogSelectionDialog(parent, entry)
        dialog.show()
    
    def publishEntry(self, entry, blogs):
        for blog in blogs:
            entry.publish(blog)
    
    def __del__(self):
        for fileName in self.__tempFiles:
            os.unlink(fileName)
