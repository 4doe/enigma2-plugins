# AutoBouquets E2 for satellite 28.2E
# stream bouquet downloader by LraiZer
# Development Forum - www.ukcvs.org
# version date - 1st March 2013
#=========================================
# New GUI thanks to OE-Alliance - AndyBlac
# and ViX TEAM: www.world-of-satellite.com
#=========================================

# for localized messages
from . import _

from Screens.Screen import Screen
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Components.Button import Button
from Tools.Directories import fileExists
from Plugins.Plugin import PluginDescriptor

from Components.ScrollLabel import ScrollLabel
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Pixmap import MultiPixmap
from Screens.Standby import Standby, inStandby
from enigma import eTimer, eServiceReference, eConsoleAppContainer
from datetime import date
from time import localtime, time, strftime, mktime, sleep
from os import stat, path

from Screens.ServiceScan import ServiceScan
from Components.NimManager import nimmanager, getConfigSatlist
from enigma import eComponentScan
from Screens.ScanSetup import getInitialTransponderList

arealist = []
arealist.append(("None", "Not Set"))
arealist.append(("4101 13", "Atherstone HD"))
arealist.append(("4097 13", "Atherstone SD"))
arealist.append(("4101 0c", "Border England HD"))
arealist.append(("4097 0c", "Border England SD"))
arealist.append(("4102 24", "Border Scotland HD"))
arealist.append(("4098 24", "Border Scotland SD"))
arealist.append(("4103 41", "Brighton HD"))
arealist.append(("4099 41", "Brighton SD"))
arealist.append(("4101 03", "Central Midlands HD"))
arealist.append(("4097 03", "Central Midlands SD"))
arealist.append(("4104 22", "Channel Isles HD"))
arealist.append(("4100 22", "Channel Isles SD"))
arealist.append(("4101 14", "East Midlands HD"))
arealist.append(("4097 14", "East Midlands SD"))
arealist.append(("4101 02", "Essex HD"))
arealist.append(("4097 02", "Essex SD"))
arealist.append(("4101 18", "Gloucester HD"))
arealist.append(("4097 18", "Gloucester SD"))
arealist.append(("4102 23", "Grampian HD"))
arealist.append(("4098 23", "Grampian SD"))
arealist.append(("4101 07", "Granada HD"))
arealist.append(("4097 07", "Granada SD"))
arealist.append(("4103 46", "Henley On Thames HD"))
arealist.append(("4099 46", "Henley On Thames SD"))
arealist.append(("4103 2b", "HTV Wales HD"))
arealist.append(("4099 2b", "HTV Wales SD"))
arealist.append(("4101 04", "HTV West HD"))
arealist.append(("4097 04", "HTV West SD"))
arealist.append(("4103 3f", "HTV West / Thames Valley HD"))
arealist.append(("4099 3f", "HTV West / Thames Valley SD"))
arealist.append(("4101 1d", "Humber HD"))
arealist.append(("4097 1d", "Humber SD",))
arealist.append(("4101 01", "London HD"))
arealist.append(("4097 01", "London SD"))
arealist.append(("4101 12", "London / Essex HD"))
arealist.append(("4097 12", "London / Essex SD"))
arealist.append(("4103 42", "London / Thames Valley HD"))
arealist.append(("4099 42", "London / Thames Valley SD"))
arealist.append(("4103 40", "London Kent HD"))
arealist.append(("4099 40", "London Kent SD"))
arealist.append(("4101 0b", "Meridian East HD"))
arealist.append(("4097 0b", "Meridian East SD"))
arealist.append(("4103 44", "Meridian North HD"))
arealist.append(("4099 44", "Meridian North SD"))
arealist.append(("4101 05", "Meridian South HD"))
arealist.append(("4097 05", "Meridian South SD"))
arealist.append(("4101 0a", "Meridian South East HD"))
arealist.append(("4097 0a", "Meridian South East SD"))
arealist.append(("4103 2d", "Merseyside HD"))
arealist.append(("4099 2d", "Merseyside SD"))
arealist.append(("4101 15", "Norfolk HD"))
arealist.append(("4097 15", "Norfolk SD"))
arealist.append(("4103 3e", "North East Midlands HD"))
arealist.append(("4099 3e", "North East Midlands SD"))
arealist.append(("4101 08", "North West Yorkshire HD"))
arealist.append(("4097 08", "North West Yorkshire SD"))
arealist.append(("4101 1a", "North Yorkshire HD"))
arealist.append(("4097 1a", "North Yorkshire SD"))
arealist.append(("4104 21", "Northern Ireland HD"))
arealist.append(("4100 21", "Northern Ireland SD"))
arealist.append(("4103 47", "Oxford HD"))
arealist.append(("4099 47", "Oxford SD"))
arealist.append(("4104 32", "Republic of Ireland HD"))
arealist.append(("4100 32", "Republic of Ireland SD"))
arealist.append(("4103 29", "Ridge Hill HD"))
arealist.append(("4099 29", "Ridge Hill SD"))
arealist.append(("4103 3d", "Scarborough HD"))
arealist.append(("4099 3d", "Scarborough SD"))
arealist.append(("4102 25", "Scottish East HD"))
arealist.append(("4098 25", "Scottish East SD"))
arealist.append(("4102 26", "Scottish West HD"))
arealist.append(("4098 26", "Scottish West SD"))
arealist.append(("4103 3c", "Sheffield HD"))
arealist.append(("4099 3c", "Sheffield SD"))
arealist.append(("4101 1c", "South Lakeland HD"))
arealist.append(("4097 1c", "South Lakeland SD"))
arealist.append(("4103 48", "South Yorkshire HD"))
arealist.append(("4099 48", "South Yorkshire SD"))
arealist.append(("4103 45", "Tees HD"))
arealist.append(("4099 45", "Tees SD"))
arealist.append(("4101 09", "Thames Valley HD"))
arealist.append(("4097 09", "Thames Valley SD"))
arealist.append(("4101 1b", "Tring HD"))
arealist.append(("4097 1b", "Tring SD"))
arealist.append(("4101 0d", "Tyne HD"))
arealist.append(("4097 0d", "Tyne SD"))
arealist.append(("4101 19", "West Anglia HD"))
arealist.append(("4097 19", "West Anglia SD"))
arealist.append(("4103 43", "West Dorset HD"))
arealist.append(("4099 43", "West Dorset SD"))
arealist.append(("4101 06", "Westcountry HD"))
arealist.append(("4097 06", "Westcountry SD"))

stylelist = []
stylelist.append(("0", "default"))
stylelist.append(("1", "style 1"))
stylelist.append(("2", "style 2"))
stylelist.append(("3", "style 3"))
stylelist.append(("4", "style 4"))
stylelist.append(("5", "style 5"))

from Components.config import config, configfile, ConfigSubsection, ConfigYesNo, ConfigSelection, ConfigText, ConfigNumber, NoSave, ConfigClock, getConfigListEntry
config.autobouquets = ConfigSubsection()
config.autobouquets.area = ConfigSelection(default = None, choices = arealist)
config.autobouquets.hdasfirst = ConfigYesNo(default = False)
config.autobouquets.numbered = ConfigYesNo(default = True)
config.autobouquets.nitscan = ConfigYesNo(default = True)
config.autobouquets.placeholder = ConfigYesNo(default = False)
config.autobouquets.parental = ConfigYesNo(default = True)
config.autobouquets.default = ConfigYesNo(default = True)
config.autobouquets.ordering = ConfigYesNo(default = False)
config.autobouquets.freetoair = ConfigYesNo(default = False)
config.autobouquets.checkscript = ConfigYesNo(default = True)
config.autobouquets.style = ConfigSelection(default = None, choices = stylelist)
config.autobouquets.schedule = ConfigYesNo(default = False)
config.autobouquets.scheduletime = ConfigClock(default = 0) # 1:00
config.autobouquets.repeattype = ConfigSelection(default = "daily", choices = [("daily", _("Daily")), ("weekly", _("Weekly")), ("monthly", _("30 Days"))])
config.autobouquets.retry = ConfigNumber(default = 30)
config.autobouquets.retrycount = NoSave(ConfigNumber(default = 0))
config.autobouquets.nextscheduletime = NoSave(ConfigNumber(default = 0))
config.autobouquets.lastlog = ConfigText(default=' ', fixed_size=False)

opt3 = " N"
scriptwasinstandby = False
autoAutoBouquetsTimer = None
defaultservice = "1:0:2:1199:7dc:2:11a0000:0:0:0:"

def AutoBouquetsautostart(reason, session=None, **kwargs):
	"called with reason=1 to during /sbin/shutdown.sysvinit, with reason=0 at startup?"
	global autoAutoBouquetsTimer
	global _session
	now = int(time())
	if reason == 0:
		print "[AutoBouquets] AutoStart Enabled"
		if session is not None:
			_session = session
			if autoAutoBouquetsTimer is None:
				autoAutoBouquetsTimer = AutoAutoBouquetsTimer(session)
	else:
		print "[AutoBouquets] Stop"
		autoAutoBouquetsTimer.stop()

class AutoAutoBouquetsTimer:
	def __init__(self, session):
		self.session = session
		self.autobouquetstimer = eTimer()
		self.autobouquetstimer.callback.append(self.AutoBouquetsonTimer)
		self.autobouquetsactivityTimer = eTimer()
		self.autobouquetsactivityTimer.timeout.get().append(self.autobouquetsdatedelay)
		now = int(time())
		global AutoBouquetsTime
		if config.autobouquets.schedule.value:
			print "[AutoBouquets] AutoBouquets Schedule Enabled at ", strftime("%c", localtime(now))
			if now > 1262304000:
				self.autobouquetsdate()
			else:
				print "[AutoBouquets] AutoBouquets Time not yet set."
				AutoBouquetsTime = 0
				self.autobouquetsactivityTimer.start(36000)
		else:
			AutoBouquetsTime = 0
			print "[AutoBouquets] AutoBouquets Schedule Disabled at", strftime("(now=%c)", localtime(now))
			self.autobouquetsactivityTimer.stop()

	def autobouquetsdatedelay(self):
		self.autobouquetsactivityTimer.stop()
		self.autobouquetsdate()

	def getAutoBouquetsTime(self):
		backupclock = config.autobouquets.scheduletime.value
		nowt = time()
		now = localtime(nowt)
		return int(mktime((now.tm_year, now.tm_mon, now.tm_mday, backupclock[0], backupclock[1], 0, now.tm_wday, now.tm_yday, now.tm_isdst)))

	def autobouquetsdate(self, atLeast = 0):
		self.autobouquetstimer.stop()
		global AutoBouquetsTime
		AutoBouquetsTime = self.getAutoBouquetsTime()
		now = int(time())
		if AutoBouquetsTime > 0:
			if AutoBouquetsTime < now + atLeast:
				if config.autobouquets.repeattype.value == "daily":
					AutoBouquetsTime += 24*3600
					while (int(AutoBouquetsTime)-30) < now:
						AutoBouquetsTime += 24*3600
				elif config.autobouquets.repeattype.value == "weekly":
					AutoBouquetsTime += 7*24*3600
					while (int(AutoBouquetsTime)-30) < now:
						AutoBouquetsTime += 7*24*3600
				elif config.autobouquets.repeattype.value == "monthly":
					AutoBouquetsTime += 30*24*3600
					while (int(AutoBouquetsTime)-30) < now:
						AutoBouquetsTime += 30*24*3600
			next = AutoBouquetsTime - now
			self.autobouquetstimer.startLongTimer(next)
		else:
			AutoBouquetsTime = -1
		print "[AutoBouquets] AutoBouquets Time set to", strftime("%c", localtime(AutoBouquetsTime)), strftime("(now=%c)", localtime(now))
		return AutoBouquetsTime

	def backupstop(self):
		self.autobouquetstimer.stop()

	def AutoBouquetsonTimer(self):
		self.autobouquetstimer.stop()
		now = int(time())
		wake = self.getAutoBouquetsTime()
		# If we're close enough, we're okay...
		atLeast = 0
		if wake - now < 60:
			print "[AutoBouquets] AutoBouquets onTimer occured at", strftime("%c", localtime(now))
			from Screens.Standby import inStandby
			if not inStandby:
				message = _("Your STB_BOX is about to update your bouquets,\nDo you want to allow this?")
				ybox = self.session.openWithCallback(self.doAutoBouquets, MessageBox, message, MessageBox.TYPE_YESNO, timeout = 30)
				ybox.setTitle('Scheduled AutoBouquets.')
			else:
				print "[AutoBouquets] in Standby, so just running backup", strftime("%c", localtime(now))
				self.doAutoBouquets(True)
		else:
			print '[AutoBouquets] Where are not close enough', strftime("%c", localtime(now))
			self.autobouquetsdate(60)

	def doAutoBouquets(self, answer):
		now = int(time())
		if answer is False:
			if config.autobouquets.retrycount.value < 2:
				print '[AutoBouquets] Number of retries',config.autobouquets.retrycount.value
				print "[AutoBouquets] AutoBouquets delayed."
				repeat = config.autobouquets.retrycount.value
				repeat += 1
				config.autobouquets.retrycount.value = repeat
				AutoBouquetsTime = now + (int(config.autobouquets.retry.value) * 60)
				print "[AutoBouquets] AutoBouquets Time now set to", strftime("%c", localtime(AutoBouquetsTime)), strftime("(now=%c)", localtime(now))
				self.autobouquetstimer.startLongTimer(int(config.autobouquets.retry.value) * 60)
			else:
				atLeast = 60
				print "[AutoBouquets] Enough Retries, delaying till next schedule.", strftime("%c", localtime(now))
				self.session.open(MessageBox, _("Enough Retries, delaying till next schedule."), MessageBox.TYPE_INFO, timeout = 10)
				config.autobouquets.retrycount.value = 0
				self.autobouquetsdate(atLeast)
		else:
			print "[AutoBouquets] Running AutoBouquets", strftime("%c", localtime(now))
			from Screens.Standby import inStandby
			global scriptwasinstandby
			if inStandby:
				scriptwasinstandby = True
				self.wasinstandby = True
				inStandby.Power()
			else:
				scriptwasinstandby = False
				self.wasinstandby = False
			self.timer = eTimer()
			self.timer.callback.append(self.doautostartscan)
			self.timer.start(10000, 1)

	def doautostartscan(self):
		self.AutoBouquets = AutoBouquets(self.session)
		postScanService = self.session.nav.getCurrentlyPlayingServiceReference()
		self.timer = eTimer()
		global opt3
		if config.autobouquets.nitscan.getValue():
			opt3 = " Y"
			self.timer.callback.append(self.AutoBouquets.go())
		else:
			self.timer.callback.append(self.AutoBouquets.startservicescan(postScanService, self.wasinstandby))
		self.timer.start(5000, 1)

class AutoBouquets(Screen):
	skin = """
		<screen position="center,center" size="365,370" title="AutoBouquets E2 for 28.2E" >
			<widget name="key_red" position="25,0" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="white" font="Regular;18" transparent="1"/>
			<widget name="key_green" position="200,0" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="white" font="Regular;18" transparent="1"/>
			<widget name="key_yellow" position="25,40" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="white" font="Regular;18" transparent="1"/>
			<widget name="key_blue" position="200,40" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="white" font="Regular;18" transparent="1"/>
			<ePixmap name="red" position="25,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
			<ePixmap name="green" position="200,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
			<ePixmap name="yellow" position="24,40" zPosition="2" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
			<ePixmap name="blue" position="200,40" zPosition="2" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/key_menu.png" position="25,90" size="35,25" alphatest="blend" transparent="1" zPosition="3" />
			<ePixmap pixmap="skin_default/buttons/key_info.png" position="70,90" size="35,25" alphatest="blend" transparent="1" zPosition="3" />
			<widget name="area" position="0,130" size="140,30" font="Regular; 22" halign="right" zPosition="2" transparent="0" />
			<widget name="areavalue" position="150,130" size="205,30" font="Regular;22" zPosition="2" />
			<widget name="hd" position="0,170" size="140,30" font="Regular; 22" halign="right" zPosition="2" transparent="0" />
			<widget name="hdcheck" position="150,170" size="32,32" alphatest="on" zPosition="1" pixmaps="skin_default/icons/lock_off.png,skin_default/icons/lock_on.png"/>
			<widget name="num" position="180,170" size="140,30" font="Regular; 22" halign="right" zPosition="2" transparent="0" />
			<widget name="numcheck" position="330,170" size="32,32" alphatest="on" zPosition="1" pixmaps="skin_default/icons/lock_off.png,skin_default/icons/lock_on.png"/>
			<widget name="nit" position="0,210" size="140,30" font="Regular; 22" halign="right" zPosition="2" transparent="0" />
			<widget name="nitcheck" position="150,210" size="32,32" alphatest="on" zPosition="1" pixmaps="skin_default/icons/lock_off.png,skin_default/icons/lock_on.png"/>
			<widget name="placeh" position="180,210" size="140,30" font="Regular; 22" halign="right" zPosition="2" transparent="0" />
			<widget name="placehcheck" position="330,210" size="32,32" alphatest="on" zPosition="1" pixmaps="skin_default/icons/lock_off.png,skin_default/icons/lock_on.png"/>
			<widget name="parental" position="0,250" size="140,30" font="Regular; 22" halign="right" zPosition="2" transparent="0" />
			<widget name="parentalcheck" position="150,250" size="32,32" alphatest="on" zPosition="1" pixmaps="skin_default/icons/lock_off.png,skin_default/icons/lock_on.png"/>
			<widget name="def" position="180,250" size="140,30" font="Regular; 22" halign="right" zPosition="2" transparent="0" />
			<widget name="defcheck" position="330,250" size="32,32" alphatest="on" zPosition="1" pixmaps="skin_default/icons/lock_off.png,skin_default/icons/lock_on.png"/>
			<widget name="ordering" position="0,290" size="140,30" font="Regular; 22" halign="right" zPosition="2" transparent="0" />
			<widget name="orderingcheck" position="150,290" size="32,32" alphatest="on" zPosition="1" pixmaps="skin_default/icons/lock_off.png,skin_default/icons/lock_on.png"/>
			<widget name="fta" position="180,290" size="140,30" font="Regular; 22" halign="right" zPosition="2" transparent="0" />
			<widget name="ftacheck" position="330,290" size="32,32" alphatest="on" zPosition="1" pixmaps="skin_default/icons/lock_off.png,skin_default/icons/lock_on.png"/>
			<widget name="status" position="0,330" size="140,30" font="Regular; 22" halign="right" zPosition="2" transparent="0" />
			<widget name="status2" position="150,330" size="205,30" font="Regular;22" zPosition="5" />
		</screen>"""

	def __init__(self, session, args = 0):
		self.session = session
		Screen.__init__(self, session)
		self['area'] = Label(_('Area:'))
		self['areavalue'] = Label()
		self['hd'] = Label(_('HD Bouquet:'))
		self['hdcheck'] = MultiPixmap()
		self['num'] = Label(_('Numbered:'))
		self['numcheck'] = MultiPixmap()
		self['nit'] = Label(_('NIT Scan:'))
		self['nitcheck'] = MultiPixmap()
		self['placeh'] = Label(_('Placeholder:'))
		self['placehcheck'] = MultiPixmap()
		self['parental'] = Label(_('Parental:'))
		self['parentalcheck'] = MultiPixmap()
		self['def'] = Label(_('Default:'))
		self['defcheck'] = MultiPixmap()
		self['ordering'] = Label(_('Custom:'))
		self['orderingcheck'] = MultiPixmap()
		self['fta'] = Label(_('FTA Only:'))
		self['ftacheck'] = MultiPixmap()
		self["status"] = Label(_("Next Update:"))
		self["status2"] = Label()

		self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Start"))
		self["key_yellow"] = Button(_("Help"))
		self["key_blue"] = Button(_("About"))

		self["myActionMap"] = ActionMap(["SetupActions", "ColorActions", "MenuActions", "TimerEditActions"],
		{
			"red": self.cancel,
			"green": self.question,
			"yellow": self.help,
			"blue": self.about,
			"cancel": self.cancel,
			"ok": self.question,
			'log': self.showLog,
			"menu": self.createSetup,
		}, -2)
		self.wasinstandby = False
		self.onLayoutFinish.append(self.doneConfiguring)

	def createSetup(self):
		self.session.openWithCallback(self.setupDone, AutoBouquetsMenu)

	def setupDone(self):
		self.doneConfiguring()

	def doneConfiguring(self):
		self['areavalue'].setText(config.autobouquets.area.getText())
		if config.autobouquets.hdasfirst.getValue():
			self['hdcheck'].setPixmapNum(1)
		else:
			self['hdcheck'].setPixmapNum(0)
		self['hdcheck'].show
		if config.autobouquets.numbered.getValue():
			self['numcheck'].setPixmapNum(1)
		else:
			self['numcheck'].setPixmapNum(0)
		self['numcheck'].show
		if config.autobouquets.nitscan.getValue():
			self['nitcheck'].setPixmapNum(1)
		else:
			self['nitcheck'].setPixmapNum(0)
		self['nitcheck'].show
		if config.autobouquets.placeholder.getValue():
			self['placehcheck'].setPixmapNum(1)
		else:
			self['placehcheck'].setPixmapNum(0)
		self['placehcheck'].show
		if config.autobouquets.parental.getValue():
			self['parentalcheck'].setPixmapNum(1)
		else:
			self['parentalcheck'].setPixmapNum(0)
		self['parentalcheck'].show
		if config.autobouquets.default.getValue():
			self['defcheck'].setPixmapNum(1)
		else:
			self['defcheck'].setPixmapNum(0)
		self['defcheck'].show
		if config.autobouquets.ordering.getValue():
			self['orderingcheck'].setPixmapNum(1)
		else:
			self['orderingcheck'].setPixmapNum(0)
		self['orderingcheck'].show
		if config.autobouquets.freetoair.getValue():
			self['ftacheck'].setPixmapNum(1)
		else:
			self['ftacheck'].setPixmapNum(0)
		self['ftacheck'].show
		now = int(time())
		if config.autobouquets.schedule.value:
			if autoAutoBouquetsTimer is not None:
				print "[AutoBouquets] AutoBouquets Schedule Enabled at", strftime("%c", localtime(now))
				autoAutoBouquetsTimer.autobouquetsdate()
		else:
			if autoAutoBouquetsTimer is not None:
				global AutoBouquetsTime
				AutoBouquetsTime = 0
				print "[AutoBouquets] AutoBouquets Schedule Disabled at", strftime("%c", localtime(now))
				autoAutoBouquetsTimer.backupstop()
		if AutoBouquetsTime > 0:
			t = localtime(AutoBouquetsTime)
			autobouquetstext = strftime(_("%a %e %b  %-H:%M"), t)
		else:
			autobouquetstext = ""
		self["status2"].setText(str(autobouquetstext))

	def showLog(self):
		self.session.open(AutoBouquetsLogView)

	def question(self):
		returnValue = config.autobouquets.area.getValue()
		self.postScanService = self.session.nav.getCurrentlyPlayingServiceReference()
		try:
			if self.postScanService.toString().find(':2:') == -1:
				self.postScanService = eServiceReference(defaultservice)
		except:
			self.postScanService = eServiceReference(defaultservice)
#		print "[AutoBouquets] postScanService: " + self.postScanService.toString()
#		print "[AutoBouquets] returnValue: " + returnValue
		if returnValue != "None":
			self.channelupdate()
		else:
			question = self.session.open(MessageBox,_('Please first setup, by pressing menu button'), MessageBox.TYPE_INFO)
			question.setTitle(_("AutoBouquets E2 for 28.2E"))

	def channelupdate(self):
		if config.autobouquets.nitscan.getValue():
			message = _("Do you want to perform a NIT scan")
		else:
			message = _("Do you want to perform a service scan")
		self.question = self.session.openWithCallback(self.updatecallback,MessageBox,message, MessageBox.TYPE_YESNO)
		self.question.setTitle(_("AutoBouquets E2 for 28.2E"))

	def updatecallback(self, val):
		global opt3
		if val:
			if config.autobouquets.nitscan.getValue():
				opt3 = " Y"
				self.go()
			else:
				opt3 = " N"
				self.startservicescan(self.postScanService)
		else:
			opt3 = " N"
			self.go()

	def startservicescan(self, postScanService=None, wasinstandby=False):
		self.wasinstandby = wasinstandby
		self.postScanService = postScanService

		tlist = []
		known_networks = [ ]
		nims_to_scan = [ ]

		for nim in nimmanager.nim_slots:
			# collect networks provided by this tuner
			need_scan = False
			networks = self.getNetworksForNim(nim)

			# we only need to scan on the first tuner which provides a network.
			# this gives the first tuner for each network priority for scanning.
			for x in networks:
				if x not in known_networks:
					need_scan = True
					print x, "not in ", known_networks
					known_networks.append(x)

# 			print "nim %d provides" % nim.slot, networks
# 			print "known:", known_networks
#
			# don't offer to scan nims if nothing is connected
			if not nimmanager.somethingConnected(nim.slot):
				need_scan = False

			if need_scan:
				nims_to_scan.append(nim)

		# we save the config elements to use them on keyGo
		self.nim_enable = [ ]

		if len(nims_to_scan):
			for nim in nims_to_scan:
				nimconfig = ConfigYesNo(default = True)
				nimconfig.nim_index = nim.slot
				self.nim_enable.append(nimconfig)

		self.scanList = []
		self.known_networks = set()
		self.nim_iter=0
		self.buildTransponderList()

	def getNetworksForNim(self, nim):
		networks = [ ]
		if nim.isCompatible("DVB-S"):
			tmpnetworks = nimmanager.getSatListForNim(nim.slot)
			for x in tmpnetworks:
				if x[0] == 282:
					networks.append(x)
		else:
			# empty tuners provide no networks.
			networks = [ ]
		return networks

	def buildTransponderList(self): # this method is called multiple times because of asynchronous stuff
		APPEND_NOW = 0
		SEARCH_CABLE_TRANSPONDERS = 1
		action = APPEND_NOW

		n = self.nim_iter < len(self.nim_enable) and self.nim_enable[self.nim_iter] or None
		self.nim_iter += 1
		if n:
			if n.value: # check if nim is enabled
				flags = 0
				nim = nimmanager.nim_slots[n.nim_index]
				networks = set(self.getNetworksForNim(nim))
				networkid = 0
				# don't scan anything twice
				networks.discard(self.known_networks)

				tlist = [ ]
				if nim.isCompatible("DVB-S"):
					# get initial transponders for each satellite to be scanned
					for sat in networks:
						getInitialTransponderList(tlist, sat[0])
				else:
					assert False
				flags |= eComponentScan.scanNetworkSearch #FIXMEEE.. use flags from cables / satellites / terrestrial.xml
				flags |= eComponentScan.scanRemoveServices

				if action == APPEND_NOW:
					self.scanList.append({"transponders": tlist, "feid": nim.slot, "flags": flags})
				elif action == SEARCH_CABLE_TRANSPONDERS:
					self.flags = flags
					self.feid = nim.slot
					self.networkid = networkid
					self.startCableTransponderSearch(nim.slot)
					return
				else:
					assert False

			self.buildTransponderList() # recursive call of this function !!!
			return
		# when we are here, then the recursion is finished and all enabled nims are checked
		# so we now start the real transponder scan
		self.startScan(self.scanList)

	def startScan(self, scanList):
		if len(scanList):
			self.timer = eTimer()
			self.start()
			self.RunServiceScan = self.session.openWithCallback(self.finished_cb, ServiceScan, scanList)

	def start(self):
		if self.finish_check not in self.timer.callback:
			self.timer.callback.append(self.finish_check)
		self.timer.startLongTimer(60)

	def stop(self):
		if self.finish_check in self.timer.callback:
			self.timer.callback.remove(self.finish_check)
		self.timer.stop()

	def finish_check(self):
		try:
			if not self.RunServiceScan["scan"].isDone():
				self.timer.startLongTimer(10)
			else:
				self.stop()
				self.RunServiceScan.close()
				self.RunServiceScan = None
		except:
			self.RunServiceScan = None
			self.stop

	def finished_cb(self):
		self.session.nav.playService(self.postScanService)
		self.go()

	def keyCancel(self):
		self.session.nav.playService(self.postScanService)
		self.close()

	def Satexists(self, tlist, pos):
		for x in tlist:
			if x == pos:
				return 1
		return 0

	def go(self):
		self.postScanService = self.session.nav.getCurrentlyPlayingServiceReference()
		try:
			if self.postScanService.toString().find(':2:') == -1:
				ref = eServiceReference(defaultservice)
				self.session.nav.playService(ref)
				self.timer = eTimer()
				self.timer.callback.append(self.doScan)
				self.timer.start(5000, 1)
			else:
				self.doScan()
		except:
			print "[AutoBouquets] script will first initialize your system!"
			self.postScanService = eServiceReference(defaultservice)
			self.doScan()

	def doScan(self):
		if config.autobouquets.hdasfirst.getValue():
			opt1 = " Y"
		else:
			opt1 = " N"
		if config.autobouquets.numbered.getValue():
			opt2 = " Y"
		else:
			opt2 = " N"
		if config.autobouquets.placeholder.getValue():
			opt4 = " Y"
		else:
			opt4 = " N"
		if config.autobouquets.parental.getValue():
			opt5 = " Y"
		else:
			opt5 = " N"
		if config.autobouquets.default.getValue():
			opt6 = " Y"
		else:
			opt6 = " N"
		if config.autobouquets.ordering.getValue():
			opt7 = " Y"
		else:
			opt7 = " N"
		if config.autobouquets.freetoair.getValue():
			opt8 = " Y"
		else:
			opt8 = " N"
		if config.autobouquets.checkscript.getValue():
			opt9 = " Y "
		else:
			opt9 = " N "
		com = "/usr/lib/enigma2/python/Plugins/Extensions/AutoBouquets/autobouquets_e2.sh "
		com += config.autobouquets.area.getValue() + opt1 + opt2 + opt3 + opt4 + opt5 + opt6 + opt7 + opt8 + opt9 + config.autobouquets.style.getValue()
		self.shcom(com)

	def shcom(self, com):
		if fileExists("/usr/bin/dvbsnoop"):
			self.session.openWithCallback(self.scancomplete,Console,_("AutoBouquets E2 for 28.2E"), ["%s" % com], closeOnSuccess=True)
		else:
			self.session.open(MessageBox,"dvbsnoop not found!",MessageBox.TYPE_ERROR)
# 			print "[AutoBouquets] dvbsnoop failed!"

	def scancomplete(self):
		if self.session.nav.getCurrentlyPlayingServiceReference() != self.postScanService:
			self.session.nav.playService(self.postScanService)
		if self.wasinstandby or scriptwasinstandby:
			from Tools import Notifications
			Notifications.AddNotification(Standby)

	def about(self):
		self.session.open(MessageBox,"AutoBouquets E2 for 28.2E\nVersion date - 01/03/2013\n\nBinary code, python coding\nfrontend scripts by LraiZer\nDeveloped by www.ukcvs.org\n\nGUI, python coding - AndyBlac\n\nThanks to ViX TEAM members\nfor feedback and beta testing\nwww.world-of-satellite.com",MessageBox.TYPE_INFO)

	def help(self):
		self.session.open(Console,_("Showing AutoBouquets readme.txt"),["cat /usr/lib/enigma2/python/Plugins/Extensions/AutoBouquets/%s" % _("readme.txt")])

	def cancel(self):
# 		print "[AutoBouquets] cancel"
		self.close(None)

class AutoBouquetsMenu(ConfigListScreen, Screen):
	skin = """
		<screen name="AutoBouquetsMenu" position="center,center" size="500,400" title="AutoBouquets Setup">
			<ePixmap pixmap="skin_default/buttons/red.png" position="90,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="265,0" size="140,40" alphatest="on" />
			<widget name="key_red" position="90,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_green" position="265,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
			<widget name="config" position="10,45" size="480,380" scrollbarMode="showOnDemand" />
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		Screen.setTitle(self, _("AutoBouquets Setup"))

		self.onChangedEntry = [ ]
		self.list = []
		ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
		self.createSetup()

		self["actions"] = ActionMap(["SetupActions", 'ColorActions', 'VirtualKeyboardActions', "MenuActions"],
		{
			"ok": self.keySave,
			"cancel": self.keyCancel,
			"red": self.keyCancel,
			"green": self.keySave,
			"menu": self.keyCancel,
		}, -2)

		self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("OK"))

	def createSetup(self):
		self.editListEntry = None
		self.list = []
		self.list.append(getConfigListEntry(_("Local Area Selection"), config.autobouquets.area))
		self.list.append(getConfigListEntry(_("Use HD First Bouquet"), config.autobouquets.hdasfirst))
		self.list.append(getConfigListEntry(_("Show Channel Numbers"), config.autobouquets.numbered))
		self.list.append(getConfigListEntry(_("Use Internal NIT Scan"), config.autobouquets.nitscan))
		self.list.append(getConfigListEntry(_("Use Pli Placeholders"), config.autobouquets.placeholder))
		self.list.append(getConfigListEntry(_("Create Child Friendly"), config.autobouquets.parental))
		self.list.append(getConfigListEntry(_("Make Default Bouquets"), config.autobouquets.default))
		self.list.append(getConfigListEntry(_("Custom Channel Swap"), config.autobouquets.ordering))
		self.list.append(getConfigListEntry(_("Scan Free To Air Only"), config.autobouquets.freetoair))
		self.list.append(getConfigListEntry(_("Enable Script Checks"), config.autobouquets.checkscript))
		self.list.append(getConfigListEntry(_("Bouquet Display Style"), config.autobouquets.style))
		self.list.append(getConfigListEntry(_("Scheduled Update Scan"), config.autobouquets.schedule))
		if config.autobouquets.schedule.value:
			self.list.append(getConfigListEntry(_("Time of Update to start"), config.autobouquets.scheduletime))
			self.list.append(getConfigListEntry(_("Repeat how often"), config.autobouquets.repeattype))
		self["config"].list = self.list
		self["config"].setList(self.list)

	# for summary:
	def changedEntry(self):
		if self["config"].getCurrent()[0] == _("Scheduled Update Scan"):
			self.createSetup()
		for x in self.onChangedEntry:
			x()

	def getCurrentEntry(self):
		return self["config"].getCurrent()[0]

	def getCurrentValue(self):
		return str(self["config"].getCurrent()[1].getText())

	def saveAll(self):
		for x in self["config"].list:
			x[1].save()
		configfile.save()

	# keySave and keyCancel are just provided in case you need them.
	# you have to call them by yourself.
	def keySave(self):
		self.saveAll()
		self.close()

	def cancelConfirm(self, result):
		if not result:
			return
		for x in self["config"].list:
			x[1].cancel()
		self.close()

	def keyCancel(self):
		if self["config"].isChanged():
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _("Really close without saving settings?"))
		else:
			self.close()

class AutoBouquetsLogView(Screen):
	skin = """
		<screen name="AutoBouquetsLogView" position="center,center" size="560,400" title="Update Log" >
			<widget name="list" position="0,0" size="560,400" font="Regular;16" />
		</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		Screen.setTitle(self, _("AutoBouquets Log"))
		if path.exists('/usr/lib/enigma2/python/Plugins/Extensions/AutoBouquets/autobouquets.log'):
			filename = '/usr/lib/enigma2/python/Plugins/Extensions/AutoBouquets/autobouquets.log'
			filedate = str(date.fromtimestamp(stat(filename).st_mtime))
			log = _('Last update') + ': ' + filedate + '\n\n'
			tmpfile = file(filename).read()
			contents = str(tmpfile)
			log = log + contents
		else:
			log = _('Last update') + ': '
		self["list"] = ScrollLabel(str(log))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "DirectionActions", "MenuActions"],
		{
			"cancel": self.cancel,
			"ok": self.cancel,
			"up": self["list"].pageUp,
			"down": self["list"].pageDown,
			"menu": self.closeRecursive,
		}, -2)

	def cancel(self):
		self.close()

	def closeRecursive(self):
		self.close(True)

class AutoBouquetsDownloader(Screen):
	skin = """
		<screen position="40,30" size="260,65" title="AutoBouquets E2 for 28.2E" flags="wfNoBorder" >
			<widget name="action" halign="center" valign="center" position="10,10" size="240,20" font="Regular;18" backgroundColor="#11000000" transparent="1" />
			<widget name="status" halign="center" valign="center" position="10,35" size="240,20" font="Regular;18" backgroundColor="#11000000" transparent="1" />
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self["action"] = Label(_("AutoBouquets E2 28.2E"))
		self["status"] = Label(  "downloading bouquets")
		if config.autobouquets.hdasfirst.getValue():
			opt1 = " Y"
		else:
			opt1 = " N"
		if config.autobouquets.numbered.getValue():
			opt2 = " Y"
		else:
			opt2 = " N"
		if config.autobouquets.placeholder.getValue():
			opt4 = " Y"
		else:
			opt4 = " N"
		if config.autobouquets.parental.getValue():
			opt5 = " Y"
		else:
			opt5 = " N"
		if config.autobouquets.default.getValue():
			opt6 = " Y"
		else:
			opt6 = " N"
		if config.autobouquets.ordering.getValue():
			opt7 = " Y"
		else:
			opt7 = " N"
		if config.autobouquets.freetoair.getValue():
			opt8 = " Y"
		else:
			opt8 = " N"
		if config.autobouquets.checkscript.getValue():
			opt9 = " Y "
		else:
			opt9 = " N "
		com = "/usr/lib/enigma2/python/Plugins/Extensions/AutoBouquets/autobouquets_e2.sh "
		com += config.autobouquets.area.getValue() + opt1 + opt2 + " Y" + opt4 + opt5 + opt6 + opt7 + opt8 + opt9 + config.autobouquets.style.getValue()
		try:
			global container
			def appClosed(retval):
				global container
				print "[AutoBouquets Downloader] FINISHED: ", retval
				container = None
				self.close()
			container = eConsoleAppContainer()
			if container.execute(com):
				raise Exception, "Script Failed: " + com
			container.appClosed.append(appClosed)
		except Exception, e:
			print "[AutoBouquets Downloader] FAILED: ", e

###########################################################################

def main(session, **kwargs):
	session.open(AutoBouquets)

def maindownloader(session, **kwargs):
	session.open(AutoBouquetsDownloader)

def mainscan(menuid, **kwargs):
	if menuid == "scan":
		return [(_("AutoBouquets (28.2E)"), main, "28.2e stream bouquet downloader", None)]
	else:
		return []

###########################################################################

def Plugins(**kwargs):
	plist = [PluginDescriptor(name="AutoBouquets E2",description="28.2e stream bouquet downloader",where = PluginDescriptor.WHERE_PLUGINMENU,icon="autobouquets.png", fnc=main)]
	plist.append(PluginDescriptor(name="AutoBouquets Downloader",description="28.2e stream bouquet downloader",where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=maindownloader))
	plist.append(PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=AutoBouquetsautostart))
	plist.append(PluginDescriptor(where=PluginDescriptor.WHERE_MENU, fnc=mainscan))
	return plist
	
