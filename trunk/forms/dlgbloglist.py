# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Blogs list dialog"""

__revision__ = '$Id$'

import time
import threading, Queue

import gobject
from gdata import service

import const
import forms
from forms.gladehelper import GladeWindow

def show_blogs_list():
    dlg = BlogListWindow()


class UpdaterThread(threading.Thread):

    def __init__(self, queue):
        self.queue = queue
        threading.Thread.__init__(self)

    def run(self):
        blogs = []
        login = const.CONFIG.get('auth', 'login')
        password = const.CONFIG.get('auth', 'password')
        svc = service.GDataService(login, password)
        svc.source = 'zgoda-JPA-0.6'
        svc.service = 'blogger'
        svc.server = 'www.blogger.com'
        svc.ProgrammaticLogin()
        query = service.Query()
        query.feed = '/feeds/default/blogs'
        feed = svc.Get(query.ToUri())
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
        self.weblogs = []
        self.create_ui(const.GLADE_PATH, 'dlg_bloglist', domain='jpa')
        self.window = self.ui.dlg_bloglist
        forms.set_window_icon(self.window)
        self._set_widgets()
        self.idle_timer = gobject.idle_add(self._pulse)
        self.queue = Queue.Queue()
        updater = UpdaterThread(self.queue)
        updater.start()
        self.window.present()

    def _set_widgets(self):
        pass

    def _pulse(self):
        try:
            self.weblogs = self.queue.get_nowait()
            print self.weblogs
            self.ui.progress_update.set_fraction(0.0)
            self.ui.box_update.hide()
        except Queue.Empty:
            pass
        if len(self.weblogs) == 0:
            time.sleep(0.1)
            self.ui.progress_update.pulse()
            return True
        return False

    def on_btn_update_clicked(self, *args):
        print 'update'

    def on_btn_close_clicked(self, *args):
        gobject.source_remove(self.idle_timer)
