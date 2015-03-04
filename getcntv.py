#encoding=utf8

import json
import os
import re
import sys
import urllib
from datetime import datetime

debug=1

def writeLog(message):
	if debug:		
		now = datetime.utcnow()
		now = now.replace(microsecond=0)
		now = now.isoformat(' ')
		file = open("log.txt", "a+")
		file.write("\n\n" + now + "\n")
		file.write(message.encode('utf-8','ignore'))
        file.close()

# Create sub directory in current directory.
def createStorageDirectory(subdir):	
	dir = '.\\' + subdir + '\\'
	if not os.path.exists(dir):
		os.makedirs(dir)
	return dir

def downloadMP4(url, destDirectory):							
	response = urllib.urlopen(url)
	buffer = bytearray()
	while True:
		data = response.read(1*1024*1024)
		if not data:
			break
		buffer += data

	open(destDirectory, 'x+b').write(buffer)
	

def getVideoFragments(jsonData):
	# Get all video fragments.
	videoFragments = []
	highResolutionVideo = 0
	for key in jsonData.keys():
		if key == 'video':
			for videoKey in jsonData['video']:
				# Videos in field 'chapters' are 3 minutes 464Kbps.
				# Videos in field 'chapters2' are 5 minutes 853Kbps.				
				#pattern = re.compile(r'chapters[0-9]*')
				#matched = pattern.match(videoKey)
				#if matched:	
				if videoKey == 'chapters2':
					print(videoKey)
					highResolutionChapters = jsonData['video'][videoKey]			
					highResolutionVideo = 1
					break
				elif videoKey == 'chapters':
					lowResolutionChapters = jsonData['video'][videoKey]
					
	if highResolutionVideo == 1:
		print("High Resolution Video.")
		chapters = highResolutionChapters
	else:
		print("Low Resolution Video.")
		chapters = lowResolutionChapters
		
	for i in range(len(chapters)):		
		#print(chapters[i]['url'])
		videoFragments.append(chapters[i]['url'])	
		
	return videoFragments
	
	
def videoNameFromUrl(url):
	return url[url.rfind('/')+1:]
	
def downloadFragments(urls, directory):
	total = len(urls)
	for i in range(total):
		filename = videoNameFromUrl(urls[i])		
		dest = directory + filename
		if os.path.exists(dest):
			print('->jumping ' + filename)
		else:
			percentage = " (%i/%i)" % (i+1, total)		
			print('downloading ' + filename + percentage)
			downloadMP4(urls[i], dest)


#def isSportsDomain(videoEntry):
	#pattern = r'sports\.'
	
def getSubSiteName(videoEntry):
	# Type 1: http://sports.cntv.cn/20130128/100886.shtml
	# Type 2: http://tv.cntv.cn/video/C16717/20100826100579
	pattern = 'http://sports'
	if pattern in videoEntry:
		return "000sports"
	else:
		return "000donghua"
	
def getVideoInfoUrl(id, subSite, entry):
	xmlUrl = 'http://vdn.apps.cntv.cn'
	xmlUrl += '/api/getHttpVideoInfo.do?pid=%s&tz=-8&from=%s&url=%s&idl=32&idlr=32&modifyed=false' % (id, subSite, entry)
	writeLog(xmlUrl)
	return xmlUrl

def getVideoInfo(videoEntry):
	size = 12*1024*1024
	response = urllib.urlopen(videoEntry)
	
	# Such a stupid thing to use different encodings in on site.
	subSite = getSubSiteName(videoEntry)
	print(subSite)
	if subSite == "000sports":
		buffer = response.read(size).decode('gbk')
	else:
		buffer = response.read(size).decode('utf8')

	# Get video's id. Video-Description url is assembly from this id.
	pattern = r'\"videoCenterId\",\"(?P<id>.*?)\"'
	result = re.search(pattern, buffer)
	if not result:
		print('error: video id not found')
		return

	# Assembly Video-Description url.
	id = result.group('id')	
	xmlUrl = getVideoInfoUrl(id, subSite, videoEntry)	
	
	# Fetch Video-Description.
	response = urllib.urlopen(xmlUrl)
	buffer = response.read(size).decode('utf8')
	writeLog(buffer)
		
	return buffer
	

def downloadVideo(cntvUrl):
	info = getVideoInfo(cntvUrl)						
	jsonFormatData = json.loads(info)
	fragments = getVideoFragments(jsonFormatData)
	videoDirectory = createStorageDirectory(jsonFormatData['title'])
	print("Videos will be stored at: " + videoDirectory)
	downloadFragments(fragments, videoDirectory)	
	
if __name__ == "__main__":	
	args = sys.argv
	argNumber = len(args)
	print(argNumber)
	if argNumber == 2:
		downloadVideo(args[1])
	elif argNumber == 3:
		type = args[1]
		pid = args[2]		
		if type == "xcm":
			xmlUrl = getVideoInfoUrl(pid, '000teleplay', 'http://donghua.cntv.cn/program/xiongchumozt/shouye/')
		else:
			xmlUrl = "";
		response = urllib.urlopen(xmlUrl)
		info = response.read(12*1024*1024).decode('utf8')
		jsonFormatData = json.loads(info)
		fragments = getVideoFragments(jsonFormatData)
		videoDirectory = createStorageDirectory(jsonFormatData['title'])
		print("Videos will be stored at: " + videoDirectory)
		downloadFragments(fragments, videoDirectory)	
	else:
		print('This is test')
		downloadVideo('http://tv.cntv.cn/video/C16717/8c267b2903e4422eb2ab3d38e4a60ee3')