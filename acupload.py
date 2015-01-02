#!/usr/bin/env python
#coding:utf-8
# Author:  Beining --<ACICFG>
# Purpose:  Upload to Letv via Acfun's API
# Created: 01/01/2015

#python acup.py 0.flv 1.flv

import urllib2, urllib
import sys
import os
import json
import subprocess
import hashlib
from io import open

global cookiepath
cookiepath = u'./accookies'
global vu_list
vu_list = []

#----------------------------------------------------------------------
def check_upload(source_id):
    u""""""
    str2Hash = u'cfflashformatjsonran0.7214574650861323uu2d8c027396ver2.1vu' + source_id + u'bie^#@(%27eib58'
    sign = hashlib.md5(str2Hash.encode(u'utf-8')).hexdigest()
    request_info = urllib2.Request(u'http://api.letvcloud.com/gpc.php?&sign='+sign+u'&cf=flash&vu='+source_id+u'&ver=2.1&ran=0.7214574650861323&qr=2&format=json&uu=2d8c027396')
    try:
        response = urllib2.urlopen(request_info)
        data = response.read()
        return json.loads(data.decode(u'utf-8'))[u'message']
    except:
        return u'Cannot check '+source_id+u' !'


#----------------------------------------------------------------------
def upload(file2Upload):
    u""""""
    #Read Cookie.....Damn it I didn't have my supper!
    try:
        cookies = open(cookiepath, u'r').readline()
        #print(cookies)
    except:
        print u'I am hungry, please give me your Cookie!'
        exit()
    #Get filename
    filename = file2Upload.split(u'/')[-1].strip()
    #print(filename)
    if not os.path.isfile(file2Upload):
        print u'Not file!'
        pass
    #Calculate Filesize
    #Not used to upload extreme large file, may cause problem
    #filesize = os.path.getsize(file2Upload)
    #print(filesize)
    #Fetch UploadUrl
    request_full = urllib2.Request(u'http://www.acfun.tv/video/createVideo.aspx?type=letv&filesize=100000', headers={ u'User-Agent' : u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', u'Cache-Control': u'no-cache', u'Pragma': u'no-cache' , u'Cookie': cookies,})
    try:
        response = urllib2.urlopen(request_full)
    except Exception:
        print u'Cannot get response from server!'
        pass
    data = response.read()
    uploadresponse = json.loads(data.decode(u'utf-8'))
    if uploadresponse[u"success"] is u'false':
        print u'ERROR: '+ uploadresponse[u'info']
        exit()
    #print(uploadresponse['upload_url'])
    #make filename
    remote_name = uploadresponse[u'sourceId'] + u'|' + unicode(filesize)
    status_url = uploadresponse[u'progress_url']
    source_id = uploadresponse[u'sourceId']
    #start upload
    upload_url = unicode(uploadresponse[u'upload_url'])
    #print(upload_url)
    os.system(u'curl   -F \"file=@'+filename+u'\"  \"'+upload_url+u'\" | cat #')
    print u'\n'+u'Hope everything is fine. '+source_id
    vu_list.append([filename, source_id])

#----------------------------------------------------------------------
def cmd_exists(cmd):
    return subprocess.call(u"type " + cmd, shell=True, 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

#----------------------------------------------------------------------
if __name__==u'__main__':
    #Test sys encoding
    if not sys.getdefaultencoding() is u'utf-8':
        os.system(u'export LC_ALL="en_US.UTF-8"')
    #Test curl
    if not cmd_exists(u'curl'):
        print u'We need curl to upload your file! Get one with apt-get or yum.'
        exit()

    total_file_num = len(sys.argv[1:])
    i = 0
    for name in sys.argv[1:]:
        #print(name)
        i = i + 1
        print u'Uploading '+ unicode(i)+u' in '+unicode(total_file_num)+u' files...'
        upload(name)
    os.system(u'export LC_ALL="en_US.UTF-8"')
    for media in vu_list:
        print media[0] + u', ' + media[1] + u', '+check_upload(media[1])
