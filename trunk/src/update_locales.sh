#! /bin/sh

intltool-extract --type=gettext/glade share/jpa2.glade
xgettext -k_ -kN_ -o src/locale/messages.pot lib/*.py share/jpa2.glade.h
msgmerge -U src/locale/pl.po src/locale/messages.pot
/usr/bin/vim src/locale/pl.po
msgfmt src/locale/pl.po -o share/locale/pl/LC_MESSAGES/jpa.mo

