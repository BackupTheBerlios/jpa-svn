# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Blogs list dialog"""

__revision__ = '$Id$'

import os
import time
import threading, Queue
import cPickle as pickle
from ConfigParser import NoSectionError, NoOptionError

import gobject
import gtk
from gdata import service

import const
import forms
from forms.gladehelper import GladeWindow
import transport

def show_blogs_list():
    dlg = BlogListWindow()


class UpdaterThread(threading.Thread):

    def __init__(self, service, queue, login, password):
        self.service = service
        self.login = login
        self.password = password
        self.queue = queue
        threading.Thread.__init__(self)

    def run(self):
        blogs = []
        query = self.service.Query()
        query.feed = '/feeds/default/blogs'
        feed = self.service.Get(query.ToUri())
        for entry in feed.entry:
            blog_dict = {
                'id': entry.id.text,
                'title': entry.title.text,
                'updated': entry.updated.text,
            }
            for link in entry.link:
                rel = link.rel.split('#')[-1]
                href = link.href
                blog_dict[rel] = href
            blogs.append(blog_dict)
        self.queue.put_nowait(blogs)


class BlogListWindow(GladeWindow):

    def __init__(self):
        self.create_ui(const.GLADE_PATH, 'dlg_bloglist', domain='jpa')
        self.window = self.ui.dlg_bloglist
        forms.set_window_icon(self.window)
        self._set_widgets()
        self.idle_timer = None
        self.queue = Queue.Queue()
        self.window.present()

    def _set_widgets(self):
        model = gtk.ListStore(str, str, str)
        cells = (gtk.CellRendererText(), gtk.CellRendererText(),
            gtk.CellRendererText())
        columns = (
            gtk.TreeViewColumn(_('Title'), cells[0], text=0),
            gtk.TreeViewColumn(_('Blog URL'), cells[1], text=1),
            gtk.TreeViewColumn(_('Updated'), cells[2], text=2),
        )
        for column in columns:
            self.ui.list_blogs.append_column(column)
        self.ui.list_blogs.set_model(model)
        try:
            fp = open(os.path.join(const.USER_DIR, 'weblogs'), 'rb')
            try:
                weblogs = pickle.load(fp)
            finally:
                fp.close()
        except IOError:
            weblogs = []
        self._update_blog_list(weblogs)

    def _pulse(self):
        weblogs = []
        try:
            weblogs = self.queue.get_nowait()
            self._update_blog_list(weblogs)
            fp = open(os.path.join(const.USER_DIR, 'weblogs'), 'wb')
            try:
                pickle.dump(weblogs, fp, -1)
            finally:
                fp.close()
            self.ui.progress_update.set_fraction(0.0)
        except Queue.Empty:
            pass
        if len(weblogs) == 0:
            time.sleep(0.1)
            self.ui.progress_update.pulse()
            return True
        return False

    def _update_blog_list(self, weblogs):
        model = self.ui.list_blogs.get_model()
        model.clear()
        for weblog in weblogs:
            model.append((weblog['title'], weblog['alternate'],
                weblog['updated']))

    def on_btn_update_clicked(self, *args):
        try:
            login = const.CONFIG.get('auth', 'login')
            password = const.CONFIG.get('auth', 'password')
            if not (login and password):
                raise NoSectionError('auth')
        except (NoSectionError, NoOptionError):
            login, password, captcha = forms.get_auth_data()
        if not (login and password):
            return
        if not transport.service:
            transport.service = service.GDataService(login, password)
        svc = transport.service
        svc.source = 'zgoda-JPA-0.6'
        svc.service = 'blogger'
        svc.server = 'www.blogger.com'
        try:
            svc.ProgrammaticLogin()
        except service.CaptchaRequired:
            url = svc.captcha_url
            token = svc.captcha_token
            login, password, captcha = forms.get_auth_data(url)
            svc.ProgrammaticLogin(token, captcha)
        except service.BadAuthentication:
            # show the error
            pass
        self.idle_timer = gobject.idle_add(self._pulse)
        updater = UpdaterThread(svc, self.queue, login, password)
        updater.setDaemon(True)
        updater.start()

    def on_btn_close_clicked(self, *args):
        if self.idle_timer:
            gobject.source_remove(self.idle_timer)
        self.window.destroy()

    def on_dlg_bloglist_delete_event(self, *args):
        if self.idle_timer:
            gobject.source_remove(self.idle_timer)
