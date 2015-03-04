#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# File http_post.py

import urllib
import urllib2
import json
import socket

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

HEADER_INFO = "'Content-Type' : 'application/json;charset=UTF-8'"

DUILIAN_SERVERHOST ="http://duilian.msra.cn/zimi/LightAnswerService.svc/Answer"
DUILIAN_QUESTION1 ='{"question":"高人一等","engineType":0,"topic":0,"focuseAnswerType":"字谜"}'
DUILIAN_QUESTION2 ='{"question":"高人一等","engineType":0,"topic":0,"focuseAnswerType":"出字谜"}'

DUILIAN2_SERVERHOST ="http://couplet.msra.cn/zimi/LightAnswerService.svc/Answer"
DUILIAN2_QUESTION1='{"question":"高人一等","engineType":0,"topic":0,"focuseAnswerType":"字谜"}'
DUILIAN2t_QUESTION2='{"question":"高人一等","engineType":0,"topic":0,"focuseAnswerType":"出字谜"}'

STRING_SERVERHOST ='http://couplet.msra.cn/app/CoupletsWS_V2.asmx/IsValidChineseString'
STRING_QUESTION = '{"inputString":"海阔凭鱼跃"}'

COUPLET_SERVERHOST = 'http://couplet.msra.cn/app/CoupletsWS_V2.asmx/GetXiaLian'
COUPLET_QUESTION = '{"shanglian":"海阔凭鱼跃","xialianLocker":"00000","isUpdate":false}'


COUPLET2_SERVERHOST = 'http://couplet.msra.cn/app/CoupletsWS_V2.asmx/GetHengPi'
COUPLET2_QUESTION = '{"shanglian":"海阔凭鱼跃","xialian":"天高任鸟飞"}'

def post_zimi(url,values):
    socket.setdefaulttimeout(2000)
    req = urllib2.Request(url,data=values,headers = {'Content-Type' : 'application/json;charset=UTF-8'})       # 生成页面请求的完整数据
    response = urllib2.urlopen(req)       # 发送页面请求
    return response.read()                    # 获取服务器返回的页面信息


def post_zimi_agent_header(url,values):
    req = urllib2.Request(url,data=urllib.urlencode(values))
    length = len(user_agents)
    index = random.randint(0, length-1)
    user_agent = user_agents[index]
    req.add_header('User-agent', user_agent)
    #request.add_header('connection','keep-alive')
    response = urllib2.urlopen(req,timeout=60)
    rep = urllib2.urlopen(req,timeout=60).read()
    result = json.loads(rep)
    print rep


url=SERVERHOST

resp = post_zimi(url,values2)
jdata = json.loads(resp)
print jdata
