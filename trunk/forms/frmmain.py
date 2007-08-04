# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Main application window"""

__revision__ = '$Id$'

import os
import cPickle as pickle
import Queue
from ConfigParser import NoSectionError, NoOptionError

import gtk, pango

import const, forms, data


class MainWindow(object):

    def __init__(self):
        self.cfg = const.CONFIG
        self.data = data.Storage()
        self.widget_tree = gtk.glade.XML(const.GLADE_PATH, 'frm_main', 'JPA')
        self.widget_tree.signal_autoconnect(self)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect('delete-event', self.delete_event)
        forms.set_window_icon(self.window)
        self.window.set_border_width(2)
        self.window.set_title('JPA, the Weblog Publishing Assistant')
        self.window.set_size_request(720, 560)
        self.main_box = gtk.VBox()
        uimgr = self._create_ui()
        uimgr.connect('connect-proxy',
            self._on_uimanager__connect_proxy)
        uimgr.connect('disconnect-proxy',
            self._on_uimanager__disconnect_proxy)
        menubar = uimgr.get_widget('/Menubar')
        self.main_box.pack_start(menubar, expand=False)
        toolbar = uimgr.get_widget('/Toolbar')
        self.main_box.pack_start(toolbar, expand=False)
        main_widget = self.widget_tree.get_widget('main_box')
        main_widget.unparent()
        self.main_box.pack_start(main_widget)
        self.statusbar = gtk.Statusbar()
        self.main_box.pack_end(self.statusbar, expand=False)
        self.window.add(self.main_box)
        self._menu_cix = -1
        self._set_widget_properties()
        self.queue = Queue.Queue()

    def show(self):
        self.window.show_all()

    def quit(self):
        self.data.save()
        config_file = os.path.join(const.USER_DIR, 'config')
        fp = open(config_file, 'w')
        try:
            self.cfg.write(fp)
        finally:
            fp.close()
        gtk.main_quit()

    # signal handlers
    def delete_event(self, widget, event, data=None):
        self.quit()
        return False

    def on_btn_search_clicked(self, widget, data=None):
        print "search"

    def on_combo_blogs_changed(self, widget, data=None):
        model = widget.get_model()
        active = widget.get_active()
        if active >= 0:
            title, feed, post_url = model[active]
            for blog in self.weblogs:
                if blog['post_url'] == post_url:
                    break

    # uimanager
    def _on_uimanager__connect_proxy(self, uimgr, action, widget):
        tooltip = action.get_property('tooltip')
        if isinstance(widget, (gtk.Item, )) and tooltip:
            cid = widget.connect(
                'select', self._on_action_item__select, tooltip)
            cid2 = widget.connect(
                'deselect', self._on_action_item__deselect)
            widget.set_data('kiwiapp::cids', (cid, cid2))

    def _on_uimanager__disconnect_proxy(self, uimgr, action, widget):
        cids = widget.get_data('kiwiapp::cids') or ()
        for name, cid in cids:
            widget.disconnect(cid)

    # actions
    def _on_action_item__select(self, item, tooltip):
        self.statusbar.push(self._menu_cix, tooltip)

    def _on_action_item__deselect(self, item):
        self.statusbar.pop(self._menu_cix)

    def _on_action_new(self, action):
        forms.edit_new_entry()

    def _on_action_edit(self, action):
        pass

    def _on_action_save_as(self, action):
        pass

    def _on_action_publish(self, action):
        pass

    def _on_action_quit(self, action):
        self.quit()

    def _on_action_preferences(self, action):
        forms.edit_preferences()

    def _on_action_refresh(self, action):
        pass

    def _on_action_list_blogs(self, action):
        forms.show_blogs_list()

    def _on_action_about(self, action):
        forms.show_about()

    # semi-private
    def _create_ui(self):
        ag = gtk.ActionGroup('Actions')
        actions = [
            ('FileMenu', None, _('_File')),
            ('New', gtk.STOCK_NEW, _('_New'), '<control>N',
                _('Write new blog entry'), self._on_action_new),
            ('Edit', gtk.STOCK_EDIT, _('_Edit'), 'F2',
                _('Edit entry'), self._on_action_edit),
            ('SaveAs', gtk.STOCK_SAVE_AS, _('Save _As...'), None,
                _('Save entry to disk file'), self._on_action_save_as),
            ('Publish', gtk.STOCK_EXECUTE, _('_Publish'), None,
                _('Publish an entry to weblog'), self._on_action_publish),
            ('Quit', gtk.STOCK_QUIT, _('_Quit'), None,
                _('Close the program'), self._on_action_quit),
            ('EditMenu', None, _('_Edit')),
            ('Preferences', gtk.STOCK_PREFERENCES, _('_Preferences'), None,
                _('Change program preferences'), self._on_action_preferences),
            ('ViewMenu', None, _('_View')),
            ('RefreshView', gtk.STOCK_REFRESH, _('_Refresh'), 'F5',
                _('Refresh entries view'), self._on_action_refresh),
            ('ToolsMenu', None, _('_Tools')),
            ('BlogList', None, _('_Blogs'), None,
                _('List of blogs'), self._on_action_list_blogs),
            ('HelpMenu', None, _('_Help')),
            ('About', gtk.STOCK_ABOUT, _('_About...'), None,
                _('About JPA, the Weblog Assistant'), self._on_action_about),
        ]
        ag.add_actions(actions)
        ui = gtk.UIManager()
        ui.insert_action_group(ag, 0)
        ui.add_ui_from_file(os.path.join(const.BASE_DIR, 'ui',
            'mainmenu.ui.xml'))
        # initial disabling of some actions
        ag.get_action('Edit').set_sensitive(False)
        ag.get_action('Publish').set_sensitive(False)
        return ui

    def _set_widget_properties(self):
        log_view = self.widget_tree.get_widget('text_log_view')
        try:
            font_name = self.cfg.get('fonts', 'log')
        except (NoSectionError, NoOptionError):
            font_name = 'Monospace 10'
        log_view.modify_font(pango.FontDescription(font_name))
        entry_view = self.widget_tree.get_widget('text_entry_body')
        try:
            font_name = self.cfg.get('fonts', 'entry')
        except (NoSectionError, NoOptionError):
            font_name = 'Sans 12'
        entry_view.modify_font(pango.FontDescription(font_name))
        # entries list
        entry_list = self.widget_tree.get_widget('lv_entries')
        model = gtk.ListStore(str, str)
        cells = (gtk.CellRendererText(), gtk.CellRendererText())
        columns = (
            gtk.TreeViewColumn(_('Title'), cells[0], text=0),
            gtk.TreeViewColumn(_('Published'), cells[1], text=1),
        )
        for column in columns:
            entry_list.append_column(column)
        entry_list.set_model(model)
        # blogs combo
        try:
            fp = open(os.path.join(const.USER_DIR, 'weblogs'), 'rb')
            try:
                self.weblogs = pickle.load(fp)
            finally:
                fp.close()
        except IOError:
            self.weblogs = []
        model = gtk.ListStore(str, str, str)
        for weblog in self.weblogs:
            model.append((weblog['title'], weblog['feed'], weblog['post']))
        blogs_combo = self.widget_tree.get_widget('combo_blogs')
        cell = gtk.CellRendererText()
        blogs_combo.pack_start(cell, True)
        blogs_combo.add_attribute(cell, 'text', 0)
        blogs_combo.set_model(model)
