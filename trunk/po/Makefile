top_srcdir = ../
NAME = jpa
ALL_LINGUAS = pl
PREFIX ?= /usr
PO_DIR ?= $(PREFIX)/share/locale

all:

po: $(addsuffix .mo, $(ALL_LINGUAS))

jpa.pot: POTFILES.in ../*.py ../forms/*.py
	intltool-update --pot --gettext-package=$(NAME)

%.po: jpa.pot
	intltool-update --dist --gettext-package=$(NAME) $*

%.mo: %.po
	msgfmt -o $@ $<

check: $(addprefix check-, $(ALL_LINGUAS))

check-%: %.po
	msgfmt -c $<

clean:
	rm -f untitled.pot messages.mo jpa.gmo notexist missing
	rm -f *.mo

distclean: clean
	rm -f *~

install-po: po
	for F in $(ALL_LINGUAS); do mkdir -p $(DESTDIR)$(PO_DIR)/$$F/LC_MESSAGES && install -m 644 $$F.mo $(DESTDIR)$(PO_DIR)/$$F/LC_MESSAGES/$(NAME).mo; done

.PHONY: po check check-% clean mo-clean distclean install-po
