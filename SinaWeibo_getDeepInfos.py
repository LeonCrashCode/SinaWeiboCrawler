#!/usr/bin/python
#-*- coding=utf-8 -*-

import re

def getContent(pagecontent):
    '''
    get main content
    '''
    pagecontent = pagecontent.replace("\\t","")
    pagecontent = pagecontent.replace("\\r","")
    pagecontent = pagecontent.replace("\\n","")
    pagecontent = pagecontent.replace("\\","")

    Title = ""
    m = re.compile("\$CONFIG\['onick'\]='(.*?)';").search(pagecontent)
    if m:
        Title = m.group(1)

    #person V
    V_Info = ""
    p = re.compile("<i title= \"(.*?)\" class=\"W_ico16 approve\">")
    m = p.search(pagecontent)
    if m:
        V_Info = m.group(1)
    
    #organization V
    if V_Info == "":
        p = re.compile("<div class=\"identity_info S_txt2\">(.*?)</div>")
        m = p.search(pagecontent)
        if m:
            V_Info = re.sub('<[^>]+>','',m.group(1))
            V_Info = re.sub('\s+',' ',V_Info)
            
    Abstract = ""
    p = re.compile("<div class=\"pf_intro bsp\"><.*?>(.*?)</span></div>")
    m = p.search(pagecontent)
    if m:
        Abstract = re.sub('<[^>]+>','',m.group(1))
        Abstract = re.sub('\s+',' ',Abstract)

    maincontent = ""
    p = re.compile("\"domid\":\"Pl_Official_LeftInfo(.*?)</script>")
    m = p.search(pagecontent)
    if m:
        maincontent = m.group(1)
    return maincontent,V_Info,Abstract,Title

def getInfo(pagecontent):
    maincontent,V_Info,Abstract,Title = getContent(pagecontent)
    p = re.compile("<div class=\"label S_txt2\">(.*?)</div>")
    TypeList = p.findall(maincontent)
    p = re.compile("<div class=\"con.*?>(.*?)</div>")
    ValueList = p.findall(maincontent)

    ret = dict()
    ret["Title"] = Title
    ret["Abstract"] = Abstract
    ret["V_Info"] = V_Info
    num = 1
    if len(TypeList) == len(ValueList):
        for i in range(len(TypeList)):
            ValueList[i] = re.sub('<[^>]+>',' ',ValueList[i])
            ValueList[i] = re.sub('\s+',' ',ValueList[i])
            ret[str(num)+"_"+TypeList[i]] = ValueList[i]
            num += 1
    return ret
    
def process(pagecontent):
    return getInfo(pagecontent)

