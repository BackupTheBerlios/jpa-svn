unix {
  UI_DIR = .ui
  MOC_DIR = .moc
  OBJECTS_DIR = .obj
}
FORMS	= mainform.ui \
	msgeditdialog.ui \
	optionsdialog.ui \
	msgimport.ui \
	aboutdialog.ui \
	applogdialog.ui \
	msghistorydialog.ui \
	msgpreviewdialog.ui \
	spellcheckdialog.ui \
	mainform2.ui \
	archviewdialog.ui \
	repleditdialog.ui \
	logindialog.ui
TEMPLATE	=app
CONFIG	+= qt warn_on release
LANGUAGE	= C++
