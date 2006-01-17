#! /bin/sh

intltool-extract --type=gettext/glade share/jpa2.glade
xgettext -k_ -kN_ -o src/locale/messages.pot lib/*.py lib/transport/*.py lib/renderer/*.py share/jpa2.glade.h
msgmerge -U src/locale/pl.po src/locale/messages.pot
gedit src/locale/pl.po
msgfmt src/locale/pl.po -o share/locale/pl/LC_MESSAGES/jpa.mo

