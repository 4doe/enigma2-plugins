import re
import urllib2


class html_parser:
		
	def __init__(self):
		self.quality = ''
		
	def get_parsed_link(self, url): 
		#print '###### HTML PARSER ########'
		#print url
		
		
		try:
			
			######## filmsehri ##########
			if url.find('filmsehri')>-1: 
				request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 nStreamVOD 0.1', 'Connection': 'Close'})
				try:
					page = urllib2.urlopen(request).read()
					page = page.strip(' \t\n\r')
					regex1 = re.findall(r'player.swf\?config=(.*?)" quality="high"',page)
					#print hash_list
					if len(regex1)>0:
						url2 = regex1[0]
						request = urllib2.Request(url2, None, {'User-agent': 'Mozilla/5.0 nStreamVOD 0.1', 'Connection': 'Close'})
						page = urllib2.urlopen(request).read()
						regex2 = re.findall(r'<file>(.*?)<\/file>',page)
						if len(regex2)>0: 
							url = regex2[0]
							#print url
			
				except Exception, ex:
					print ex	    		    
				

			######## watchcinema.ru ##########
			if url.find('watchcinema.ru')>-1: 
				request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 nStreamVOD 0.1', 'Connection': 'Close'})
				try:
					page = urllib2.urlopen(request).read()
					page = page.strip(' \t\n\r')
					regex = re.findall(r'<iframe src="(http:\/\/v[^"]*)',page)
					url = regex[0]
					
					#YOUTUBUE FIX
					request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 nStreamVOD 0.1', 'Connection': 'Close'})
					page = urllib2.urlopen(request).read()
					regex = re.findall(r'src="http://www.youtube.com/embed/([^?]*)',page)
					if(len(regex)==1):
						url = 'http://www.youtube.com/watch?v=' + regex[0]
					#print '######## watchcinema.ru ##########'
					#print url

				except Exception, ex:
					print ex
					
			######## xvideos.com ##########
			if url.find('xvideos.com')>-1: 
				request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 nStreamVOD 0.1', 'Connection': 'Close'})
				try:
					page = urllib2.urlopen(request).read()
					regex = re.findall(r'3GP\|\|(.*?)\|\|',page)
					url = regex[0]

				except Exception, ex:
					print ex 
					
			######## vizor.tv ##########
			if url.find('vizor.tv')>-1 and url.find('http://vizor.tv/get_file')<0: 
				request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 nStreamVOD 0.1', 'Connection': 'Close'})
				try:
					page = urllib2.urlopen(request).read()
					regex = re.findall(r'file=([^&]*)',page)
					url = 'VIZOR' + regex[0]

				except Exception, ex:
					print ex
   	    				

		except Exception, ex:
			print ex
			print 'html_parser ERROR'                	
		return url 