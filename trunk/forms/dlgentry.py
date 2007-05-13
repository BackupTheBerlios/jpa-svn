# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Entry editing dialog"""

__revision__ = '$Id$'

from ConfigParser import NoSectionError, NoOptionError

import gtk, pango
import gobject

import forms
from forms.gladehelper import GladeWindow
import const

def edit_new_entry():
    dlg = EntryWindow()
    return dlg.run()

class EntryWindow(GladeWindow):

    def __init__(self, entry_dict={}):
        self.entry = entry_dict
        self.saved = False
        self.create_ui(const.GLADE_PATH, 'dlg_entry', domain='jpa')
        self.window = self.ui.dlg_entry
        forms.set_window_icon(self.window)
        self._set_widget_properties()

    def run(self):
        while 1:
            ret = self.window.run()
            if ret == gtk.RESPONSE_APPLY:
                self.save()
            elif ret == gtk.RESPONSE_OK:
                self.save()
                break
            else:
                break
        self.window.destroy()
        return self.saved

    def save(self):
        if self.entry:
            entry = self.entry
        else:
            text_buffer = self.ui.tv_text.get_buffer()
            labels_text = self.ui.ed_labels.get_text().decode('utf-8').strip()
            if labels_text == u'':
                labels = []
            else:
                labels = [label.strip() for label in labels_text.split(',')]
            entry = {
                'title': self.ui.ed_title.get_text().decode('utf-8'),
                'text': text_buffer.get_text(text_buffer.get_start_iter(),
                    text_buffer.get_end_iter()).decode('utf-8'),
                'labels': labels,
                'is_draft': self.ui.ckb_is_draft.get_active(),
            }
        print entry
        self.saved = True

    def _set_widget_properties(self):
        try:
            font_name = const.CONFIG.get('fonts', 'editor')
        except (NoSectionError, NoOptionError):
            font_name = 'Monospace 10'
        self.ui.tv_text.modify_font(pango.FontDescription(font_name))
        model = gtk.ListStore(str)
        for markup_type in const.MARKUP_TYPES:
            model.append((markup_type, ))
        self.ui.combo_contenttype.set_model(model)
        cell = gtk.CellRendererText()
        self.ui.combo_contenttype.pack_start(cell)
        self.ui.combo_contenttype.add_attribute(cell, 'text', 0)
        self.ui.combo_contenttype.set_active(0)
        completion = gtk.EntryCompletion()
        self.ui.ed_labels.set_completion(completion)
        store = gtk.ListStore(gobject.TYPE_STRING)
        completion.set_model(store)
        completion.set_text_column(0)
        completion.connect('match-selected', self.on_match_selected)
        if self.entry:
            self.ui.ed_title.set_text(self.entry['title'])
            bf = self.ui.tv_text.get_buffer()
            bf.set_text(self.entry['text'])

    def on_match_selected(self, *args, **kwds):
        pass
