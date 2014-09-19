#!/usr/bin/python
#-*- coding=utf-8 -*-

import re

def getNumber(pagecontent):
    pagecontent = pagecontent.replace("\\t","")
    pagecontent = pagecontent.replace("\\r","")
    pagecontent = pagecontent.replace("\\n","")
    pagecontent = pagecontent.replace("\\","")

    #p =re.compile("<a class=\"S_func1\".*?mod=.*?follow\">.*?<strong.*?>([0-9]*?)</strong>")
    p = re.compile("<strong.*?>(.*?)</strong>.*?<span>关注</span>")
    m = p.search(pagecontent)
    if m:
        #print m.group(1)
        return int(m.group(1))
    return 0

def getFanNumber(pagecontent):
    pagecontent = pagecontent.replace("\\t","")
    pagecontent = pagecontent.replace("\\r","")
    pagecontent = pagecontent.replace("\\n","")
    pagecontent = pagecontent.replace("\\","")

    #p =re.compile("<a class=\"S_func1\".*?mod=.*?fans\">.*?<strong.*?>([0-9]*?)</strong>")
    p = re.compile("<strong.*?>(.*?)</strong>.*?<span>粉丝</span>")
    m = p.search(pagecontent)
    if m:
        #print m.group(1)
        return int(m.group(1))
    return 0

def getWeiboNumber(pagecontent):
    pagecontent = pagecontent.replace("\\t","")
    pagecontent = pagecontent.replace("\\r","")
    pagecontent = pagecontent.replace("\\n","")
    pagecontent = pagecontent.replace("\\","")

    #p =re.compile("<a class=\"S_func1\".*?mod=.*?weibo\">.*?<strong.*?>([0-9]*?)</strong>")
    p = re.compile("<strong.*?>(.*?)</strong>.*?<span>微博</span>")
    m = p.search(pagecontent)
    if m:
        #print m.group(1)
        return int(m.group(1))
    return 0

def getAllNumber(pagecontent):
    pagecontent = pagecontent.replace("\\t","")
    pagecontent = pagecontent.replace("\\r","")
    pagecontent = pagecontent.replace("\\n","")
    pagecontent = pagecontent.replace("\\","")

    part = pagecontent.split("pf_head_pic")
    if len(part) >= 2:
        pagecontent = part[1]
    #p =re.compile("<a class=\"S_func1\".*?mod=.*?weibo\">.*?<strong.*?>([0-9]*?)</strong>")
    p = re.compile("<strong.*?>([0-9]*?)</strong>")
    numlist = p.findall(pagecontent)
    if len(numlist) <3:
        return 0,0,0
    else:
        return int(numlist[0]),int(numlist[1]),int(numlist[2])
def getContentList(pagecontent):
    '''
    get main content
    '''
    pagecontent = pagecontent.replace("\\t","")
    pagecontent = pagecontent.replace("\\r","")
    pagecontent = pagecontent.replace("\\n","")
    pagecontent = pagecontent.replace("\\","")
    #p = re.compile("<script>STK && STK\.pageletM && STK\.pageletM\.view\(\{\"pid\":\"pl_relation_myfollow\"(.*?)</script>")
    p = re.compile("FM.view\(\{\"ns\":\"pl.content.followTab.index\"(.*?)</script>")
    maincontent = ""
    m = p.search(pagecontent)
    if m:
        maincontent = m.group(1)
    #return maincontent.split("<div class=\"myfollow_list S_line2 SW_fun\"")
    return maincontent.split("<li class=\"clearfix S_line1\"")

def getFollowInfo(person):
    '''
    face = ""
    uid = ""
    nickname = ""
    p = re.compile("<img src=\"(.*?)\" usercard=\"id=(.*?)\" alt=\"(.*?)\" \/>")
    m = p.search(person)
    if m:
        face = m.group(1)
        uid = m.group(2)
        nickname = m.group(3)

    V = False
    if re.compile("class=\"W_ico16 approve\"").search(person):
        V = True

    Abstract = ""
    p = re.compile("<div class=\"intro S_txt2\">(.*?)</div>")
    m = p.search(person)
    if m:
        Abstract = m.group(1)
    
    return [face,uid,nickname,V,Abstract]
    '''
    uid = ""
    nickname = ""
    sex = ""
    p = re.compile("action-data=\"uid=(.*?)&fnick=(.*?)&sex=(.*?)\">")
    m = p.search(person)
    if m:
        uid = m.group(1)
        nickname = m.group(2)
        sex = m.group(3)
    '''
    face = ""
    p = re.compile("<img .*? src=\"(.*?)\">")
    m = p.search(person)
    if m:
        face = m.group(1)

    V = False
    if re.compile("class=\"W_ico16 approve\"").search(person):
        V = True
    '''

    '''
    way = ""
    p = re.compile("<div class=\"from W_textb\">.*?<a.*?class=\"S_link2\".*?>(.*?)</a>.*?</div>")
    m = p.search(person)
    if m:
        way = m.group(1)
    '''
    ret = dict()
    ret['uid'] = uid
    '''
    ret['nickname'] = nickname
    ret['sex'] = sex
    ret['face'] = face
    ret['V'] = V
    '''
    return ret
def process(pagecontent):
    ContentList = getContentList(pagecontent)
    FollowList = list()
    for content in ContentList[1:]:
        FollowList.append(getFollowInfo(content))
    return FollowList
                                          
                                      
