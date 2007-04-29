# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Main application window"""

__revision__ = '$Id$'

import os

import gtk

import const, forms


class MainWindow(object):

    def __init__(self):
        widget_tree = gtk.glade.XML(const.GLADE_PATH, 'frm_main', 'JPA')
        widget_tree.signal_autoconnect(self)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect('delete-event', self.delete_event)
        forms.set_window_icon(self.window)
        self.window.set_border_width(1)
        self.window.set_size_request(720, 560)
        self.main_box = gtk.VBox()
        uimgr = self._create_ui()
        menubar = uimgr.get_widget('/Menubar')
        self.main_box.pack_start(menubar, expand=False)
        toolbar = uimgr.get_widget('/Toolbar')
        self.main_box.pack_start(toolbar, expand=False)
        main_widget = widget_tree.get_widget('main_box')
        main_widget.unparent()
        self.main_box.pack_start(main_widget)
        self.statusbar = gtk.Statusbar()
        self.main_box.pack_end(self.statusbar, expand=False)
        self.window.add(self.main_box)

    def show(self):
        self.window.show_all()

    def quit(self):
        gtk.main_quit()

    # signal handlers
    def delete_event(self, widget, event, data=None):
        self.quit()
        return False

    def _on_action_new(self, action):
        pass

    def _on_action_edit(self, action):
        pass

    def _on_action_save_as(self, action):
        pass

    def _on_action_publish(self, action):
        pass

    def _on_action_quit(self, action):
        self.quit()

    def _on_action_preferences(self, action):
        pass

    def _on_action_refresh(self, action):
        pass

    def _on_action_list_blogs(self, action):
        pass

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
            ('Publish', gtk.STOCK_CONNECT, _('_Publish'), None,
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
            ('HelpMenu', None, _('Help')),
            ('About', gtk.STOCK_ABOUT, _('_About...'), None,
                _('About JPA, the Weblog Assistant'), self._on_action_about),
        ]
        ag.add_actions(actions)
        ui = gtk.UIManager()
        ui.insert_action_group(ag, 0)
        ui.add_ui_from_file(os.path.join(const.BASE_DIR, 'ui',
            'mainmenu.ui.xml'))
        return ui
