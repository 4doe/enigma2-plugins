# ---- coding: utf-8 --
###########################################################################
##################### By:subixonfire  www.satforum.me #####################
###########################################################################
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.InfoBar import MoviePlayer as MP_parent
from Screens.InfoBar import InfoBar
from Screens.MessageBox import MessageBox
from ServiceReference import ServiceReference
from enigma import eServiceReference, eConsoleAppContainer, ePicLoad, getDesktop, eServiceCenter
from Components.MenuList import MenuList
from Screens.MessageBox import MessageBox
from Components.Input import Input
from Screens.InputBox import InputBox
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel
from cookielib import CookieJar
import urllib, urllib2, re, time, os
from urllib2 import Request, urlopen, URLError, HTTPError



###########################################################################
class ShowHelp(Screen):
    wsize = getDesktop(0).size().width() - 200
    hsize = getDesktop(0).size().height() - 300
    
    skin = """
        <screen position="100,150" size=\"""" + str(wsize) + "," + str(hsize) + """\" title="1channel" >
        <widget name="myLabel" position="10,10" size=\"""" + str(wsize - 20) + "," + str(hsize - 20) + """\" font="Console;18" />
        </screen>"""
        
    def __init__(self, session, args = None):
        self.session = session

        Screen.__init__(self, session)
        
        #Help text
        text = """
HELP:
To add links to this plugin check urllist.txt file in plugin folder.
Za dodati linkove u ovaj plugin pogledajte datoteku urllist.txt u folderu plugina.

TODO: Write some nice help text here.
        
ABOUT:

        
Thanx to/ Zahvale:
        
Satforum.me ( For being a nice litle buletinboard where we all feel like a family.)
grle @ satforum.me (Testing and finding bugs in all my plugins incl. this one.)

Posebna zahvala bosnianrasta @ satforum.me koj mi je nije dao da dišem dok nisam slozio plugin za letmewatch/1channel!

Ovo je test i bugfix verzija, nije dozvoljena redistribucija iste na bilo koj način, to uključuje postavljanje  na druge forume, i/ili pakiranje iste u bilo koj E2 Img.
        """
         
        self["myLabel"] = ScrollLabel(text)
        self["myActionMap"] = ActionMap(["WizardActions", "SetupActions", "ColorActions"],
        {
        "cancel": self.close,
        "ok": self.close,
        "up": self["myLabel"].pageUp,
		"down": self["myLabel"].pageDown,
        }, -1)
###########################################################################
class MyMenux(Screen):
    wsize = getDesktop(0).size().width() - 200
    hsize = getDesktop(0).size().height() - 300
    
    skin = """
        <screen position="100,150" size=\"""" + str(wsize) + "," + str(hsize) + """\" title="1channel" >
        <widget name="myMenu" position="10,10" size=\"""" + str(wsize - 20) + "," + str(hsize - 20) + """\" scrollbarMode="showOnDemand" />
        </screen>"""
            

        
    def __init__(self, session, action, value):
        
        self.session = session

        self.action = action
        
        self.value = value
        
        
        osdList = []
        
        if self.action is "start":
            osdList.append((_("Movie"), "movie"))
            osdList.append((_("Tv Show"), "tvshow"))
            osdList.append((_("Userlist"), "userlist"))
            osdList.append((_("Kill all downloads!!!"), "kill"))
        
        elif self.action is "userlist":    
            urlList = open(os.path.dirname( __file__ ) + "/urllist.txt", 'r')
            urlData = urlList.readlines()
            for urlLine in urlData:
                if not urlLine.startswith("#"): 
                    urlLine = urlLine.split("; ")
                    osdList.append((_(urlLine[0]), urlLine[1]))
        
        elif self.action is "movie" or "tvshow":
            osdList = [(' --- 123 --- ', '123'), (' ---- A ---- ', 'a'), (' ---- B ---- ', 'b'), (' ---- C ---- ', 'c'), (' ---- D ---- ', 'd'), (' ---- E ---- ', 'e'), (' ---- F ---- ', 'f'), (' ---- G ---- ', 'g'), (' ---- H ---- ', 'h'), (' ----  I  ---- ', 'i'), (' ---- J ---- ', 'j'), (' ---- K ---- ', 'K'), (' ---- L ---- ', 'l'), (' ---- M ---- ', 'm'), (' ---- N ---- ', 'n'), (' ---- O ---- ', 'o'), (' ---- P ---- ', 'p'), (' ---- Q ---- ', 'q'), (' ---- R ---- ', 'r'), (' ---- S ---- ', 's'), (' ---- T ---- ', 't'), (' ---- U ---- ', 'u'), (' ---- V ---- ', 'v'), (' ---- W ---- ', 'w'),  (' ---- X ---- ', 'x'), (' ---- Y ---- ', 'y'), (' ---- Z ---- ', 'z'),('Search', 'search')]
            
        elif self.action is "page":
            print "########PMOVIE#################" + self.value
            page = self.value
            url = "http://www.1channel.ch/index.php?letter=" + page + "&sort=alphabet&page=1"
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            pages = (re.compile ('<a href="/index.php\?letter=.+?&sort=alphabet&page=([0-9]*)"> >> </a>').findall(htmlDoc))
     
            for page in range(int(pages[0]) / 5):
                page = int(page + 1) * 5
                osdList.append((_("Page " + str(page - 4) + " - " + str(page) ), "page"))
            
               
        osdList.append((_("Help & About"), "help"))
        osdList.append((_("Exit"), "exit"))
        
        Screen.__init__(self, session)
        self["myMenu"] = MenuList(osdList)
        self["myActionMap"] = ActionMap(["SetupActions"],
        {
        "ok": self.go,
        "cancel": self.cancel
        }, -1)    
        
    
    def go(self):
        returnValue = self["myMenu"].l.getCurrentSelection()[1]
        returnValue2 = self["myMenu"].l.getCurrentSelection()[1] + "," + self["myMenu"].l.getCurrentSelection()[0] 
        
        if returnValue is "help":
                self.session.open(ShowHelp)
        elif returnValue is "exit":
                self.close(None)
            
        
        elif self.action is "start":
            if returnValue is "movie":
                self.session.open(MyMenux, "movie", "0")
            elif returnValue is "tvshow":
                self.session.open(MyMenux, "tvshow", "0")
            elif returnValue is "userlist":
                self.session.open(MyMenux, "userlist", "0")
            elif returnValue is "kill":
                os.system("killall -9 wget")
        
        elif self.action is "userlist":
            value = returnValue2
            self.session.open(MovieSource, "userlist", value)
                
        elif self.action is "movie":
            if returnValue is "search":
                print "search"
                self.Search1()
            else:     
                value = returnValue
                self.session.open(MyMenu2, "movie", value)
            
        elif self.action is "tvshow":
            if returnValue is "search":
                print "search"
                self.Search2()
            else:     
                value = returnValue
                self.session.open(MyMenu2, "tvshow", value)
    
    def Search1(self):
        self.session.openWithCallback(self.askForWord1, InputBox, title=_("Search:"), text=" " * 55, maxSize=55, type=Input.TEXT)
       
    def askForWord1(self, returnValue):
        if returnValue is None:
            pass
        else:
            value = "search " + returnValue
            self.session.open(MyMenu2, "movie", value)
            
    def Search2(self):
        self.session.openWithCallback(self.askForWord2, InputBox, title=_("Search:"), text=" " * 55, maxSize=55, type=Input.TEXT)
       
    def askForWord2(self, returnValue):
        if returnValue is None:
            pass
        else:
            value = "search " + returnValue
            self.session.open(MyMenu2, "tvshow", value)       
    
         
                   
    def cancel(self):
        self.close(None)
        
                    
###########################################################################
class MyMenu2(Screen):
    wsize = getDesktop(0).size().width() - 200
    hsize = getDesktop(0).size().height() - 300
    
    skin = """
        <screen position="100,150" size=\"""" + str(wsize) + "," + str(hsize) + """\" title="1channel" >
        <widget name="myMenu" position="10,10" size=\"""" + str(wsize - 20) + "," + str(hsize - 20) + """\" scrollbarMode="showOnDemand" />
        </screen>"""
            

        
    def __init__(self, session, action, value):
        
        self.session = session

        self.action = action
        
        self.value = value
        
        osdList = []
        
        if self.action is "movie":
            if (value.find("search") > -1 ):
                value = value[7:]
                value = str(value.strip ())
                print value
                value = str(value.replace(" ", "+"))
                print value
                url = "http://www.1channel.ch/index.php"
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                searchkey = (re.compile ('<input type="hidden" name="key" value="(.+?)" />').findall(htmlDoc))
                url = "http://www.1channel.ch/index.php?search_keywords=" + value + "&key=" + searchkey[0] + "&sort=alphabet&search_section=1"
                print htmlDoc
                restring = '<a href=.+?&page=([0-9]*)"> >> </a>'
                self.value = "search" + "-" + value + "-" + searchkey[0] 
            else:    
                page = self.value
                url = "http://www.1channel.ch/index.php?letter=" + page + "&sort=alphabet&page=1"
                restring = '<a href="/index.php\?letter=.+?&sort=alphabet&page=([0-9]*)"> >> </a>'
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            pages = (re.compile (restring).findall(htmlDoc))
            
            
        if self.action is "tvshow":
            if (value.find("search") > -1 ):
                value = value[7:]
                value = str(value.strip ())
                print value
                value = str(value.replace(" ", "+"))
                print value
                url = "http://www.1channel.ch/index.php?tv="
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                searchkey = (re.compile ('<input type="hidden" name="key" value="(.+?)" />').findall(htmlDoc))
                url = "http://www.1channel.ch/index.php?search_keywords=" + value + "&key=" + searchkey[0] + "&sort=alphabet&search_section=2"
                print htmlDoc
                restring = '<a href=.+?&page=([0-9]*)"> >> </a>'
                self.value = "search" + "-" + value + "-" + searchkey[0] 
            else:    
                page = self.value
                url = "http://www.1channel.ch/index.php?letter=" + page + "&tv=&sort=alphabet&page=1"
                restring = '<a href="/index.php\?letter=.+?&tv=&sort=alphabet&page=([0-9]*)"> >> </a>'
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            pages = (re.compile (restring).findall(htmlDoc))
            
            
            
        if not pages:
            pages =["1"]
                
        page_x = 0     
        for page in range(int(pages[0]) / 5):
            page = int(page + 1) * 5
            if page < int(pages[0]):
                page_str = str(page - 4) + " - " + str(page) 
                osdList.append((_("Page " + page_str), self.value + "," + page_str))
                page_x = page
        if int(pages[0]) - page_x is 1 or 2 or 3 or 4:
            page_str =  str(page_x + 1) + " - " + pages[0]
            osdList.append((_("Page " + page_str ), self.value + "," + page_str))        
            
               
        osdList.append((_("Help & About"), "help"))
        osdList.append((_("Exit"), "exit"))
        
        Screen.__init__(self, session)
        self["myMenu"] = MenuList(osdList)
        self["myActionMap"] = ActionMap(["SetupActions"],
        {
        "ok": self.go,
        "cancel": self.cancel
        }, -1)    
        
    
    def go(self):
        returnValue = self["myMenu"].l.getCurrentSelection()[1]
        
        if returnValue is "help":
            self.session.open(ShowHelp)
        elif returnValue is "exit":
            self.close(None)
        else:
            value = returnValue
            self.session.open(MovieList, self.action, value)  
            print value      
        
            
    def cancel(self):
        self.close(None)
                         
###########################################################################
class MovieList(Screen):
    wsize = getDesktop(0).size().width() - 200
    hsize = getDesktop(0).size().height() - 300
    
    skin = """
        <screen position="100,150" size=\"""" + str(wsize) + "," + str(hsize) + """\" title="1channel (button green Subtitle player)" >
        <widget name="myMenu" position="10,10" size=\"""" + str(wsize - 20) + "," + str(hsize - 20) + """\" scrollbarMode="showOnDemand" />
        </screen>"""
            

        
    def __init__(self, session, action, value):
        
        self.session = session

        self.action = action
        
        self.value = value
        
        osdList = []
        
        if self.action is "movie":
            self.value = self.value.split(',')
            if (self.value[0].find("search") > -1 ):
                search = self.value[0].split('-')
                value = search[1]
                searchkey = search[2]
                url = "http://www.1channel.ch/index.php?search_keywords=" + value + "&key=" + searchkey + "&search_section=1&sort=alphabet&page="    
            else:
                letter = self.value[0]
                url = "http://www.1channel.ch/index.php?letter=" + letter + "&sort=alphabet&page="
            pages = self.value[1].split(' - ')
            page_a = pages[0]
            page_b = pages[1]
            pages = int(page_b) - int(page_a) + 1
            data = []
            for x in range (pages):
                page = int(page_a)
                page_a = int(page_a) + 1 
                pageurl = url + str(page)
                print url
                reString = '<div class="index_item index_item_ie"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>(.+?)</h2>'

                req = urllib2.Request(pageurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
    	        response.close()
    	        data = data + (re.compile (reString, re.DOTALL,).findall(htmlDoc))
    	    x = 0
    	    for movie in data:
    	        osdList.append((_(movie[1][6:]), movie[0]))
    	        x = x +1
    	    print x
    	    
    	if self.action is "tvshow":
            self.value = self.value.split(',')
            if (self.value[0].find("search") > -1 ):
                search = self.value[0].split('-')
                value = search[1]
                searchkey = search[2]
                url = "http://www.1channel.ch/index.php?search_keywords=" + value + "&key=" + searchkey + "&search_section=2&sort=alphabet&page="    
            else:
                letter = self.value[0]
                url = "http://www.1channel.ch/index.php?letter=" + letter + "&tv=&sort=alphabet&page="
            pages = self.value[1].split(' - ')
            page_a = pages[0]
            page_b = pages[1]
            pages = int(page_b) - int(page_a) + 1
            data = []
            for x in range (pages):
                page = int(page_a)
                page_a = int(page_a) + 1 
                pageurl = url + str(page)
                print url
                reString = '<div class="index_item index_item_ie"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>(.+?)</h2>'

                req = urllib2.Request(pageurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
    	        response.close()
    	        data = data + (re.compile (reString, re.DOTALL,).findall(htmlDoc))
    	    x = 0
    	    for movie in data:
    	        osdList.append((_(movie[1][6:]), movie[0]))
    	        x = x +1
    	    print x
    	    
    	if not osdList:
    	    osdList.append((_("Sorry nothing found!"), "exit")) 
        
               
        osdList.append((_("Help & About"), "help"))
        osdList.append((_("Exit"), "exit"))
        
        Screen.__init__(self, session)
        self["myMenu"] = MenuList(osdList)
        self["myActionMap"] = ActionMap(["SetupActions","ColorActions"],
        {
        "green": self.ddsubtitle,
        "ok": self.go,
        "cancel": self.cancel
        }, -1)

    def ddsubtitle(self):
		returnValue = self["myMenu"].l.getCurrentSelection()[0]
		fp = open('/tmp/zasp','w')
		fp.write(str(returnValue))
		fp.close()	
		from Plugins.Extensions.DD_Subt.plugin import Mojtitle
		ref=self.session.nav.getCurrentlyPlayingServiceReference()
		self.session.open(Mojtitle, ref)	
    
    def go(self):
        returnValue = self["myMenu"].l.getCurrentSelection()[1]
        
        if returnValue is "help":
            self.session.open(ShowHelp)
        elif returnValue is "exit":
            self.close(None)
        else:
            value = returnValue  + "," + self["myMenu"].l.getCurrentSelection()[0]
            print value
            if self.action is "movie":
                self.session.open(MovieSource, "moviesource", value)      
            if self.action is "tvshow":
                print "jebigaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                self.session.open(TvEpisode, "tvepisode", value)
            
            
         
                   
    def cancel(self):
        self.close(None)
                         
###########################################################################
class TvEpisode(Screen):
    wsize = getDesktop(0).size().width() - 200
    hsize = getDesktop(0).size().height() - 300
    
    skin = """
        <screen position="100,150" size=\"""" + str(wsize) + "," + str(hsize) + """\" title="1channel" >
        <widget name="myMenu" position="10,10" size=\"""" + str(wsize - 20) + "," + str(hsize - 20) + """\" scrollbarMode="showOnDemand" />
        </screen>"""
            

        
    def __init__(self, session, action, value):
        
        self.session = session

        self.action = action
        
        self.value = value
        
        osdList = []
        
        print self.value
        
        url = "http://www.1channel.ch" + self.value.split(",")[0] 
        

        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        htmlDoc = str(response.read())
        response.close()

        links = (re.compile (' <div class="tv_episode_item"> <a href="(.+?)">(.+?)    .+?</a> </div>', re.DOTALL,).findall(htmlDoc))
        
        for link in links:
            osdList.append((_(link[1]), link[0]))
        
        
               
        osdList.append((_("Help & About"), "help"))
        osdList.append((_("Exit"), "exit"))
        
        Screen.__init__(self, session)
        self["myMenu"] = MenuList(osdList)
        self["myActionMap"] = ActionMap(["SetupActions"],
        {
        "ok": self.go,
        "cancel": self.cancel
        }, 
        -1)    
        
    
    def go(self):
        returnValue = self["myMenu"].l.getCurrentSelection()[1]
        returnSelection = self["myMenu"].l.getCurrentSelection()[0]
        
        if returnValue is "help":
            self.session.open(ShowHelp)
        elif returnValue is "exit":
            self.close(None)
        else:
            value = returnValue + "," +  self.value.split(",")[1] + " " + returnSelection
            print value
            self.session.open(MovieSource, "moviesource", value)
        
            
            
         
                   
    def cancel(self):
        self.close(None)
###########################################################################
class MovieSource(Screen):
    wsize = getDesktop(0).size().width() - 200
    hsize = getDesktop(0).size().height() - 300
    
    skin = """
        <screen position="100,150" size=\"""" + str(wsize) + "," + str(hsize) + """\" title="1channel" >
        <widget name="myMenu" position="10,10" size=\"""" + str(wsize - 20) + "," + str(hsize - 20) + """\" scrollbarMode="showOnDemand" />
        </screen>"""
            

        
    def __init__(self, session, action, value):
        
        self.session = session

        self.action = action
        
        self.value = value
        
        osdList = []
        
        resolved = []
        print self.value
        
        if not (self.value.split(",")[0].find("http://") > -1 ):
        
            url = "http://www.1channel.ch" + self.value.split(",")[0] 
            #reString = '<div class="index_item index_item_ie"><a href="(.+?)" title=".+?"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>(.+?)</h2>'

            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()


            links = (re.compile ('<a href="(.+?)" onClick="return',).findall(htmlDoc))
            
            for link in links:
                if (link.find("&domain=" ) > -1 ):
                    x = False
                    try:
                        x = urllib2.urlopen("http://1channel.ch" + link)
                    except:
                        print e.reason
                
                    if x:
                        x_url = x.geturl()
                    
                        if (x_url.find("1channel.ch") > -1 ):    
                            x_doc = str(x.read())
                            l = (re.compile ('</frameset><noframes>(.+?)</noframes>',).findall(x_doc))
                            x_url = l[0]
                        
                    
                
                    resolved.append(x_url)
                    
        else:
                resolved.append(self.value.split(",")[0])
             
        print resolved 
                    
        linksfound = 0
        for link in resolved:
            if (link.find("putlocker.com/file/") > -1 ):
                osdList.append((_("Putlocker: " + link[30:]), link))
                linksfound = linksfound + 1
                
            elif (link.find("sockshare.com/file/") > -1 ):
                osdList.append((_("Sockshare: " + link[30:]), link))
                linksfound = linksfound + 1
                
            elif (link.find("novamov.com/video/") > -1 ):
                osdList.append((_("Novamov: " + link[29:]), link))
                linksfound = linksfound + 1
                
            elif (link.find("divxstage.eu/video/") > -1 ):
                osdList.append((_("Divixstage: " + link[30:]), link))
                linksfound = linksfound + 1
                
            elif (link.find("nowvideo.eu/video/") > -1 ):
                osdList.append((_("Nowvideo: " + link[29:]), link))
                linksfound = linksfound + 1
                
            elif (link.find("zalaa.com/") > -1 ):
                osdList.append((_("Zalaa: " + link.split("/")[3]), link))
                linksfound = linksfound + 1
                
            elif (link.find("uploadc.com/") > -1 ):
                osdList.append((_("Uploadc: " + link.split("/")[3]), link))
                linksfound = linksfound + 1
            
            elif (link.find("vidxden.com/") > -1 ):
                osdList.append((_("Vidixden: " + link.split("/")[3]), link))
                linksfound = linksfound + 1
            
            elif (link.find("vidbux.com/") > -1 ):
                osdList.append((_("Vidbux: " + link.split("/")[3]), link))
                linksfound = linksfound + 1
                
            elif (link.find("filenuke.com/") > -1 ):
                osdList.append((_("Filenuke: " + link.split("/")[3]), link))
                linksfound = linksfound + 1 
        
        if linksfound is 0:
            osdList.append((_("Sorry no usable links found!"), "exit"))
        
        
               
        osdList.append((_("Help & About"), "help"))
        osdList.append((_("Exit"), "exit"))
        
        Screen.__init__(self, session)
        self["myMenu"] = MenuList(osdList)
        self["myActionMap"] = ActionMap(["SetupActions"],
        {
        "ok": self.go,
        "cancel": self.cancel
        }, 
        -1)    
        
    
    def go(self):
        returnValue = self["myMenu"].l.getCurrentSelection()[1]
        
        if returnValue is "help":
            self.session.open(ShowHelp)
        elif returnValue is "exit":
            self.close(None)
        elif (returnValue.find("putlocker.com/file/") > -1 ) or (returnValue.find("sockshare.com/file/") > -1 ):
            returnValue = returnValue + "," + self.value.split(",")[1]
            self.Putlocker(returnValue)
        elif (returnValue.find("novamov.com/video/") > -1 ) or (returnValue.find("divxstage.eu/video/") > -1 ) or (returnValue.find("nowvideo.eu/video/") > -1 ):
            returnValue = returnValue + "," + self.value.split(",")[1]
            self.Novamov(returnValue)
        elif (returnValue.find("zalaa.com/") > -1 ) or (returnValue.find("uploadc.com/") > -1 ):
            returnValue = returnValue + "," + self.value.split(",")[1]
            self.Uploadc(returnValue)
        elif (returnValue.find("vidbux.com/") > -1 ) or (returnValue.find("vidxden.com/") > -1 ):
            returnValue = returnValue + "," + self.value.split(",")[1]
            self.Vidbux(returnValue)
        elif (returnValue.find("filenuke.com/") > -1 ):
            returnValue = returnValue + "," + self.value.split(",")[1]
            self.Filenuke(returnValue)
            
            
         
                   
    def cancel(self):
        self.close(None)
        
    def Putlocker(self, fileUrl):
        
        self.title = fileUrl.split(",")[1]
        fileUrl = fileUrl.split(",")[0]
        
                       
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        req = urllib2.Request(fileUrl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')

        response = ""
        html_doc =""
        try:response = urllib2.urlopen(req)
        except URLError, e:
            print e.reason
        except HTTPError, e:
            print e.reason
        if not response is "":
            try: html_doc = str(response.read())    
            except URLError, e:
                print e.reason
            except HTTPError, e:
                print e.reason
            response.close()
        
        plhash =""
        if not html_doc is "":
            plhash = (re.compile ('<input type="hidden" value="([0-9a-f]+?)" name="hash">').findall(html_doc))
            
        if plhash is "":
            self.session.open(MessageBox,_("Host Resolver > File not found error:\n" + self["myMenu"].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout = 5)
                        
        else:    
            time.sleep(7)
            data = {'hash': plhash[0], 'confirm':'Continue as Free User'}
            data = urllib.urlencode(data)
            req = urllib2.Request(fileUrl, data)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            html_doc = str(response.read())
            response.close()
            plplaylist = (re.compile ("playlist: \'/get_file.php\\?stream=(.+?)\'").findall(html_doc))
            if not plplaylist:
                self.session.open(MessageBox,_("Host Resolver > Unable to resolve:\n" + self["myMenu"].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout = 5)
                        
            else:
                print fileUrl
                if (fileUrl.find("http://www.putlocker.com/file/") > -1 ):
                    url = "http://www.putlocker.com/get_file.php?stream=" + plplaylist[0]
                elif (fileUrl.find("http://www.sockshare.com/file/") > -1 ):
                    url = "http://www.sockshare.com/get_file.php?stream=" + plplaylist[0]    
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                html_doc = str(response.read())
                response.close()

                plurl = (re.compile ('<media:content url="(.+?)" type="video/x-flv"').findall(html_doc))
                
                if not plurl:
                    self.session.open(MessageBox,_("Host Resolver > Unable to resolve:\n" + self["myMenu"].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout = 5)
                        
                else:
                    try:
                        url = plurl[0].replace("&amp;", "&") 
                        url = url.replace("'", "")
                    except:     
                        url = plurl[0]
                    print "### " + url + " ###"
                    
                    
                    
                    fileRef = eServiceReference(4097,0,url)
                    fileRef.setName (self.title) 
                    self.session.open(MoviePlayer, fileRef)
                    
                    
    def Novamov(self, fileUrl):
    
        self.title = fileUrl.split(",")[1]
        fileUrl = fileUrl.split(",")[0]                
        
        req = urllib2.Request(fileUrl)

        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')

        response = urllib2.urlopen(req)

        html_doc = str(response.read())

        response.close()

        r = re.search('flashvars.domain="(.+?)".+?flashvars.file="(.+?)".+?flashvars.filekey="(.+?)"', html_doc, re.DOTALL)

        if r:
        
            print r.groups()

            domain, filename, filekey = r.groups()

            print domain

            url = domain + "/api/player.api.php?key=" + filekey + "&file=" + filename

            req = urllib2.Request(url)
    
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')

            response = urllib2.urlopen(req)

            html_doc = str(response.read())

            response.close()

            print html_doc

            html_doc = html_doc.split("&")

            url = str(html_doc[0][4:]) 
            
            
                
            fileRef = eServiceReference(4097,0,url)
            fileRef.setName (self.title) 
            self.session.open(MoviePlayer, fileRef)
            
        else:
            self.session.open(MessageBox,_("Host Resolver > Unable to resolve:\n" + self["myMenu"].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout = 5)

    def Uploadc(self, fileUrl):
    
        self.title = fileUrl.split(",")[1]
        fileUrl = fileUrl.split(",")[0]                
        
        try:
            import jsunpack
        except:
            print "no jsunpack.py"


        try:
            req = urllib2.Request(fileUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            html_doc = str(response.read())
            response.close()
 
            post = (re.compile ('<input type="hidden" name="(.+?)".+?value="(.+?)">').findall(html_doc))

            data = urllib.urlencode(post)

            response = urllib2.urlopen(req, data)
            html_doc = str(response.read())
            response.close()

            try:
                jspack = (re.compile ("<script type='text/javascript'>eval(.+?)script>", re.DOTALL).findall(html_doc))[1]
                js = jsunpack.unpack(jspack)
                url =  (re.compile ('<param name="src"0="(.+?)"/>', re.DOTALL).findall(js))[0]
            except:
                url = (re.compile ("'file','(.+?)'", re.DOTALL).findall(html_doc))[0]

            print url
        
            
            
            print self.title    
            fileRef = eServiceReference(4097,0,url)
            fileRef.setName (self.title) 
            self.session.open(MoviePlayer, fileRef)
            
        except:
            print "jebiga"
            self.session.open(MessageBox,_("Host Resolver > Unable to resolve:\n" + self["myMenu"].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout = 5)
            
    def Vidbux(self, fileUrl):
    
        self.title = fileUrl.split(",")[1]
        fileUrl = fileUrl.split(",")[0]                
        
        try:
            import jsunpack
        except:
            print "no jsunpack.py"


        try:
            req = urllib2.Request(fileUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            html_doc = str(response.read())
            response.close()

            post = (re.compile ('<input name="(.+?)".+?value="(.+?)"').findall(html_doc))

            data = urllib.urlencode(post)

            response = urllib2.urlopen(req, data)
            html_doc = str(response.read())
            response.close()

            jspack = (re.compile ("<script type='text/javascript'>eval(.+?)script>", re.DOTALL).findall(html_doc))[0]

            js = jsunpack.unpack(jspack)

            url =  (re.compile ("'file','(.+?)'", re.DOTALL).findall(js))[0]

            print url
        
            
            
            print self.title    
            fileRef = eServiceReference(4097,0,url)
            fileRef.setName (self.title) 
            self.session.open(MoviePlayer, fileRef)
            
        except:
            print "jebiga"
            self.session.open(MessageBox,_("Host Resolver > Unable to resolve:\n" + self["myMenu"].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout = 5)
                                 
    def Filenuke(self, fileUrl):
    
        self.title = fileUrl.split(",")[1]
        fileUrl = fileUrl.split(",")[0]                
        
        try:
            import jsunpack
        except:
            print "no jsunpack.py"


        try:
    
            req = urllib2.Request(fileUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            html_doc = str(response.read())
            response.close()

            post = (re.compile ('<form method="POST" action=\'\'>(.+?)</form>', re.DOTALL).findall(html_doc))[0]
            post_data = (re.compile ('<input type="hidden" name="(.+?)" value="(.+?)">',).findall(post))
   
            post_data.append(("method_free", "Free"))

            data = urllib.urlencode(post_data)

            response = urllib2.urlopen(req, data)
            html_doc = str(response.read())
            response.close()
    

            jspack = (re.compile ("<script type='text/javascript'>eval(.+?)script>", re.DOTALL).findall(html_doc))[1]
            js = jsunpack.unpack(jspack)
    
            url =  (re.compile ("'file','(.+?)'", re.DOTALL).findall(js))[0]
        
            
            
            print self.title    
            fileRef = eServiceReference(4097,0,url)
            fileRef.setName (self.title) 
            self.session.open(MoviePlayer, fileRef)
            
        except:
            print "jebiga"
            self.session.open(MessageBox,_("Host Resolver > Unable to resolve:\n" + self["myMenu"].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout = 5)
                                 
                          
###########################################################################

def main(session, **kwargs):
        
    
    
    action = "start"
    value = 0 
    burek = session.open(MyMenux, action, value)
        
                  
###########################################################################    

class MoviePlayer(MP_parent):
	def __init__(self, session, service):
		self.session = session
		self.WithoutStopClose = True
		MP_parent.__init__(self, self.session, service)
###########################################################################

def Plugins(**kwargs):
    return PluginDescriptor(
        name="1channel",
        description="1channel video on demand",
        where = [ PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU ],
        icon="./icon.png",
        fnc=main)


