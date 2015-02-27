#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# Create by yunbo.
#
# Last updated: 2013-09-26
#
# fetch the pdf file of paper from google scholar

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2, socket, time
import re, random, types

from bs4 import BeautifulSoup 

base_url = 'http://scholar.google.com'

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

# results from the search engine
# basically include url, title,content
class SearchResult:
    def __init__(self):
        self.url= '' 
        self.title = '' 
        self.author = ''
        self.abstract = ''
        self.citeinfo = ''
        self.organization = ''
        self.basepath = ''

    def getURL(self):
        return self.url

    def setURL(self, url):
        self.url = url 

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title
    
    def getAuthor(self):
        return self.author
    
    def setAuthor(self,author):
        self.author = author
    
    def getAbstract(self):
        return self.abstract
    
    def setAbstract(self,abstract):
        self.abstract = abstract
    
    def getCiteinfo(self):
        return self.citeinfo
    
    def setCiteinfo(self,citeinfo):
        self.citeinfo = citeinfo
    
    def getOrganization(self):
        return self.organization
    
    def setOrganization(self,organization):
        self.organization = organization

    def printIt(self, prefix = ''):
        print 'url\t->', self.url
        print 'title\t->', self.title
        print 'abstract\t->', self.abstract
        print 'author\t->',self.author
        print 'citinfo\t->',self.citeinfo
        print 'organization\t->',self.organization
        print 

    def writeFile(self, filename):
        file = open(filename, 'a')
        try:
            file.write('url:' + self.url+ '\n')
            file.write('title:' + self.title + '\n')
            file.write('abstract:' + self.abstract + '\n')
            file.write('author:' + self.author + '\n')
            file.write('citinfo:' + self.citeinfo + '\n')
            file.write('organization:' + self.organization+'\n\n')

        except IOError, e:
            print 'file error:', e
        finally:
            file.close()

    def downloadPdf(self):
        try:
            request = urllib2.Request(self.url)
            length = len(user_agents)
            index = random.randint(0, length-1)
            user_agent = user_agents[index]
            request.add_header('User-agent', user_agent)
            request.add_header('connection','keep-alive')
            response = urllib2.urlopen(request)
            content = response.read()
            pdfpath = self.basepath+self.title+'.pdf'
            f = open(pdfpath,'wb')
            f.write(content)
            f.close
        except urllib2.URLError,e:
            print 'url error:', e
            return
        except IOError, e:
            print 'file error:', e
                
        except Exception, e:
            print 'error:', e
            return


class GoogleAPI:
    def __init__(self):
        timeout = 40
        socket.setdefaulttimeout(timeout)

    def randomSleep(self):
        sleeptime =  random.randint(60, 120)
        time.sleep(sleeptime)

    #extract the domain of a url
    def extractDomain(self, url):
        domain = ''
        pattern = re.compile(r'http[s]?://([^/]+)/', re.U | re.M)
        url_match = pattern.search(url)
        if(url_match and url_match.lastindex > 0):
            domain = url_match.group(1)

        return domain
    
    def extractOrganzation(self,info):
        #'[PDF] from researchgate.netresearchgate.net [PDF]'
        info = re.sub(r'</?\w+[^>]*>','',info)
        info = re.sub(r'\[PDF\]','',info)
        string1 = info.strip()
        string2 = string1[len(string1)/2+3:]
        return string2
    
    # extract serach results list from downloaded html file
    def extractSearchResults(self, html):
        results = list()
        soup = BeautifulSoup(html)
        bdy_div = soup.find('div', id  = 'gs_bdy')
        if (type(bdy_div) == types.NoneType):
            return results
        
        resbdy_div = bdy_div.find('div', id  = 'gs_res_bdy')
        if (type(resbdy_div) == types.NoneType):
            return results
        
        ccl_div = resbdy_div.find('div', id  = 'gs_ccl')
        if (type(ccl_div) == types.NoneType):
            return results
    
        total = 0
        if (type(ccl_div) != types.NoneType):
            lis = ccl_div.findAll('div', {'class': 'gs_r'})
            if(len(lis) > 0):
                for li in lis:
                    result = SearchResult()
                    
                    result_div = li.find('div', {'class': 'gs_ggs gs_fl'})
                    #print "1=====>"+str(result_div)
                    if(type(result_div) == types.NoneType):
                        continue
                    
                    link_div = result_div.find('div', {'class': 'gs_md_wp gs_ttss'})
                    #print "2=====>"+str(link_div)
                    if(type(link_div) == types.NoneType):
                        continue

                    # extract domain and title from h3 object
                    link = link_div.find('a')
                    if (type(link) == types.NoneType):
                        continue

                    url = link['href']
                    if(cmp(url, '') == 0):
                        continue
                            
                    organization = link.renderContents()
                    organization = self.extractOrganzation(organization)

                    result.setURL(url)
                    result.setOrganization(organization)

                    #find paper title+author+abstract
                    ri_div = li.find('div', {'class': 'gs_ri'})
                    #print "1=====>"+str(ri_div)
                    if(type(ri_div) != types.NoneType):
                        #get title
                        rt_div = ri_div.find('h3', {'class': 'gs_rt'})
                        if(type(rt_div) != types.NoneType):
                            link = rt_div.find('a')
                            #print link
                            if(type(link) != types.NoneType):
                                title = link.renderContents()
                                title = re.sub(r'</?\w+[^>]*>','',title)
                                result.setTitle(title)

                
                        #get author
                        gs_a_div = ri_div.find('div', {'class': 'gs_a'})
                        if(type(gs_a_div) != types.NoneType):
                            #或者作者主页
                            author = gs_a_div.renderContents()
                            author = re.sub(r'</?\w+[^>]*>','',author)
                            result.setAuthor(author)

                        #get abstract
                        gs_rs_div = ri_div.find('div', {'class': 'gs_rs'})
                        if(type(gs_rs_div) != types.NoneType):
                            abstract = gs_rs_div.renderContents()
                            abstract = re.sub(r'</?\w+[^>]*>','',abstract)
                            result.setAbstract(abstract)

                        #get citeinfo
                        gs_fl_div = ri_div.find('div', {'class': 'gs_fl'})
                        if(type(gs_fl_div) != types.NoneType):
                            citeinfo = gs_fl_div.renderContents()
                            citeinfo = re.sub(r'</?\w+[^>]*>','',citeinfo)
                            result.setCiteinfo(citeinfo)
                    #end detail information

                    results.append(result)
                    total += 1
                    print "total files=%d"%(total)
        return results

    # search web
    # @param query -> query key words 
    # @param lang -> language of search results  
    # @param num -> number of search results to return 
    def search(self, query, lang='en', num=20):
        query = urllib2.quote(query)
        search_results = list()
        url = '%s/scholar?hl=%s&num=%d&q=%s' % (base_url, lang, num,query)
        print url
        str = ''
        retry = 3
        while(retry > 0):
            try:
                request = urllib2.Request(url)
                length = len(user_agents)
                index = random.randint(0, length-1)
                user_agent = user_agents[index] 
                request.add_header('User-agent', user_agent)
                request.add_header('connection','keep-alive')
                response = urllib2.urlopen(request)
                html = response.read() 
                results = self.extractSearchResults(html)
                
                next_page =''
                soup=BeautifulSoup(html)
                link_td = soup.find('td',{'align':'left'})
                if (type(link_td) != types.NoneType):
                    #print link_td
                    next_a = link_td.find('a')
                    if (type(next_a) != types.NoneType):
                            next_page = base_url + next_a['href']
                print next_page+'\n'
                
                return results
            except urllib2.URLError,e:
                print 'url error:', e
                self.randomSleep()
                retry = retry - 1
                continue
            
            except Exception, e:
                print 'error:', e
                retry = retry - 1
                self.randomSleep()
                continue
        return search_results
        
def test():
    if(len(sys.argv) < 2):
        print 'please enter search query.'
        return
    query = sys.argv[1]
    api = GoogleAPI()
    result = api.search(query)
    for r in result:
        r.printIt()
        r.writeFile('scholar_google_result.txt')
        r.downloadPdf()

if __name__ == '__main__':
    test()

