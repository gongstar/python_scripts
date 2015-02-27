#!/usr/bin/env python
#coding=utf-8

import os
import math
import random
import shutil
import uuid
import sys
import urllib
import urllib2
import json
import time
from threading import Thread
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


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

# HTTP GET
def post_get_url(url):
    req = urllib2.Request(url)
    rep = urllib2.urlopen(req,timeout=60).read()
    result = json.loads(rep)
    print rep

# HTTP POST
def post_post_file(url,path):
    data,headers = multipart_encode({'file':open(path,'rb')})
    req = urllib2.Request(url,data,headers)
    rep = urllib2.urlopen(req,timeout=60).read()
    result = json.loads(rep)
    print rep


# HTTP GET with header
def post_recog_file_with_header(url):
    req = urllib2.Request(url)
    length = len(user_agents)
    index = random.randint(0, length-1)
    user_agent = user_agents[index]
    req.add_header('User-agent', user_agent)
    #request.add_header('connection','keep-alive')
    response = urllib2.urlopen(req,timeout=60)
    rep = urllib2.urlopen(req,timeout=60).read()
    result = json.loads(rep)
    print rep



testurl = 'http://api.qrserver.com/v1/read-qr-code/?fileurl=http%3A%2F%2Fapi.qrserver.com%2Fv1%2Fcreate-qr-code%2F%3Fdata%3DHelloWorld'

testurl2 = 'http://api.qrserver.com/v1/read-qr-code/'

test_image_path = 'qrcode1.jpg'

if __name__ == '__main__':
    register_openers()
    post_get_url(testurl)
    post_post_file(testurl2,test_image_path)
    post_recog_file_with_header(testurl)






