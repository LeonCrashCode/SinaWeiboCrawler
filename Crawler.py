#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import time
class Crawler:
    '''
    a crawler class
    variables
        list(string): proxy
    functions
        bytes[] url_get(string url, dict para)
    '''
    def __init__(self):
        urllib2.socket.setdefaulttimeout(10)
        self.Proxy = list()
        self.ProxyIter = 0
        self.cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(self.cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
    def url_get(self,url,para,headers):
        time.sleep(0.5)
        params = urllib.urlencode(para)
        req = urllib2.Request(url,params,headers)
        respones = urllib2.urlopen(req)
        return respones.read()

    
        

