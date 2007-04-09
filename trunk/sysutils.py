# -*- coding: utf-8 -*-

# Copyright 2003-2007 Jarek Zgoda <jzgoda@o2.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Various system-related utilities"""

__revision__ = '$Id$'

import os
import webbrowser

def open_url(url, system='system', command=None):
    """A function that opens document at URL using somewhat-default
    web browser. As there's no real default, a little cheating is done
    here. By specifying system as "gnome" or "kde", the platform's default
    will be used. If you specify system as "system", you will rely on what
    standard webbrowser module decides to use. Alternatively you may specify
    anything and give a ready system command to launch your browser."""
    if system.lower() == 'system':
        browser = webbrowser.get()
        browser.open(url, 1)
        return
    elif system.lower() == 'kde':
        cmd = 'kfmclient exec'
    elif system.lower() == 'gnome':
        cmd = 'gnome-open'
    else:
        cmd = command
    if os.name != 'nt':
        url = url.replace('"', '\\"')
    cmd = '%s "%s"' % (cmd, url)
    # FIXME: this is a dirty hack
    try:
        os.system(cmd)
    except:
        pass

def initialize_config(config, **section_dicts):
    """A function that initializes application config using
    defaults. Each section has to be a dictionary."""
    for name, section in section_dicts.items():
        if not config.has_section(name):
            config.add_section(name)
        for k, v in section.items():
            config.set(name, k, v)