#coding:utf-8
import re
import urllib
import urllib2
import pprint
import logging
import random
import json
from sets import Set

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
               (KHTML, like Gecko) Element Browser 5.0', \
               'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
               'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
               'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
               Version/6.0 Mobile/10A5355d Safari/8536.25', \
               'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/28.0.1468.0 Safari/537.36', \
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

allwords = Set()


def fetch_page_get(url):
    request = urllib2.Request(url)
    length = len(user_agents)
    index = random.randint(0, length-1)
    user_agent = user_agents[index]
    request.add_header('User-agent', user_agent)
    #request.add_header('connection','keep-alive')
    response = urllib2.urlopen(request,timeout=2000)
    htmldata = response.read()
    return htmldata

def fetch_page(url,values):
    request = urllib2.Request('http://api.pullcore.com/post.php',data=urllib.urlencode(values))
    length = len(user_agents)
    index = random.randint(0, length-1)
    user_agent = user_agents[index]
    request.add_header('User-agent', user_agent)
    #request.add_header('connection','keep-alive')
    response = urllib2.urlopen(request,timeout=2000)
    htmldata = response.read()
    return htmldata

def loadtextlist(filename):
    textlist=[]
    file = open(filename)
    lines = file.readlines()
    file.close()
    
    for line in lines:
        line = line.strip()
        textlist.append(line)
    return textlist

def extractword(buf):
    global allwords
    items = buf.split('\n')
    for item in items:
        if len(item) < 1: continue
        #print item
        allwords.add(item)
    pass


#pullword interface
#get method: http://api.pullcore.com/get.php
#post method: http://api.pullcore.com/post.php
#source=[a paragraph of chinese words] for example: source=清华大学是好学校
#param1=[debug] no use now, just set 0
#param2=[debug] no use now, just set 1

if __name__ == '__main__':
    
    textlist = loadtextlist('asr_result.txt')
    i = 0
    for text in textlist:
        #s = urllib.quote_plus(text)
        url = 'http://api.pullcore.com/get.php?source=%s&param1=1&param2=0'%text
        values= {"source":text, "param1":1, "param2":0}
        print url
        ret =  fetch_page(url,values);
        extractword(ret)
                      
        if i > 2: break
        i += 1

    for word in allwords:
        print word

