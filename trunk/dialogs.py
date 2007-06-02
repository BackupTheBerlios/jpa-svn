# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Miscellaneous dialogs"""

__revision__ = '$Id$'

import gtk

def question(text, parent=None):
    """
    Dialog with question. Returns true if response was "Yes".
    """
    msg = gtk.MessageDialog(parent, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION,
        gtk.BUTTONS_YES_NO, text)
    try:
        resp = msg.run()
    finally:
        msg.destroy()
    return resp == gtk.RESPONSE_YES

def error(text, parent=None):
    """
    Error message dialog.
    """
    msg = gtk.MessageDialog(parent, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,
        gtk.BUTTONS_OK, text)
    try:
        msg.run()
    finally:
        msg.destroy()

def warning(text, parent=None):
    """
    Warning message dialog.
    """
    msg = gtk.MessageDialog(parent, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING,
        gtk.BUTTONS_OK, text)
    try:
        msg.run()
    finally:
        msg.destroy()
