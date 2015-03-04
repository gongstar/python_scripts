#coding=utf-8
import urllib
import urllib2
import string
import sys

from bs4 import BeautifulSoup
user_agent = 'Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0'  #自己描述的一个用户代理
headers = { 'User-Agent' : user_agent }
values = {'q' : sys.argv[1] }   #这个'q'就是get方法的那个input的‘name’，上面已经指出
data = urllib.urlencode(values)
request = urllib2.Request("http://dict.youdao.com/search", data, headers)  #这是搜索的ation的页面，上面已经指出
response = urllib2.urlopen(request)
the_page = response.read()
pool = BeautifulSoup(the_page)
results = pool.find('div', attrs={'class':'trans-wrapper clearfix','id':'phrsListTab'}) #看图，因为直接寻找'class':'trans-container'
                                                     #内容太多，多层过滤了一下
results = results.find('div', attrs={'class':'trans-container'}).find('ul').findAll('li') #根据网站设计的标签 找到所有符合项
translations = []
for result in results:
    data=result.getText().split('.')
    data[0]=data[0]+'.'
    translations.append((data[0],data[1]))
print u'查询词－>'+sys.argv[1].decode('utf-8')+u'的结果:'
for translation in translations:
    print "%s => %s" % (translation[0], translation[1])

