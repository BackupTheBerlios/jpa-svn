# -*- coding: utf-8 -*-
 
# gladehelper.py
# Copyright (C) 2005 by Roman Roelofsen
# develop@tuxed.de
#
# Stripped-down and enabled for i18n by Jarek Zgoda <jzgoda@o2.pl>, (c) 2007
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


"""
CHANGES TO THE ORIGINAL CODE:
 1. Removed __getattr__ and __setattr__ machinery related to access classes;
 2. Removed the access classes and related things from the code;

I don't know why, but the access machinery made into infinite recursion...
"""


import sys
import os

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

import xml.dom.minidom


# #######################
# glade class
# #######################

class _CachedParser:
    cache = {}
    
    def parse(self, xmlfile):
        if xmlfile not in self.cache:
            self.cache[xmlfile] = xml.dom.minidom.parse(xmlfile)
            
        return self.cache[xmlfile]

cachedParser = _CachedParser()


class GladeWindow(object):

    def create_ui(self, gladefile, window, checkcallbacks=False, domain=None):
        self.__dict__['gladefile'] = gladefile
        self.__dict__['window'] = window

        # path to glade file
        mn = self.__class__.__module__
        filename = sys.modules[mn].__file__
        path = os.path.dirname(os.path.abspath(filename))
        gladefile = os.path.join(path, gladefile)

        # should i check the callback methods?
        if checkcallbacks:
            self.check_callbacks(gladefile)
            
        # call glade XML
        if domain:
            wTree = gtk.glade.XML(gladefile, self.window, domain)
        else:
            wTree = gtk.glade.XML(gladefile, self.window)
        
        # UI namespace
        classname = self.__class__.__name__
        class UI:
            def __getattr__(self, name):
                widget = wTree.get_widget(name)
                if widget is not None:
                    self.__dict__[name] = widget
                    return widget
                else:
                    msg = "Glade window " + classname + " has no attribute '" + name + "'"
                    raise AttributeError(msg)
        self.__dict__['ui'] = UI()

        # connect signals and slots
        for attr in dir(self):
            method = getattr(self, attr)
            if callable(method):
                wTree.signal_autoconnect({attr: method})
        
        
    def check_callbacks(self, gladefile):
        dom = cachedParser.parse(gladefile)
        conf = dom.getElementsByTagName("glade-interface")[0]
        for node in conf.childNodes:
            if node.nodeName == "widget":
                wn = self.get_attribute(node, "id")
                if wn == self.window:
                    # widget found
                    self.handle_node(node)
                    return 
    
    def handle_node(self, node):
        if node.nodeName == "widget":
            self.handle_widget(node)
             
        if node.hasChildNodes():
            for child in node.childNodes:
                self.handle_node(child)
    
    def handle_widget(self, widget):
        # connect signals
        if widget.hasChildNodes():
            for child in widget.childNodes:
                if child.nodeName == "signal":
                    signal = self.get_attribute(child, "handler")
                    if signal not in dir(self):
                        classname = self.__class__.__name__
                        print "WARNING: method [" + signal + "] in class [" + classname + "] not found!"
    
    def get_attribute(self, node, name):
        attrs = node.attributes
        for i in range(attrs.length):
            att = attrs.item(i)
            if att.name == name:
                return att.nodeValue


