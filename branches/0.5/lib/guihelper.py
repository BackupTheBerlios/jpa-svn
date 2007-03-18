# -*- coding: UTF-8 -*-

# This file is part of JPA.
# Copyright: (C) 2003 - 2006 Jarek Zgoda <jzgoda@o2.pl>
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

"""PyGTK GUI helpers"""

__revision__ = '$Id$'


import os
import gettext

try:
    from xml.etree import ElementTree
except ImportError:
    try:
        import cElementTree as ElementTree
    except ImportError:
        try:
            import lxml.etree as ElementTree
        except ImportError:
            # if this one fails, we will be unable to go any further
            from elementtree import ElementTree

import gtk, gtk.glade


def get_widget_names(glade_path, glade_file_name):
    """Get list of all widgets in glade file."""
    glade_file_path = os.path.join(glade_path, window_name)
    tree = ElementTree.parse(glade_file_path)
    root = tree.getroot()
    widgets = root.findall('.//widget')
    widget_names = []
    for child_widget in widgets:
        widget_names.append(child_widget.get('id'))
    return widget_names


class GtkGuiHelper:

    def __init__(self, glade_path, app_name, i18n_path):
        """Helper class constructor.
        Expected arguments are: path to directory with glade files,
        application name (used as gettext translation "domain" name) and
        path to directory where translation catalogs reside."""
        self.glade_path = glade_path
        self.app_name = app_name
        self.i18n_path = i18n_path
        gtk.glade.bindtextdomain(app_name, i18n_path)
        gtk.glade.textdomain(app_name)
        gettext.install(app_name, i18n_path, unicode=True)
        self.widget_trees = {}

    def _get_widget_tree(window_name):
        try:
            widget_tree = self.widget_trees[window_name]
        except KeyError:
            # this window is created for 1st time
            glade_file_name = os.path.join(self.glade_path, window_name)
            widget_tree = gtk.glade.XML(glade_file_name, window_name, \
                self.app_name)
            self.widget_trees[window_name] = widget_tree
        return widget_tree

    def get_widgets(self, window_name):
        """This method returns tuple of toplevel widget (usually a window)
        and a dictionary of child widgets (name => widget)."""
        widget_tree = self._get_widget_tree(window_name)
        window = widget_tree.get_widget(window_name)
        widget_names = get_widget_names(self.glade_path, window_name)
        widgets = {}
        for widget_name in widget_names:
            widgets[widget_name] = widget_tree.get_widget(widget_name)
        return (window, widgets)

    def connect_signals(self, window_name, signal_dict):
        """This method connect signals defined in glade file to dictionary
        of signals, usually some class instance."""
        widget_tree = self._get_widget_tree(window_name)
        widget_tree.signal_autoconnect(signal_dict)
