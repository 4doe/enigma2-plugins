# coding: utf-8
#===============================================================================
# PlayStream Plugin by pcd@i-have-a-dreambox  May 2012                   
#
# This is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2, or (at your option) any later
# version.
#===============================================================================

from urllib2 import urlopen
from Components.MenuList import MenuList
from Components.Label import Label

from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import NumberActionMap
from Components.Input import Input
from Components.Pixmap import Pixmap
from Components.FileList import FileList
from Screens.ChoiceBox import ChoiceBox
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Screens.InputBox import InputBox, PinInput

#from twisted.web.client import getPage, downloadPage
#from Plugins.Extensions.VlcPlayer.VlcServerConfig import vlcServerConfig

from enigma import eServiceReference
from enigma import eServiceCenter
from Screens.InfoBar import MoviePlayer
import os

from Components.Task import Task, Job, job_manager as JobManager, Condition
from Screens.TaskView import JobView
from Components.Button import Button
from Tools.Directories import fileExists, copyfile

class PlayStream(Screen):

    skin = """
		<screen position="center,center" size="550,400" title="Streams" >
			<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->
			<widget name="list" position="10,0" size="500,350" scrollbarMode="showOnDemand" />
			<!--widget name="pixmap" position="200,0" size="190,250" /-->
			<eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />
			<widget name="info" position="100,230" zPosition="4" size="300,25" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />
		</screen>"""

    def __init__(self, session):
		self.skin = PlayStream.skin
		Screen.__init__(self, session)

        	self["list"] = MenuList([])
		self["info"] = Label()
                self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.okClicked, "cancel": self.cancel}, -1)
                self.data = []
                self.names = []
                self.urls = []
                self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
                self.onLayoutFinish.append(self.stream)
                

    def stream(self):
                path = "/usr/lib/enigma2/python/Plugins/Extensions/PlayStream/streams"
                self.streamlist = []
		for root, dirs, files in os.walk(path):
			for name in files:
                                self.streamlist.append(name)
             
                self["list"].setList(self.streamlist)
                
    def cancel(self):
		self.session.nav.playService(self.srefOld)
		self.close()
	
    def keyRight(self):
		self["text"].right()
		
    def okClicked(self):
		itype = self["list"].getSelectionIndex()
		sfile = self.streamlist[itype]
                self.session.open(Streamurl, sfile) 
	
    def keyNumberGlobal(self, number):
		print "pressed", number
		self["text"].number(number)
		
class Streamurl(Screen):

    skin = """
		<screen position="center,center" size="550,400" title="Streams" >
			<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->
			<widget name="list" position="10,0" size="500,350" scrollbarMode="showOnDemand" />
			<!--widget name="pixmap" position="200,0" size="190,250" /-->
			<eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />
			<widget name="info" position="100,230" zPosition="4" size="300,25" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />
		</screen>"""

    def __init__(self, session, sfile):
		self.skin = PlayStream.skin
		Screen.__init__(self, session)

        	self["list"] = MenuList([])
		self["info"] = Label()
                self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.okClicked, "cancel": self.cancel}, -1)
                self.sfile = sfile
                self.data = []
                self.names = []
                self.urls = []
                self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
                self.onLayoutFinish.append(self.stream)
                

    def stream(self):
                slist = "/usr/lib/enigma2/python/Plugins/Extensions/PlayStream/streams/" + self.sfile
                print "slist =", slist
                myfile = open(slist, "r")
                icount = 0
                for line in myfile.readlines():
                         print "line =", line
                         self.data.append(icount)
                         self.data[icount] = line[:-1]
                         icount = icount+1
                n = len(self.data)
                n1 = n/2
                print "n1 = ", n1
                i = 0
                j = 0
                k = 0
                while i<n1:
                         j = i*2
                         k = i*2 + 1
                         self.names.append(i)
                         self.names[i] = self.data[j]
                         self.urls.append(i)
                         self.urls[i] = self.data[k]
                         
                         i = i+1
              
                self["list"].setList(self.names)
                
    def cancel(self):
		self.session.nav.playService(self.srefOld)
		self.close()
	
    def keyRight(self):
		self["text"].right()
		
    def okClicked(self):
		itype = self["list"].getSelectionIndex()
		url = self.urls[itype]
		name = self.names[itype]
		if "rtmp" in url:
                       self.session.open(Showstream, name, url)

		else:
                       name = " "
                       pvid = Playvid(self.session, name, url)
                       pvid.openTest()		
	
    def keyNumberGlobal(self, number):
		print "pressed", number
		self["text"].number(number)
	
                                    
class Showstream(Screen):

    skin = """
		<screen position="center,center" size="400,300" title="Play Options" >
			<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->
			<widget name="list" position="10,0" size="300,200" scrollbarMode="showOnDemand" />
			<!--widget name="pixmap" position="200,0" size="190,250" /-->
			<eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />
			<widget name="info" position="50,10" zPosition="4" size="200,100" font="Regular;22" foregroundColor="#ffffff" transparent="1" halign="left" valign="top" />
		        <ePixmap name="red"    position="0,250"   zPosition="2" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
	                <ePixmap name="green"  position="140,250" zPosition="2" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
	                <!--ePixmap name="yellow" position="280,450" zPosition="2" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" /> 
	                <ePixmap name="blue"   position="420,450" zPosition="2" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" /--> 

	                <widget name="key_red" position="0,250" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> 
	                <widget name="key_green" position="140,250" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> 
	                <!--widget name="key_yellow" position="280,450" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />
	                <widget name="key_blue" position="420,450" size="140,50" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /-->
                </screen>"""
  

    def __init__(self, session, name, url):
		Screen.__init__(self, session)
                self.skin = Showstream.skin
                title = "Play"
                self.setTitle(title)

        	self["list"] = MenuList([])
		self["info"] = Label()
                self["key_red"] = Button(_("Exit"))
		self["key_green"] = Button(_("Play"))
                self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "TimerEditActions"],
		{
			"red": self.stopdl,
			"green": self.okClicked,
			"cancel": self.stopdl,
			"ok": self.okClicked,
		}, -2)
                self.icount = 0
                print "Showrtmp : name =", name
                self.name = name
                self.url = url
                txt = self.name
                self["info"].setText(txt)

                self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
                self.onLayoutFinish.append(self.getrtmp)
                
                
             

    def getrtmp(self):
#            try:           
                    if not fileExists("/tmp/vid"):
			   os.system("/usr/bin/mkfifo /tmp/vid")
 
                    local_file = "/tmp/vid"

                    self.urtmp = "rtmpdump -v -r " + self.url + " -o '" + local_file + "'"


#            except:
#                    self.close()
                    

    def okClicked(self):
                svfile = "/tmp/vid"
                self.svf = svfile

                JobManager.AddJob(downloadJob(self, self.urtmp, svfile, 'Title 1')) 
                
#                self.LastJobView()
                self.play()
 
    def LastJobView(self):
		currentjob = None
		for job in JobManager.getPendingJobs():
			currentjob = job

		if currentjob is not None:
			self.session.open(JobView, currentjob)
 
    def play(self):
         try:
                print "Showrtmp here 2"
                svfile = self.svf
                pvd = Playvid(self.session, self.name, svfile)
                pvd.openTest()
         
         except:       
                return
                
    
    def cancel(self):
	        self.session.nav.playService(self.srefOld)                
                self.close()

    def stopdl(self):
                svfile = self.svf
                cmd = "rm " + svfile
                os.system(cmd)                
                self.session.nav.playService(self.srefOld)
                cmd1 = "killall -9 rtmpdump"
                cmd2 = "killall -9 wget"
                os.system(cmd1)
                os.system(cmd2)
                self.close()

 
    def keyLeft(self):
		self["text"].left()
	
    def keyRight(self):
		self["text"].right()

    def keyNumberGlobal(self, number):
		print "pressed", number
		self["text"].number(number)
		

class Playvid(Screen):

    def __init__(self, session, name, url):
		self.skin = PlayStream.skin
		Screen.__init__(self, session)

        	self["list"] = MenuList([])
		self["info"] = Label()
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "TimerEditActions"],
		{
			
			"cancel": self.cancel,
			"ok": self.okClicked,
		}, -2)
                self.icount = 0
                print "Playvid : name =", name
                print "Playvid : url =", url
                self.name = name
                self.url = url
                self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
                self.onLayoutFinish.append(self.openTest)

    def openTest(self):
          if self.url != " ": 
                url = self.url
                name = self.name
                self.session.nav.stopService()
                sref = eServiceReference(4097,0,url)
                sref.setName(name)
                print "sref =", sref.toString()
                self.session.open(MoviePlayer, sref)
          else:
                return
           

    def cancel(self):
	        self.session.nav.playService(self.srefOld)
                self.close()

    def okClicked(self):            
                return

    def keyLeft(self):
		self["text"].left()
	
    def keyRight(self):
		self["text"].right()
	
    def keyNumberGlobal(self, number):
		print "pressed", number
		self["text"].number(number)	


class downloadJob(Job):
	def __init__(self, toolbox, cmdline, filename, filetitle):
		Job.__init__(self, _("Saving Video"))
		self.toolbox = toolbox
		self.retrycount = 0
		
                downloadTask(self, cmdline, filename, filetitle)

	def retry(self):
		assert self.status == self.FAILED
		self.retrycount += 1
		self.restart()
		
class downloadJob(Job):
	def __init__(self, toolbox, cmdline, filename, filetitle):
		Job.__init__(self, _("Saving Video"))
		self.toolbox = toolbox
		self.retrycount = 0
		
                downloadTask(self, cmdline, filename, filetitle)

	def retry(self):
		assert self.status == self.FAILED
		self.retrycount += 1
		self.restart()
	
class downloadTask(Task):
	ERROR_CORRUPT_FILE, ERROR_RTMP_ReadPacket, ERROR_SEGFAULT, ERROR_SERVER, ERROR_UNKNOWN = range(5)
	def __init__(self, job, cmdline, filename, filetitle):
		Task.__init__(self, job, filetitle)
#		self.postconditions.append(downloadTaskPostcondition())
		self.setCmdline(cmdline)
		self.filename = filename
		self.toolbox = job.toolbox
		self.error = None
		self.lasterrormsg = None
		
	def processOutput(self, data):
		try:
			if data.endswith('%)'):
				startpos = data.rfind("sec (")+5
				if startpos and startpos != -1:
					self.progress = int(float(data[startpos:-4]))
			elif data.find('%') != -1:
				tmpvalue = data[:data.find("%")]
				tmpvalue = tmpvalue[tmpvalue.rfind(" "):].strip()
				tmpvalue = tmpvalue[tmpvalue.rfind("(")+1:].strip()
				self.progress = int(float(tmpvalue))
			else:
				Task.processOutput(self, data)
		except Exception, errormsg:
			print "Error processOutput: " + str(errormsg)
			Task.processOutput(self, data)

	def processOutputLine(self, line):
			self.error = self.ERROR_SERVER
			
	def afterRun(self):
		pass

class downloadTaskPostcondition(Condition):
	RECOVERABLE = True
	def check(self, task):
		if task.returncode == 0 or task.error is None:
			return True
		else:
			return False

	def getErrorMessage(self, task):
		return {
			task.ERROR_CORRUPT_FILE: _("Video Download Failed!Corrupted Download File:%s" % task.lasterrormsg),
			task.ERROR_RTMP_ReadPacket: _("Video Download Failed!Could not read RTMP-Packet:%s" % task.lasterrormsg),
			task.ERROR_SEGFAULT: _("Video Download Failed!Segmentation fault:%s" % task.lasterrormsg),
#			task.ERROR_SERVER: _("Download Failed!-Server error:%s" % task.lasterrormsg),
			task.ERROR_SERVER: _("Download Failed!-Server error:"),
			task.ERROR_UNKNOWN: _("Video Download Failed!Unknown Error:%s" % task.lasterrormsg)
		}[task.error]

#######################
		
	

 
def main(session, **kwargs):
        if not fileExists("/usr/bin/rtmpdump"):
		os.system("cp /usr/lib/enigma2/python/Plugins/Extensions/PlayStream/rtmpdump /usr/bin/ && chmod 755 /usr/bin/rtmpdump")
      
        session.open(PlayStream)

def Plugins(**kwargs):
	return PluginDescriptor(name="PlayStream", description="Streams from user urls", where = PluginDescriptor.WHERE_PLUGINMENU, fnc=main)




