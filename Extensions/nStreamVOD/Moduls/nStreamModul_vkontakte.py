# nitrogen14 - www.pristavka.de
from xml.etree.cElementTree import fromstring, ElementTree
import urllib2
import urllib as ul
import os, re
from datetime import datetime
from time import time

def debug(obj, text=''):
	print datetime.fromtimestamp(time()).strftime('[%H:%M:%S]')
	print '%s' % text +  ' %s\n' % obj

def mod_request(url, param = None):
	url = 'http://' + url
	html = ''
	try:
		debug(url, 'MODUL REQUEST URL')
		req = urllib2.Request(url, param, {'User-agent': 'Mozilla/5.0 nStreamVOD 0.1', 'Connection': 'Close'})
		html = urllib2.urlopen(req).read() 
		#print html
	except Exception, ex:
		print ex
		print 'REQUEST Exception'
	return html

      
class html_parser_vkontakte:
	
	def __init__(self):
		self.video_list = []
		self.next_page_url = ''
		self.next_page_text = ''
		self.prev_page_url = ''
		self.prev_page_text = ''
		self.search_text = ''
		self.search_on = ''
		self.active_site_url = ''
		self.playlistname = ''
		self.playlist_cat_name = ''
		self.kino_title = ''
		self.category_back_url = ''
		self.error = ''


	def get_list(self, url):
		debug(url, 'MODUL URL: ')
		parts = url.split('@')
		#print parts 
		video_list_temp = []
		url = parts[0]
		page = parts[1]
		name = parts[2].encode('utf-8')
		self.search_text = 'SEARCH'
		self.search_on = 'search'
		chan_counter = 0
		if(len(parts)==3): 
			self.playlistname = 'VKONTAKTE SEARCH'
			new = (
				1,
				'PRESS STOP BUTTON TO ENTER KEYWORD',
				None,
				None,
				None,
				'',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new) 

		if(len(parts)==4):
			 
			url = 'watchcinema.ru/search/' 
			param = ul.quote(parts[3].encode('cp1251'))
			debug(param, 'param')
			param = 'q=%s&quality=1&poisk=add' % param
			page = mod_request(url, param)
			results = re.findall(r'class="tooltip" href="(http://[^"]*).*\s.*\s.*src="([^<"]*)".*?alt="([^"]*)',page)
			self.playlistname = 'VKONTAKTE SEARCHRESULT FOR "%s" %i' % (parts[3], len(results))
			for text in results:
				img = text[1]
				title = text[2].decode('1251').encode('utf-8')
				title = re.sub('&[^;]*.', '', title)
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img,
					url,
					None,
					None,
					img,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)
			#print video_list_temp
		self.prev_page_url = ''
		self.prev_page_text = 'BACK'
		self.video_list = video_list_temp
