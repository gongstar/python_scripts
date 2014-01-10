import urllib2
import urllib
import time
import os

OPENSEEKER_CALLBACK_URL = "http://translate.google.com/translate_tts"

def sendCallback(taskuuid,status):
    try:
        text = 'hello'
        lang = 'en'
        #values = urllib.urlencode({"taskuuid": taskuuid,  "status": lang})
        values = urllib.urlencode({"q": text, "textlen": len(text), "tl": lang})
        hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7"}
        req = urllib2.Request(OPENSEEKER_CALLBACK_URL, data=values,headers=hrs)
        p = urllib2.urlopen(req)
        print p.read()
    
    except Exception, e:
        print 'error',e

sendCallback('111',1)