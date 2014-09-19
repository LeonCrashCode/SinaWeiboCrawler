#!/usr/bin/python
#-*- coding=utf-8 -*-

import re

def getPageID(pagecontent):
    '''
    get main content
    '''
    pagecontent = pagecontent.replace("\\t","")
    pagecontent = pagecontent.replace("\\r","")
    pagecontent = pagecontent.replace("\\n","")
    pagecontent = pagecontent.replace("\\","")

    m = re.compile("\$CONFIG\['page_id'\]='(.*?)';").search(pagecontent)
    if m:
        return m.group(1)
    return ""

    
def process(pagecontent):
    return getPageID(pagecontent)
    
                                          
                                      
