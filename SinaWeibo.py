#!/usr/bin/python
#-*- coding:utf-8 -*-

import re
import base64
import types
import MySQLdb

import Crawler
import SinaWeibo_encodeUsrname
import SinaWeibo_encodePassword
import SinaWeibo_getFollows
import SinaWeibo_getPageID
import SinaWeibo_getDeepInfos

class SinaWeibo:
    def __init__(self, usrname, password, change):
        self.preLogin_URL = "http://login.sina.com.cn/sso/prelogin.php"
        self.Login_URL = "http://login.sina.com.cn/sso/login.php"
        self.servertime = ""
        self.nonce = ""
        self.usrname = usrname
        self.password = password
        if change:
            self.change()
        self.crawler = Crawler.Crawler()
        self.Queue = list()
        
        self.Queue_limit = 1000000
        
        #self.log = open("log","w")
        #for mysqldb
        self.conn = conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="SinaWeibo",port=3307)
        self.cursor = conn.cursor()

        self.existuid = list()
        sql = "select uid from usr_relation";
        self.cursor.execute(sql)
        while True:
            row = self.cursor.fetchone()
            if row:
                pass
            else:
                break;
            if row[0]!="":
                self.existuid.append(row[0])
        
    def change(self):
        nl = list(self.usrname[::-1])
        newusrname = ""
        for i in range(len(nl)):
            newusrname+= chr(ord(nl[i])-5)
            
        pl = list(self.password[::-1])
        newpassword = ""
        for i in range(len(pl)):
            newpassword+= chr(ord(pl[i])-i-1)
        self.usrname = newusrname
        self.password= newpassword
    def preLogin(self):
        '''
        get values of
            servertime
            nonce
            pubkey
            rsakv
        '''
        para = dict()
        para['entry'] = 'sso'
        para['callback'] = 'sinaSSOController.preloginCallBack'
        para['su'] = self.usrname
        para['rsakt'] = 'mod'
        para['client'] = 'ssologin.js(v1.4.18)'

        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11'}         
        content = self.crawler.url_get(self.preLogin_URL,para,headers)

        p = re.compile("\"servertime\":(.*?),")
        m = p.search(content)
        if m:
            self.servertime = m.group(1)
            
        p = re.compile("\"nonce\":\"(.*?)\"")
        m = p.search(content)
        if m:
            self.nonce = m.group(1)
            
        p = re.compile("\"pubkey\":\"(.*?)\"")
        m = p.search(content)
        if m:
            self.pubkey = m.group(1)
            
        p = re.compile("\"rsakv\":\"(.*?)\"")
        m = p.search(content)
        if m:
            self.rsakv = m.group(1)
    def Login(self):
        '''
        get values of
            ajax sites
        '''
        para = dict()
        para['client'] = 'ssologin.js(v1.4.18)'
        para['entry'] = 'weibo'
        para['gateway'] = '1'
        para['from'] = ''
        para['savestate'] = '7'
        para['useticket'] = '1'
        para['vsnf'] = '1'
        para['ssosimplelogin'] = '1'
        #main
        para['su'] = SinaWeibo_encodeUsrname.encodeUsrname(self.usrname)
        
        para['service'] = 'miniblog'
        para['servertime'] = self.servertime
        para['nonce'] = self.nonce
        para['pwencode'] = 'rsa2'
        #main
        para['sp'] = SinaWeibo_encodePassword.encodePassword(self.password,self.servertime,self.nonce,self.pubkey)
        
        para['encoding'] = 'UTF-8'
        para['prelt'] = '115'
        para['rsakv'] = self.rsakv
        para['url'] = 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack'
        para['returetype'] = 'META'
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11'}         
        content = self.crawler.url_get(self.Login_URL,para,headers)
        p = re.compile("location.replace\(\'(.*?)\'\)")
        m = p.search(str(content))
        if m:
            self.ajax_URL = m.group(1)
    def ajaxLogin(self):
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11'} 
        content = self.crawler.url_get(self.ajax_URL,{},headers)
    def getCookies(self):
        '''
        get cookies and save to urllib2
        '''
        self.preLogin()
        self.Login()
        self.ajaxLogin()

    '''
    following funtion can be used to extract many information
    under the cookies saved in self.crawler
    '''

    def mainpage(self):
        para =dict()
        para['wvr']='5'
        para['lf']='reg'
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11','Referer':'http://weibo.com/leonova'} 
        content = self.crawler.url_get("http://weibo.com/leonova/home",para,headers)
        #print content
    def follower(self,uid):

        if uid in self.existuid:
            if len(self.Queue) >= self.Queue_limit:
                return
            sql = "select follows from usr_relation where uid='"+uid+"'";
            self.cursor.execute(sql)
            while True:
                row = self.cursor.fetchone()
                if row:
                    pass
                else:
                    break;
                follows = row[0].split("$")
                for follow in follows:
                    if len(self.Queue) >= self.Queue_limit:
                        return
                    if follow.strip() == "":
                        continue
                    self.Queue.append(follow)
            return
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11','Referer':'http://weibo.com/leonova'} 
        content = self.crawler.url_get("http://weibo.com/u/"+uid,{},headers)
        PageID = SinaWeibo_getPageID.process(content)
        content = self.crawler.url_get("http://weibo.com/p/"+PageID+"/info",{},headers)

        '''
        FollowNumber = SinaWeibo_getFollows.getNumber(content)
        if FollowNumber >= 3000:
            return
        FanNumber = SinaWeibo_getFollows.getFanNumber(content)
        WeiboNumber = SinaWeibo_getFollows.getWeiboNumber(content)
        '''
        FollowNumber,FanNumber,WeiboNumber = SinaWeibo_getFollows.getAllNumber(content)
        if FollowNumber == 0 and FanNumber == 0 and WeiboNumber == 0:
            return
        Infos = SinaWeibo_getDeepInfos.process(content)
        
        
        '''
        self.log.write("uid: "+uid+"\t")
        self.log.write("Title: "+str(Infos["Title"])+"\t")
        self.log.write("Abstract: "+str(Infos["Abstract"])+"\t")
        self.log.write("V_Info: "+str(Infos["V_Info"])+"\t")
        self.log.write("Follows: "+str(FollowNumber)+"\t")
        self.log.write("Fans: "+str(FanNumber)+"\t")
        self.log.write("Weibos: "+str(WeiboNumber)+"\t")
        for item in Infos:
            if item == "V_Info" or item == "Abstract" or item == "Title":
                continue
            if type(Infos[item]) == types.StringType:
                self.log.write(item+": "+str(Infos[item])+"\t")
            elif type(Infos[item]) == types.ListType:
                self.log.write(item+": ")
                for v in Infos[item]:
                    self.log.write(str(v)+" ")
                self.log.write("\t")
        self.log.write("\n")
        self.log.flush()
        '''
        tmp = ""
        for item in Infos:
            if item == "V_Info" or item == "Abstract" or item == "Title":
                continue
            if type(Infos[item]) == types.StringType:
                tmp += item+":"+str(Infos[item])+"$split$"
            elif type(Infos[item]) == types.ListType:
                tmp += item+":"
                for v in Infos[item]:
                    tmp += str(v)+" "
                tmp += "$split$"
        

        
        loop=0
        if FollowNumber%20 == 0:
            loop = (FollowNumber/20)+1
        else:
            loop = (FollowNumber/20)+2
        follows = ""
        for i in range(loop)[1:]:
            content = self.crawler.url_get("http://weibo.com/p/"+PageID+"/follow?page="+str(i),{},headers)
            FollowList = SinaWeibo_getFollows.process(content)
            for follow in FollowList:
                if follow['uid'].strip() == "":
                    continue
                follows += str(follow['uid'])+"$"
                if follow['uid'] in self.existuid:
                    continue
                if len(self.Queue) >= self.Queue_limit:
                    continue
                self.Queue.append(follow['uid'])

        
        sql = "insert into usr_basic_info(uid,title,intro,V_Info) values('"+uid+"','"+str(Infos["Title"]).replace("'","\"")+"','"+str(Infos["Abstract"]).replace("'","\"")+"','"+str(Infos["V_Info"]).replace("'","\"")+"')";
        self.cursor.execute(sql)
        sql = "insert into usr_deep_info(uid,info) values('"+uid+"','"+tmp.replace("'","\"")+"')"
        self.cursor.execute(sql)
        sql = "insert into usr_relation(uid,follow_count,fan_count,weibo_count,follows) values('"+uid+"',"+str(FollowNumber)+","+str(FanNumber)+","+str(WeiboNumber)+",'"+follows+"')";
        self.cursor.execute(sql)
        self.existuid.append(uid)
        #print content
    def CrawlFollowers(self,seed):
        self.Queue.append(seed)
        while len(self.Queue) != 0:
            uid = self.Queue[0]
            print uid
            self.Queue = self.Queue[1:]
            self.follower(uid)
            self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
if __name__ == "__main__":
    usrname = ""
    password = ""
    sina = SinaWeibo(usrname,password,"False")
    sina.getCookies()
    #sina.mainpage()
    sina.CrawlFollowers("1480448774")
    
