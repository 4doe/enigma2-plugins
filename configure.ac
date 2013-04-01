AC_INIT(plugins,0.0.1)
AM_INIT_AUTOMAKE(plugins,0.0.1)

TUXBOX_APPS_DIRECTORY

AM_PATH_PYTHON()
AC_PYTHON_DEVEL

AC_PROG_CXX

AC_PATH_PROG(MSGFMT, msgfmt, AC_MSG_ERROR(Could not find msgfmt))

AC_ARG_WITH(boxtype,
	[  --with-boxtype=NAME box type [[none,dm7025,dm800...]]],
	[BOXTYPE="$withval"],[BOXTYPE="dm800"])

AC_SUBST(BOXTYPE)
AC_DEFINE_UNQUOTED(BOXTYPE,"$BOXTYPE",[box type])

AM_CONDITIONAL([DM8000], [test "$BOXTYPE" = "dm8000"])
AM_CONDITIONAL([DM7025], [test "$BOXTYPE" = "dm7025"])

AC_ARG_WITH(po,
	AS_HELP_STRING([--with-po],[enable updating of po files]),
	[with_po="$withval"],[with_po="no"])
if test "$with_po" = "yes"; then
	AC_PATH_PROG(MSGINIT, msginit)
	AC_PATH_PROG(MSGMERGE, msgmerge)
	AC_PATH_PROG(MSGUNIQ, msguniq)
	AC_PATH_PROG(XGETTEXT, xgettext)
	if test -z "$MSGINIT" -o -z "$MSGMERGE" -o -z "$MSGUNIQ" -o -z "$XGETTEXT"; then
		AC_MSG_ERROR([Could not find required gettext tools])
	fi
fi
AM_CONDITIONAL(UPDATE_PO, test "$with_po" = "yes")

AC_OUTPUT([
Makefile
PLi/Makefile
PLi/SoftcamSetup/Makefile
PLi/SoftcamSetup/src/Makefile
PLi/SoftcamSetup/po/Makefile
PLi/SnmpAgent/Makefile
Extensions/Makefile
Extensions/AutoBouquets/Makefile
Extensions/icefilms/Makefile
Extensions/icefilms/resolvers/Makefile
Extensions/UShare/Makefile
Extensions/OnDemand/Makefile
Extensions/OnDemand/icons/Makefile
xtensions/PlayStream/Makefile
Extensions/PlayStream/streams/Makefile
Extensions/TSonlineTV/Makefile
Extensions/TSonlineTV/img/Makefile
Extensions/TSonlineTV/picons/Makefile
Extensions/nStreamVOD/Makefile
Extensions/nStreamVOD/img/Makefile
Extensions/nStreamVOD/img/playlist/Makefile
Extensions/nStreamVOD/Moduls/Makefile
Extensions/1channel/Makefile
Extensions/SHOUTcast/Makefile
Extensions/SHOUTcast/locale/Makefile
Extensions/SHOUTcast/locale/de/Makefile
Extensions/SHOUTcast/locale/de/LC_MESSAGES/Makefile
Extensions/SHOUTcast/locale/it/Makefile
Extensions/SHOUTcast/locale/it/LC_MESSAGES/Makefile
Extensions/CoolTVGuide/Makefile
Extensions/CoolTVGuide/Cool3D/Makefile
Extensions/CoolTVGuide/Cool3D/Menu/Makefile
Extensions/CoolTVGuide/Cool3D/Standard/Makefile
Extensions/CoolTVGuide/Cool3D/MyDesign/Makefile
Extensions/CoolTVGuide/CoolSkin/Makefile
Extensions/CoolTVGuide/locale/Makefile
Extensions/CoolTVGuide/locale/bg/Makefile
Extensions/CoolTVGuide/locale/bg/LC_MESSAGES/Makefile
Extensions/CoolTVGuide/locale/cs/Makefile
Extensions/CoolTVGuide/locale/cs/LC_MESSAGES/Makefile
Extensions/CoolTVGuide/locale/de/Makefile
Extensions/CoolTVGuide/locale/de/LC_MESSAGES/Makefile
Extensions/CoolTVGuide/locale/fa/Makefile
Extensions/CoolTVGuide/locale/fa/LC_MESSAGES/Makefile
Extensions/CoolTVGuide/locale/fr/Makefile
Extensions/CoolTVGuide/locale/fr/LC_MESSAGES/Makefile
Extensions/CoolTVGuide/locale/it/Makefile
Extensions/CoolTVGuide/locale/it/LC_MESSAGES/Makefile
Extensions/CoolTVGuide/locale/nl/Makefile
Extensions/CoolTVGuide/locale/nl/LC_MESSAGES/Makefile
Extensions/CoolTVGuide/locale/no/Makefile
Extensions/CoolTVGuide/locale/no/LC_MESSAGES/Makefile
Extensions/CoolTVGuide/locale/pl/Makefile
Extensions/CoolTVGuide/locale/pl/LC_MESSAGES/Makefile
Extensions/CoolTVGuide/locale/sk/Makefile
Extensions/CoolTVGuide/locale/sk/LC_MESSAGES/Makefile
Extensions/MyTube/Makefile
Extensions/PermanentTimeshift/Makefile
Extensions/PermanentTimeshift/images/Makefile
Extensions/PermanentTimeshift/locale/Makefile
Extensions/PermanentTimeshift/locale/de/Makefile
Extensions/PermanentTimeshift/locale/de/LC_MESSAGES/Makefile
Extensions/PermanentTimeshift/locale/it/Makefile
Extensions/PermanentTimeshift/locale/it/LC_MESSAGES/Makefile
Extensions/PermanentTimeshift/locale/pl/Makefile
Extensions/PermanentTimeshift/locale/pl/LC_MESSAGES/Makefile
Extensions/PermanentTimeshift/locale/ru/Makefile
Extensions/PermanentTimeshift/locale/ru/LC_MESSAGES/Makefile
Extensions/PermanentTimeshift/locale/sk/Makefile
Extensions/PermanentTimeshift/locale/sk/LC_MESSAGES/Makefile
Extensions/PPanel/Makefile
Extensions/PPanel/data/Makefile
Extensions/TSsatEditor/Makefile
Extensions/TSsatEditor/ddbuttons/Makefile
Extensions/SatelliteEquipmentControl/Makefile
SystemPlugins/Makefile
SystemPlugins/NetworkWizard/Makefile
])
#Extensions/OnDemand/locale/Makefile
#Extensions/OnDemand/locale/ar/Makefile
#Extensions/OnDemand/locale/ar/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/bg/Makefile
#Extensions/OnDemand/locale/bg/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/ca/Makefile
#Extensions/OnDemand/locale/ca/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/cs/Makefile
#Extensions/OnDemand/locale/cs/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/da/Makefile
#Extensions/OnDemand/locale/da/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/de/Makefile
#Extensions/OnDemand/locale/de/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/el/Makefile
#Extensions/OnDemand/locale/el/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/en/Makefile
#Extensions/OnDemand/locale/en/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/en_GB/Makefile
#Extensions/OnDemand/locale/en_GB/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/es/Makefile
#Extensions/OnDemand/locale/es/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/et/Makefile
#Extensions/OnDemand/locale/et/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/fa/Makefile
#Extensions/OnDemand/locale/fa/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/fi/Makefile
#Extensions/OnDemand/locale/fi/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/fr/Makefile
#Extensions/OnDemand/locale/fr/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/fy/Makefile
#Extensions/OnDemand/locale/fy/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/he/Makefile
#Extensions/OnDemand/locale/he/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/hr/Makefile
#Extensions/OnDemand/locale/hr/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/hu/Makefile
#Extensions/OnDemand/locale/hu/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/is/Makefile
#Extensions/OnDemand/locale/is/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/it/Makefile
#Extensions/OnDemand/locale/it/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/lt/Makefile
#Extensions/OnDemand/locale/lt/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/lv/Makefile
#Extensions/OnDemand/locale/lv/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/nb/Makefile
#Extensions/OnDemand/locale/nb/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/nl/Makefile
#Extensions/OnDemand/locale/nl/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/no/Makefile
#Extensions/OnDemand/locale/no/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/pl/Makefile
#Extensions/OnDemand/locale/pl/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/pt/Makefile
#Extensions/OnDemand/locale/pt/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/pt_BR/Makefile
#Extensions/OnDemand/locale/pt_BR/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/ro/Makefile
#Extensions/OnDemand/locale/ro/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/ru/Makefile
#Extensions/OnDemand/locale/ru/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/sk/Makefile
#Extensions/OnDemand/locale/sk/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/sl/Makefile
#Extensions/OnDemand/locale/sl/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/sr/Makefile
#Extensions/OnDemand/locale/sr/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/sv/Makefile
#Extensions/OnDemand/locale/sv/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/th/Makefile
#Extensions/OnDemand/locale/th/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/tr/Makefile
#Extensions/OnDemand/locale/tr/LC_MESSAGES/Makefile
#Extensions/OnDemand/locale/uk/Makefile
#Extensions/OnDemand/locale/uk/LC_MESSAGES/Makefile
