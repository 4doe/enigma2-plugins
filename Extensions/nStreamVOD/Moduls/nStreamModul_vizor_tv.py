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

      
class html_parser_vizor_tv:
	
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
		url = parts[0]
		page = parts[1]
		name = parts[2].encode('utf-8')
		
		self.active_site_url = 'vizor.tv'

		if(page=='start'): 
			self.playlistname = name
			self.video_list = self.get_vizortv_categories(url)
		
		if(page=='category'):
			self.playlist_cat_name = name
			self.playlistname = 'Vizor.TV CAT: ' + self.playlist_cat_name
			self.video_list = self.get_vizortv_category_films(url)
			self.category_back_url = url
			self.category_title = name
		
		if(page=='episodes'):
			self.kino_title = name
			self.playlistname = self.playlist_cat_name + ' ' + name
			self.video_list = self.get_vizortv_episodes(url)



#FUNCTIONS vizortv ###############################################################################################################

	def get_vizortv_categories(self, url): 
		#print 'get_vizortv_categories'
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 0
			regex = re.findall(r'<li><a.*href="http://([^<"]*)".*>([^<"]*)</a',page)
			for text in regex:
				title = text[1]
				url = text[0]
				chan_counter +=1

				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_vizortv_category'   									    	

		return video_list_temp  
		
		
	def get_vizortv_category_films(self, url):
		#print 'get_filmsevenler_category_films'
		#try:              
		#page = mod_request(url).encode('utf-8')

		video_list_temp = []
		regex_films_tmp = [] 
		chan_counter = 0
		page_nr = 1
		while True:

			page = mod_request(url + '?from=%i' % page_nr).encode('utf-8')
			page_nr = page_nr + 1

			regex_films = re.findall(r'<li.*<a href="http://([^<"]*)".*src="([^<"]*)".*alt="([^<"]*)"',page) 
			if(regex_films == regex_films_tmp):
				break
			regex_films_tmp = regex_films			
			if(regex_films):
				for text in regex_films:
					play = None
					myurl = None
					chan_counter +=1
					url_f = text[0]
					img_url = text[1]
					title = text[2]
					descr = ''
					modus = ''
					if(url_f.find('dvdgroup.php')>-1):
						modus = 'category'
					else:
						modus = 'episodes'
					myurl = 'nStreamModul@' + url_f + '@' + modus + '@' + title
					if(url_f.find('/videos/')>-1):
						myurl = None
						play = 'http://%s' % url_f

					chan_tulpe = (
						chan_counter,
						title,
						descr,
						img_url,
						play,
						myurl,
						None,
						img_url,
						'',
						None,
						None
					)  
					video_list_temp.append(chan_tulpe)
			else:
				break

		self.prev_page_url = 'nStreamModul@vizor.tv@start@Vizor.TV'
		self.prev_page_text = 'Vizor.TV Home'                                                           
		
		
		
		if(len(video_list_temp)<1):
			print 'ERROR CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		#except:
		 #   print 'ERROR get_filmsevenler_category_films'   									    	

		return video_list_temp


	def get_vizortv_episodes(self, url): 
		print 'get_vizortv_episodes'
		page = mod_request(url).encode('utf-8')
		#print page
		chan_counter = 0
		video_list_temp = []


		regex = re.findall(r'<li><a.*href="([^<"]*)".*title="([^<"]*)".*src="(.*.jpg)',page)
		#print regex
		if(len(regex)>0):
			for text in regex:
				chan_counter +=1
				url = text[0]
				img = text[2]
				title = text[1] 
				chan_tulpe = (
					chan_counter,
					title,
					'',
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
    

		self.prev_page_url = 'nStreamModul@vizor.tv@start@Vizor.TV'
		self.prev_page_text = 'Vizor.TV Home'

		return video_list_temp
		
		
				                
# chan_tulpe = (
# 	chan_counter,
# 	name,
# 	description,
# 	picon_url,
# 	stream_url,
# 	playlist_url,
# 	category_id,
# 	img_src,
# 	description4playlist_html,
# 	protected
#	ts_stream (IPTV quickzapping)
# )
# iptv_list_temp.append(chan_tulpe) 