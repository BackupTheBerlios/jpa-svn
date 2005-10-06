#! /usr/bin/env python
# -*- coding: UTF-8 -*-

# This file is part of JPA.
# Copyright: (C) 2003, 2004 Jarek Zgoda <jzgoda@gazeta.pl>
#
# JPA is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# JPA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JPA; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""Main program file, used to set up paths, import globals into app 
namespace etc..."""

__revision__ = '$Id'

import sys, locale
import os.path as op
import qt

basepath = op.dirname(op.dirname(op.abspath(sys.argv[0])))
__paths = {}
for subdir in ('bin', 'doc', 'lib', 'share'):
    __paths[subdir] = op.join(basepath, subdir)

sys.path.append(__paths['lib'])
import jt_const
jt_const.PATHS = __paths
del __paths

locale.setlocale(locale.LC_ALL, '')

if __name__ == '__main__':
    import qjt_main
    a = qt.QApplication(sys.argv)
    qt.QObject.connect(a, qt.SIGNAL('lastWindowClosed()'), a, qt.SLOT('quit()'))
    w = qjt_main.MainForm()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()