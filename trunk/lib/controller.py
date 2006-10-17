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

import os, tempfile
import os.path as op

import louie
import gtk
import gtk.glade

import appconst, apputils, renderer, transport, blogoper
from appconst import DEBUG
import entry_dialog, categories_dialog, prefs_dialog, category_dialog, \
    about_dialog, identities_dialog, identity_dialog, htmlview_dialog, \
    weblogs_dialog, weblog_dialog, weblogdisco_dialog, weblogsel_dialog, \
    pubhistory_dialog, catsel_dialog, filter_dialog, captcha_dialog, \
    mediafiles_dialog

class Controller:

    def __init__(self):
        self._tempFiles = []
        self.cfg = appconst.CFG

    def showAbout(self, parent):
        dialog = about_dialog.AboutDialog(parent)
        dialog.run()

    def showHelpIndex(self):
        fileName = op.join(appconst.PATHS['doc'], 'index.html')
        uri = 'file://%s' % fileName
        browserType = self.cfg.getOption('features', 'browser', 'system')
        command = self.cfg.getOption('features', 'browser_cmd', '')
        apputils.openURL(uri, browserType, command)

    def newEntry(self, parent=None):
        dialog = entry_dialog.EntryDialog(None, parent)
        dialog.show()

    def editEntry(self, entry, parent=None):
        dialog = entry_dialog.EntryDialog(entry, parent)
        dialog.show()

    def deleteEntry(self, entry, parent):
        if entry.publications:
            text = _('This entry has been published to weblogs.\n'
                'Do you want to delete this entry with all publications?')
        else:
            text = _('Do you really want to delete this entry?')
        if apputils.question(text, parent.window):
            i = len(entry.publications) - 1
            if DEBUG:
                print entry.publications
            while i > -1:
                publication = entry.publications[i]
                blog = publication.weblog
                publication.deleteRemoteEntry(blog, parent)
                publication.destroySelf()
                i = i - 1
            entry.destroySelf()
            louie.send('entry-deleted')

    def saveEntry(self, entry, parent):
        dialog = gtk.FileChooserDialog(
            title=_('Save entry to file'),
            parent=parent.window,
            action=gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                gtk.STOCK_SAVE, gtk.RESPONSE_OK
            ),
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
            dialog.set_current_folder(op.expanduser('~'))
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

    def getEntryFilter(self, parent, curFilter):
        dialog = filter_dialog.FilterDialog(parent, curFilter)
        dialog.run()

    def showIdentities(self):
        dialog = identities_dialog.IdentitiesDialog(self)
        dialog.show()

    def showCategories(self):
        dialog = categories_dialog.CategoriesDialog(self)
        dialog.show()

    def showRemoteCategories(self, categories, parent):
        dialog = categorydisco_dialog.CategoryDiscoveryDialog(categories, parent)
        dialog.show()

    def showWeblogs(self):
        dialog = weblogs_dialog.WeblogsDialog(self)
        dialog.show()

    def showMedia(self):
        dialog = mediafiles_dialog.MediafilesDialog(self)
        dialog.show()

    def showPreferences(self, parent):
        dialog = prefs_dialog.PreferencesDialog(parent)
        dialog.run()

    def showPubHistory(self, entry):
        dialog = pubhistory_dialog.PublicationHistoryDialog(self, entry)
        dialog.show()

    def editCategory(self, category, parent):
        dialog = category_dialog.CategoryDialog(parent, category)
        dialog.run()

    def newCategory(self, parent):
        dialog = category_dialog.CategoryDialog(parent)
        dialog.run()

    def deleteCategory(self, category, parent):
        text = _('Do you really want to delete this category?')
        if apputils.question(text, parent.window):
            category.destroySelf()
            louie.send('category-deleted')

    def newIdentity(self, parent):
        dialog = identity_dialog.IdentityDialog(parent)
        dialog.run()

    def editIdentity(self, identity, parent):
        dialog = identity_dialog.IdentityDialog(parent, identity)
        dialog.run()

    def deleteIdentity(self, identity, parent):
        text = _('Do you really want to delete this identity?')
        if apputils.question(text, parent.window):
            identity.destroySelf()
            louie.send('identity-deleted')

    def newWeblog(self, parent):
        dialog = weblog_dialog.WeblogDialog(parent)
        dialog.run()

    def editWeblog(self, weblog, parent):
        dialog = weblog_dialog.WeblogDialog(parent, weblog)
        dialog.run()

    def deleteWeblog(self, weblog, parent):
        text = _('Do you really want to delete this weblog?')
        if apputils.question(text, parent.window):
            weblog.destroySelf()
            louie.send('weblog-deleted')

    def discoverWeblogs(self, identity, parent):
        dialog = weblogdisco_dialog.WeblogDiscoveryDialog(parent, identity)
        dialog.show()

    def previewEntry(self, entry):
        fd, fileName = tempfile.mkstemp('.html')
        self._tempFiles.append(fileName)
        title = entry.title.encode('utf-8')
        text = entry.body.encode('utf-8')
        bodyType = entry.bodyType.encode('utf-8')
        html = renderer.renderPage(title, text, bodyType)
        fp = os.fdopen(fd, 'w')
        try:
            fp.write(html)
        finally:
            fp.close()
        uri = 'file://%s' % fileName
        browserType = self.cfg.getOption('features', 'browser', 'system')
        command = self.cfg.getOption('features', 'browser_cmd', '')
        apputils.openURL(uri, browserType, command)

    def showHtml(self, entry, parent=None):
        dialog = htmlview_dialog.HtmlViewDialog(parent, entry)
        dialog.show()

    def getPublishTo(self, parent):
        dialog = weblogsel_dialog.WeblogSelectionDialog(parent)
        dialog.show()

    def getRepublishTo(self, entry, parent):
        dialog = weblogsel_dialog.WeblogSelectionDialog(parent, entry)
        dialog.show()

    def selectCategories(self, entry, service, parent):
        dialog = catsel_dialog.CategorySelectionDialog(parent, entry, service)
        dialog.show()

    def getCaptchaCode(self, filePath, parent):
        dialog = captcha_dialog.CaptchaDialog(parent, filePath)
        return dialog.run()

    def __del__(self):
        for fileName in self._tempFiles:
            os.unlink(fileName)
