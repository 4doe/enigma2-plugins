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
Extensions/UShare/Makefile
Extensions/MyTube/Makefile
Extensions/nStreamVOD/Makefile
Extensions/nStreamVOD/img/Makefile
Extensions/nStreamVOD/img/playlist/Makefile
Extensions/nStreamVOD/Moduls/Makefile
Extensions/1channel/Makefile
Extensions/CoolTVGuide/Makefile
Extensions/CoolTVGuide/Cool3D/Makefile
Extensions/CoolTVGuide/Cool3D/Menu/Makefile
Extensions/CoolTVGuide/Cool3D/Standard/Makefile
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
Extensions/CoolTVGuide/locale/nl/Makefile
Extensions/CoolTVGuide/locale/nl/LC_MESSAGES/Makefile
Extensions/CoolTVGuide/locale/no/Makefile
Extensions/CoolTVGuide/locale/no/LC_MESSAGES/Makefile
Extensions/CoolTVGuide/locale/pl/Makefile
Extensions/CoolTVGuide/locale/pl/LC_MESSAGES/Makefile
])
