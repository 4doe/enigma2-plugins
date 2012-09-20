# nitrogen14 - www.pristavka.de
from xml.etree.cElementTree import fromstring, ElementTree
import urllib2
import urllib as ul
import os, re
from datetime import datetime
from time import time
#ADD EXTERNAL MODUL
from nStreamModul_vkontakte import html_parser_vkontakte
from nStreamModul_vizor_tv import html_parser_vizor_tv

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

      
class html_parser_moduls:
	
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
		

	def reset_buttons(self):
		self.kino_title = ''
		self.next_page_url = None
		self.next_page_text = ''
		self.prev_page_url = None
		self.prev_page_text = ''
		self.search_text = ''
		self.search_on = None

	def get_list(self, url):
		debug(url, 'MODUL URL: ')
		self.reset_buttons() 

#EXTERNAL FILE WITH SWITCH AND PARSER  vkontakte search ################################################################################################################ 		
		if(url.find('vkontaktesearch')>-1):
			VKONTAKTESEARCH = html_parser_vkontakte() 
			VKONTAKTESEARCH.get_list(url)
			self.video_list = VKONTAKTESEARCH.video_list
			self.next_page_url = VKONTAKTESEARCH.next_page_url
			self.next_page_text = VKONTAKTESEARCH.next_page_text
			self.prev_page_url = VKONTAKTESEARCH.prev_page_url
			self.prev_page_text = VKONTAKTESEARCH.prev_page_text
			self.search_text = VKONTAKTESEARCH.search_text
			self.search_on = VKONTAKTESEARCH.search_on
			self.active_site_url = VKONTAKTESEARCH.active_site_url
			self.playlistname = VKONTAKTESEARCH.playlistname
			self.playlist_cat_name = VKONTAKTESEARCH.playlist_cat_name
			self.kino_title = VKONTAKTESEARCH.kino_title
			self.category_back_url = VKONTAKTESEARCH.category_back_url
			self.error = VKONTAKTESEARCH.error 		
#EXTERNAL FILE WITH SWITCH AND PARSER  vkontakte search ################################################################################################################ 
			  

#EXTERNAL FILE WITH SWITCH AND PARSER  vizor.tv ################################################################################################################ 		
		if(url.find('vizor.tv')>-1):
			VIZORTV = html_parser_vizor_tv() 
			VIZORTV.get_list(url)
			self.video_list = VIZORTV.video_list
			self.next_page_url = VIZORTV.next_page_url
			self.next_page_text = VIZORTV.next_page_text
			self.prev_page_url = VIZORTV.prev_page_url
			self.prev_page_text = VIZORTV.prev_page_text
			self.search_text = VIZORTV.search_text
			self.search_on = VIZORTV.search_on
			self.active_site_url = VIZORTV.active_site_url
			self.playlistname = VIZORTV.playlistname
			self.playlist_cat_name = VIZORTV.playlist_cat_name
			self.kino_title = VIZORTV.kino_title
			self.category_back_url = VIZORTV.category_back_url
			self.error = VIZORTV.error 		
#EXTERNAL FILE WITH SWITCH AND PARSER  vizor.tv ################################################################################################################

#SWITCH  m3u ########################################################################################

		if(url.find('m3u')>-1):
			parts = url.split('@') 
			filename = parts[0]
			name = parts[2].encode('utf-8')
			self.playlistname = name 
			ts = None
			if(url.find('TS')>-1):
				ts = 'True'
			try:               
				video_list_temp = [] 
				chan_counter = 0
				if filename.find('http')>-1:
					url = filename.replace('http://', '')
					myfile = mod_request(url) 
				else:
					myfile = open("/usr/lib/enigma2/python/Plugins/Extensions/nStreamVOD/%s" % filename, "r").read()
				#print myfile
				regex = re.findall(r'#EXTINF.*,(.*\s)\s*(.*)',myfile)
				if not len(regex)>0:
					regex = re.findall(r'((.*.+)(.*))',myfile)
				#print regex
		 
				for text in regex:
					title = text[0].strip()
					url = text[1].strip()
					chan_counter +=1 
					chan_tulpe = (
						chan_counter,
						title,
						'',
						'xxx.png',
						url,
						None,
						None,
						'',
						'',
						None,
						ts
					)
					video_list_temp.append(chan_tulpe) 

					if(len(video_list_temp)<1):
						print 'ERROR m3u CAT LIST_LEN = %s' %  len(video_list_temp)  
			except:
				print 'ERROR m3u'   									    	

			return video_list_temp			
		
#SWITCH  kinomaxpro.com ################################################################################################################ 		
		if(url.find('kinomaxpro')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')
			
			self.active_site_url = 'kinomaxpro.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_kinomaxpro_categories(url)
			
			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'Kinomaxpro CAT: ' + self.playlist_cat_name
				self.video_list = self.get_kinomaxpro_category_films(url)
				self.category_back_url = url
				self.category_title = name
			
			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' PAGE ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_kinomaxpro_category_films(url)
				self.category_back_url = url       				
			
			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_kinomaxpro_film(url)

#SWITCH filmsevenler.net ################################################################################################################				

		if(url.find('filmsevenler')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'www.filmsevenler.net'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_filmsevenler_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'filmsevenler CAT: ' + self.playlist_cat_name
				self.video_list = self.get_filmsevenler_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==5 and page[3]=='page'):
					page_nr= ' PAGE ' + page[4]
				if (len(page)==3 and page[1]=='page'):
					page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_filmsevenler_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_filmsevenler_film(url)				
									
		
#SWITCH filmsehri.com ################################################################################################################				

		if(url.find('filmsehri')>-1):
			debug('#SWITCH filmsehri.com #')
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'filmsehri.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_filmsehri_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'filmsehri CAT: ' + self.playlist_cat_name
				self.video_list = self.get_filmsehri_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==5 and page[3]=='page'):
					page_nr= ' PAGE ' + page[4]
				if (len(page)==3 and page[1]=='page'):
					page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_filmsehri_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_filmsehri_film(url)				


#SWITCH http://www.xvideos.com/################################################################################################################				

		if(url.find('xvideos.com')>-1):
			debug('#SWITCH xvideos.com #')
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'www.xvideos.com'
			video_list_temp = []
			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_xvideos_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'XVIDEOS CAT: ' + self.playlist_cat_name
				self.video_list = self.get_xvideos_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				print '++++++++++++'
				
				print page
				print len(page)
				if(int(len(page)-2)>0):
					page_nr= ' PAGE ' + page[len(page)-2]
				#if (len(page)==3 and page[1]=='page'):
				#	page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_xvideos_category_films(url)
				self.category_back_url = url
 # --> nStreamHTMLparser QUICKSTART PLAY FROM CATEGORY
			# if(page=='film'):
			# 	self.kino_title = name
			# 	self.playlistname = self.playlist_cat_name + '     ' + name
			# 	self.video_list = self.get_xvideos_film(url)      			       				

#SWITCH www.sinemaizle.org ################################################################################################################				

		if(url.find('sinemaizle.org')>-1):
			debug('#SWITCH filmsehri.com #')
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'www.sinemaizle.org'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_sinemaizle_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'sinemaizle CAT: ' + self.playlist_cat_name
				self.video_list = self.get_sinemaizle_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==5 and page[3]=='page'):
					page_nr= ' PAGE ' + page[4]
				if (len(page)==3 and page[1]=='page'):
					page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_sinemaizle_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_sinemaizle_film(url)
				    			   
########################################################################
		return self.video_list  ########################################	
########################################################################
 
#FUNCTIONS kinomaxpro.com################################################################################################################  
			
	def get_kinomaxpro_categories(self, url): 
		#print 'get_kinomaxpro_categories'
		try:              
			page = mod_request(url).decode('cp1251').encode('utf-8') 
			video_list_temp = [] 

			chan_counter = 1
			
			new = (
				chan_counter,
				'NEW',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/@category@NEW',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)
			
			regex = re.findall(r'<a href="/(.*)/">(.*)</a>',page) 
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
					'nStreamModul@' + self.active_site_url + '/' + url + '/@category@' + title,
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
			print 'ERROR get_kinomaxpro_category'   									    	
		
		return video_list_temp
		


	def get_kinomaxpro_category_films(self, url):
		#print 'get_kinomaxpro_category_films'
		try:              
			page = mod_request(url).decode('cp1251').encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 0
			regex_films = re.findall(r'<div class="poster">\s.*<img.*src="(.*jpg)".*>\s.*\s.*\s.*\s.*href="(.*html)".*>(.*)<\/a',page)
			regex_descr = re.findall(r'<div id="news.*">(.*)<\/div>',page)
		
			for text in regex_films:
				chan_counter +=1
				url = text[1].replace('http://', '')
				img_url = text[0]
				title = text[2]
				descr = regex_descr[chan_counter-1]
				chan_tulpe = (
					chan_counter,
					title,
					descr,
					'http://' + self.active_site_url + img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					'http://' + self.active_site_url + img_url,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)
			
				navi = re.findall(r'<div class="navigation">\s*.*<a\s+href=".*">.*<\/a>.*\s*<\/div>',page)
			if(len(navi)>0):
				#pages = re.findall(r'ref=\"([^\"]*)\">([^<"]*)',navi[0])
				pages = re.findall(r'ref=\"([^\"]*)\">([^\d][^<"]*)',navi[0])
				if(len(pages)==1):
					if(pages[0][1].find('8592')==-1):
						self.next_page_url = pages[0][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
						text = pages[0][1].replace(' &#8594;','')
						self.next_page_text = text
						self.prev_page_url = 'nStreamModul@kinomaxpro.com@start@KINOMAXPRO ALL CATEGORIES'
						self.prev_page_text = 'Categories'
					else:
						self.prev_page_url = pages[0][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
						text = pages[0][1].replace('&#8592; ','')
						self.prev_page_text = text
				if(len(pages)==2):
					self.next_page_url = pages[1][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
					self.next_page_text = pages[1][1].replace(' &#8594;','') 
					self.prev_page_url = pages[0][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
					self.prev_page_text = pages[0][1].replace('&#8592; ','')										 
		
			if(len(video_list_temp)<1):
				print 'ERROR CAT_FIL LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_kinomaxpro_category'   									    	

		return video_list_temp
		


	def get_kinomaxpro_film(self, url): 
		#print 'get_kinomaxpro_film'
		page = mod_request(url)#.decode('cp1251').encode('utf-8') 
		ref_url_vimeo = url
		chan_counter = 0
		video_list_temp = []
		trailer = re.findall(r'param.*&videoUrl=(http:\/\/.*)&videoHDUrl=',page)
		
		img = re.findall(r'<div class="poster">\s.*<img.*src="(.*jpg)"',page)
		
		if(len(trailer)>0):
			chan_counter = chan_counter + 1 
			url = trailer[0]
			chan_tulpe = (
				chan_counter,
				self.kino_title + '(trailer)',
				'',
				'http://' + self.active_site_url + img[0],
				url,
				None,
				None,
				'http://' + self.active_site_url + img[0],
				'',
				None,
				None
			)
			video_list_temp.append(chan_tulpe)			
		
		vk = re.findall(r'<iframe src="(http:\/\/vk.*)" width',page)
		if(len(vk)>0): 
			url = vk[0].replace('&amp;', '&') 
			chan_counter = chan_counter + 1
			chan_tulpe = (
				chan_counter,
				self.kino_title + ' (vkontakte)',
				'',
				'http://' + self.active_site_url + img[0],
				url,
				None,
				None,
				'http://' + self.active_site_url + img[0],
				'',
				None,
				None
			)
			video_list_temp.append(chan_tulpe)

		vkontakte2 = re.findall(r'value=.(http:\/\/vkontakte.ru\/[^<"]*).>([^<]*)',page)
		#print vkontakte2
		if(len(vkontakte2)>0):
			for film in vkontakte2:
				title = film[1].decode('cp1251').encode('utf-8') 
				url = film[0].replace('&amp;', '&') 
				chan_counter = chan_counter + 1
				chan_tulpe = (
					chan_counter,
					self.kino_title + '/'+ title + ' (vkontakte)',
					'',
					'http://' + self.active_site_url + img[0],
					url,
					None,
					None,
					'http://' + self.active_site_url + img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		
		vimeo = re.findall(r'iframe.*src="(http:\/\/player.vimeo.com\/[^<"]*)',page)
		if(len(vimeo)>0):
			
			url_vimeo = vimeo[0]
			url_ref = 'http://' + ref_url_vimeo
			request = urllib2.Request(url_vimeo, None, {'User-agent': 'Mozilla/5.0 nStreamVOD 0.1', 'Connection': 'Close'})
			request.add_header('Referer', url_ref) 
			page = urllib2.urlopen(request)
			page = page.read()
			params = re.findall(r'"signature":"([0-9a-f]{32})","timestamp":([0-9]+),[^\}]+\},"video":\{"id":(\d+)',page) 
			qualitys = re.findall(r'{"h264":[^\}]*',page)
			qualitys = re.findall(r'"(hd|sd|mobile)"',qualitys[0])			
			
			for quality in qualitys:
				url = 'http://player.vimeo.com/play_redirect?clip_id=video/' + params[0][2] + '&sig=' + params[0][0] + '&time=' + params[0][1] + '&quality=' + quality + '&codecs=H264,VP8,VP6&type=moogaloop&embed_location=' + url_ref
				chan_counter = chan_counter + 1
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' (vimeo ' + quality + ')',
					'',
					'http://' + self.active_site_url + img[0],
					url,
					None,
					None,
					'http://' + self.active_site_url + img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)     

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name


		
		return video_list_temp		
		


#FUNCTIONS filmsevenler.net###############################################################################################################

	def get_filmsevenler_categories(self, url): 
		#print 'get_filmsevenler_categories'
		try:              
			page = mod_request(url).encode('utf-8') 
			page = re.sub('\n','', page)
			video_list_temp = [] 

			chan_counter = 1

			new = (
				chan_counter,
				'NEW',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/@category@NEW',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex = re.findall(r'cat-item-\d+"><ahref="http:\/\/www.filmsevenler.net\/(filmizle\/[^"]*)".*?>([^<]*)',page)
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
					'nStreamModul@' + self.active_site_url + '/' + url + '/@category@' + title,
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
			print 'ERROR get_filmsevenler_category'   									    	

		return video_list_temp  
		
		
	def get_filmsevenler_category_films(self, url):
		#print 'get_filmsevenler_category_films'
		#try:              
		page = mod_request(url).encode('utf-8')
		page = re.sub('\n','', page) 
		video_list_temp = [] 
		chan_counter = 0
		regex_films = re.findall(r'<divclass="video-film odd" id="post-\d+">.*?<ahref="http:\/\/www.(filmsevenler.net\/[^"]*)".*?title="([^<"]*)".*?imgsrc="([^<"]*)".*?<em>(.*?)<\/em.*?imgsrc="([^<"]*)".*?alt',page)
		for text in regex_films:
			chan_counter +=1

			url = text[0]
			img_url = text[4]
			title = text[1]
			descr = text[3].replace('&nbsp;', '')

			chan_tulpe = (
				chan_counter,
				title,
				descr,
				img_url,
				None,
				'nStreamModul@' + url + '@film@' + title,
				None,
				img_url,
				'',
				None,
				None
			)  
			video_list_temp.append(chan_tulpe)

		navi = re.findall(r'postpage.*?<divclass="reklamicerik">',page) 
		if(len(navi)>0):
			pages = re.findall(r'ref=\"([^\"]*)\">([^<"]*)',navi[0]) 
			if(len(pages)==1):
				if(pages[0][1].find('laquo')==-1):
					self.next_page_url = pages[0][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
					text = pages[0][1].replace(' &raquo;','')
					self.next_page_text = text
					self.prev_page_url = 'nStreamModul@www.filmsevenler.net@start@filmsevenler ALL CATEGORIES'
					self.prev_page_text = 'Categories'
				else:
					self.prev_page_url = pages[0][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
					text = pages[0][1].replace('&laquo; ','')
					self.prev_page_text = text
			if(len(pages)==2):
				self.next_page_url = pages[1][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = pages[1][1].replace(' &raquo;','') 
				self.prev_page_url = pages[0][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = pages[0][1].replace('&laquo; ','')                                                           
		
		
		
		if(len(video_list_temp)<1):
			print 'ERROR CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		#except:
		 #   print 'ERROR get_filmsevenler_category_films'   									    	

		return video_list_temp


	def get_filmsevenler_film(self, url): 
		#print 'get_filmsevenler_film'
		page = mod_request(url)
		page = re.sub('\n','', page) 
		ref_url_vimeo = url
		chan_counter = 0
		video_list_temp = []


		img = re.findall(r'filmdetayx_resim.*?imgsrc="(http[^<"]*)',page)
		descr = re.findall(r'filmdetayx_aciklama.*?p>([^<]*)',page) 


		vk = re.findall(r'iframesrc="(http[^<"]*)',page)
		if(len(vk)>0): 
			url = vk[0].replace('&amp;', '&') 
			chan_counter = chan_counter + 1
			chan_tulpe = (
				chan_counter,
				self.kino_title + ' (vkontakte)',
				descr[0],
				img[0],
				url,
				None,
				None,
				img[0],
				'',
				None,
				None
			)
			video_list_temp.append(chan_tulpe)
    

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		#print video_list_temp


		return video_list_temp








# FUNCTIONS filmsehri.com ###############################################################################################################

	def get_filmsehri_categories(self, url): 
		#print 'get_filmsehri_categories'
		try:              
			page = mod_request(url).encode('utf-8') 
			page = re.sub('\n','', page)
			video_list_temp = [] 

			chan_counter = 1

			new = (
				chan_counter,
				'NEW',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/@category@NEW',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)


			regex_url = re.findall(r'<li><a href=\"http:\/\/www.filmsehri.com\/(.*?)\" id=\"kategoriler\"',page)
			regex_title = re.findall(r'id=\"kategoriler\">(.*?)<\/a><\/li>',page)
		
			for text in regex_url:
				title = regex_title[chan_counter - 1]
				url = text
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + self.active_site_url + '/' + url + '/@category@' + title,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'   									    	

		return video_list_temp  


	def get_filmsehri_category_films(self, url):
		#print 'get_filmsevenler_category_films'
		try:              
			page = mod_request(url).encode('utf-8')
			page = re.sub('\n','', page) 
			video_list_temp = [] 
			chan_counter = 0
			#print page
		
			regex_helper = re.findall(r'<div id=\"orta-icerik\">(.*?)<\/div>', page)
			regex_link_title = re.findall(r'hidden\"><a href=\"http:\/\/(.*?)\">(.*?)<\/a', regex_helper[0])
			regex_img =  re.findall(r'<img src=\"(.*?)\" width=', regex_helper[0])
		
		
			for text in regex_link_title:
			
				url = text[0]
				img_url = regex_img[chan_counter]
				title = text[1]
				descr = ''
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					descr,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			
			next = re.findall(r"class=['\"]ileri['\"]><a href=['\"](.*?)['\"]>(.*?)<", page)
			prev = re.findall(r"class=['\"]geri['\"]><a href=['\"](.*?)['\"]>(.*?)<", page)
		
			if len(next):
				self.next_page_url = next[0][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = next[0][1] 

			if len(prev):
				self.prev_page_url = prev[0][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = prev[0][1]
			else:	
				self.prev_page_url = 'nStreamModul@filmsehri.com@start@filmsehri ALL CATEGORIES'
				self.prev_page_text = 'Categories'			                                                           



			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_filmsehri_category_films'   									    	

		return video_list_temp


	def get_filmsehri_film(self, url): 
		print 'get_filmsehri_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		parts = re.findall(r'\"1\">(.*?)<\/font>',page)
		
		if(len(parts)>0):
			for part in parts: 

				chan_counter = chan_counter + 1
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' (vkontakte)' + part,
					'',
					'',
					'http://' + url + str(chan_counter),
					None,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)


		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp 
		
		
		
# FUNCTIONS xvideos.com ###############################################################################################################

	def get_xvideos_categories(self, url):
		video_list_temp = []
		chan_counter = 0
		chan_counter = chan_counter + 1 
		new = (
			chan_counter,
			'LAST',
			None,
			None,
			None,
			'nStreamModul@www.xvideos.com/@category@XVIDEOS LAST VIDEOS',
			None,
			'',
			'',
			None,
			None
		)
		video_list_temp.append(new)
		chan_counter = chan_counter + 1
		new = (
			chan_counter,
			'HITS',
			None,
			None,
			None,
			'nStreamModul@www.xvideos.com/hits@category@XVIDEOS HITS',
			None,
			'',
			'',
			None,
			None
		)		
		video_list_temp.append(new)
		chan_counter = chan_counter + 1		
		new = (
			chan_counter,
			'Best Of Today',
			None,
			None,
			None,
			'nStreamModul@www.xvideos.com/best/day/@category@XVIDEOS Best Of Today',
			None,
			'',
			'',
			None,
			None
		)
		video_list_temp.append(new)
		chan_counter = chan_counter + 1
		new = (
			chan_counter,
			'Best Of 7 Days',
			None,
			None,
			None,
			'nStreamModul@www.xvideos.com/best/week/@category@XVIDEOS Best Of 7 Days',
			None,
			'',
			'',
			None,
			None
		)
		video_list_temp.append(new)
		chan_counter = chan_counter + 1
		new = (
			chan_counter,
			'Best Of 30 Days',
			None,
			None,
			None,
			'nStreamModul@www.xvideos.com/best/month/@category@XVIDEOS Best Of 30 Days',
			None,
			'',
			'',
			None,
			None
		)
		video_list_temp.append(new)
		chan_counter = chan_counter + 1
		new = (
			chan_counter,
			'Best Of All Time',
			None,
			None,
			None,
			'nStreamModul@www.xvideos.com/best@category@XVIDEOS Best Of All Time',
			None,
			'',
			'',
			None,
			None
		)
				
		video_list_temp.append(new) 
		
		return video_list_temp

	def get_xvideos_category_films(self, url):
		#print 'get_xvideos_category_films'
		try:              
			page = mod_request(url).encode('utf-8')
			#page = re.sub('\n','', page) 
			video_list_temp = [] 
			chan_counter = 0
			print page
		
			regex_link = re.findall(r'<a href=\"(.*?)\" class=\"miniature\">', page)
			regex_img = re.findall(r'\"miniature\"><img src=\"(.*?)\" onMouseOver=\"startThumbSl', page)
			regex_title_ln_qa =  re.findall(r'<span class=\"red\" style=\"text-decoration\:.*underline;\">(.*?)<\/span><\/a><br>\s.*<(b|strong)>(.*)<\/(b|strong)>(.*)<\/td>', page)
	
			for text in regex_link:
		
				url = text
				img_url = regex_img[chan_counter]
				info = regex_title_ln_qa[chan_counter]
				title = info[0]
				chan_counter +=1
				descr =  info[2] + ' ' + info[4]
				chan_tulpe = (
					chan_counter,
					title,
					descr,
					img_url,
					url,
					None,#'nStreamModul@' + url + '@film@' + title, no extra pahe -> direct play from category
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

		
			next = re.findall(r'nP" href="([^<"]*)">Next', page)
			prev = re.findall(r'<a href="([^<"]*)" class="nP">Prev', page)
				
			if next:
				slash = ''
				if next[0][0:1]!='/':
					slash = '/'
				self.next_page_url =  'nStreamModul@www.xvideos.com' + slash + next[0] + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'NEXT' 
			
			if prev:
				slash = ''
				if prev[0][0:1]!='/':
					slash = '/' 
				self.prev_page_url = 'nStreamModul@www.xvideos.com' + slash + prev[0] + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'PREV'
			else:	
				self.prev_page_url = 'nStreamModul@www.xvideos.com@start@XVIDEOS ALL CATEGORIES'
				self.prev_page_text = 'Categories'  		                                                           



			if(len(video_list_temp)<1):
				print 'ERROR xvideos CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_xvideos_category_films'   									    	

		return video_list_temp 	

	# --> nStreamHTMLparser QUICKSTART PLAY FROM CATEGORY    
	# def get_xvideos_film(self, url): 
	# 	print 'get_xvideos_film'
	# 	page = mod_request(url)
	# 	video_list_temp = []
	# 	video = re.findall(r'3GP\|\|(.*?)\|\|',page)
	# 	if(len(video)>0): 
	# 		url = video 
	# 		chan_tulpe = (
	# 			1,
	# 			self.kino_title,
	# 			'',
	# 			'',
	# 			url[0],
	# 			None,
	# 			None,
	# 			'',
	# 			'',
	# 			None,
	# 			None
	# 		)
	# 		video_list_temp.append(chan_tulpe)
	# 
	# 
	# 	self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
	# 	self.prev_page_text = self.playlist_cat_name   	
	# 
	# 	return video_list_temp		
		
# FUNCTIONS www.sinemaizle.org ###############################################################################################################

	def get_sinemaizle_categories(self, url): 
		print 'get_sinemaizle_categories'
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 0

			print page
			regex1 = re.findall(r'<li class="inline-block">.*<a href="http:\/\/(.*)" title=".*">(.*)</a>.*</li>',page) 
			#print regex1 
			regex2 = re.findall(r'<li class="cat-item cat-item-\d+"><a href="http:\/\/(.*)" title=".*">(.*)</a>',page)
			#print regex2
			for line in regex2:
			   regex1.append(line)
			print regex1

			for text in regex1:
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
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'   									    	

		return video_list_temp  


	def get_sinemaizle_category_films(self, url):
		print 'get_sinemaizle_category_films'
		try:              
			page = mod_request(url).encode('utf-8')
			print page
			video_list_temp = [] 
			chan_counter = 0

			regex = re.findall(r'<a class=".*" href="http:\/\/([^<"]*)">.*\s.*\s.*src="(.*?)".*alt="([^<"]*).*\s.*<p>(.*)</p>', page)
			print regex

			for text in regex:

				url = text[0]
				title = text[2]
				title = re.sub('&[^;]*.', '', title)
				img_url =  text[1]
				print img_url
				descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					descr,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)


			next = re.findall(r'<a href="([^<"]*)" class="next">([^<"]*)<', page)
			prev = re.findall(r'<a href="([^<"]*)" class="prev">([^<"]*)<', page)
			
			if len(next):
				self.next_page_url = next[0][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'NEXT' 
			
			if len(prev):
				self.prev_page_url = prev[0][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'PREVIEW'
			else:	
				self.prev_page_url = 'nStreamModul@www.sinemaizle.org@start@sinemaizle.org ALL CATEGORIES'
				self.prev_page_text = 'Categories'  		                                                           



			if(len(video_list_temp)<1):
				print 'ERROR sinemaizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_sinemaizle_category_films'   									    	

		return video_list_temp


	def get_sinemaizle_film(self, url): 
		print 'get_sinemaizle_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		parts = re.findall(r'',page)
						
		parts = re.findall(r'mod=([^<&]*)',page)

		if(len(parts)>0):
			for url in parts:
				chan_counter = chan_counter + 1 
				if len(parts)==1:
					part = ''
				else:
					part = str(chan_counter)

				chan_tulpe = (
					chan_counter,
					self.kino_title + ' ' + part,
					'',
					'',
					'http://' + url,
					None,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)
				
		vk = re.findall(r'<iframe src="(http:\/\/vk[^<"]*)',page)
		print vk
		part_counter = 1
		if(len(vk)>0):
			for url in vk:
				if len(parts)==1:
					part = ''
				else:
					part = str(part_counter)
				part_counter = part_counter + 1				 
				url = vk[0].replace('&amp;', '&') 
				chan_counter = chan_counter + 1
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' (vkontakte) Part:' + part,
					'',
					'',
					url,
					None,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)  			


		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

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