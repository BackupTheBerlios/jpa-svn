#! /usr/bin/env python
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

"""Main program file, used to initialize stuff, import global modules and set
standard paths."""

__revision__ = '$Id$'

# path setup
import os, sys
import os.path as op
basePath = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.insert(0, basePath)
paths = {}
for dirName in ('bin', 'doc', 'lib', 'share'):
    paths[dirName] = op.join(basePath, dirName)
paths['img'] = op.join(paths['share'], 'images')
paths['i18n'] = op.join(paths['share'], 'locale')
userPath = op.expanduser('~')
if not os.access(userPath, os.F_OK) and os.name == 'nt':
    #OMG, misconfigured Windows
    userPath = os.environ['USERPROFILE']
    if not os.access(userPath, os.F_OK):
        #OMFG, totally fucked-up Windows
        userPath = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
if not os.access(userPath, os.F_OK):
    # give up
    userPath = basePath
userPath = op.join(userPath, '.jpa')
paths['user'] = userPath
userTransports = op.join(userPath, 'plugins', 'transport')
if not op.isdir(userTransports):
    os.makedirs(userTransports)
    fp = open(op.join(userTransports, '__init__.py'), 'w')
    try:
        fp.write('# transport plugins go here\n')
    finally:
        fp.close()
paths['transport plugins'] = userTransports
userRenderers = op.join(userPath, 'plugins', 'renderer')
if not op.isdir(userRenderers):
    os.makedirs(userRenderers)
    fp = open(op.join(userRenderers, '__init__.py'), 'w')
    try:
        fp.write('# simplified markup renderer plugins go here\n')
    finally:
        fp.close()
paths['renderer plugins'] = userRenderers
dbPath = op.join(userPath, 'data', 'jpa.db')
paths['data'] = dbPath
if os.name == 'nt':
    uri = dbPath.replace(':', '|').replace('\\', '/')
    uri = 'sqlite:///%s' % uri
else:
    uri = 'sqlite://%s' % dbPath
import lib.appconst
lib.appconst.PATHS = paths
lib.appconst.DB_URI = uri


if __name__ == '__main__':
    pidFile = op.join(lib.appconst.PATHS['user'], 'jpa.pid')
    import lib.config
    lib.appconst.CFG = lib.config.AppConfig(op.join(lib.appconst.PATHS['user'],
        'jpa.cfg'))
    cfg = lib.appconst.CFG
    runSingle = (cfg.getOption('misc', 'single_instance', '1') == '1')
    if runSingle:
        if os.name == 'nt':
            try:
                from lib.w32_singleinstance import SingleInstance
                instance = SingleInstance()
                if instance.alreadyRunning():
                    sys.exit(0)
            except ImportError:
                # no win32 libraries, just continue
                pass
        else:
            import fcntl
            fp = open(pidFile, 'w')
            try:
                fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                # another instance is running
                sys.exit(0)
    import pygtk
    pygtk.require('2.0')
    import gtk, gobject, gtk.glade
    gobject.threads_init()
    import gettext, locale
    locale.setlocale(locale.LC_ALL, '')
    if os.name == 'nt':
        # windows hack for locale setting
        lang = os.getenv('LANG')
        if lang is None:
            defaultLang, defaultEnc = locale.getdefaultlocale()
            if defaultLang:
                lang = defaultLang
        if lang:
            os.environ['LANG'] = lang
    gtk.glade.bindtextdomain('jpa', lib.appconst.PATHS['i18n'])
    gtk.glade.textdomain('jpa')
    gettext.install('jpa', lib.appconst.PATHS['i18n'], unicode=True)
    from lib.jpa import JPAApplication
    app = JPAApplication()
    gtk.main()
    if op.isfile(pidFile):
        os.unlink(pidFile)
