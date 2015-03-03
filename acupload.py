#!/usr/bin/env python3
#coding:utf-8
# Author:  Beining --<ACICFG>
# Purpose:  Upload to Letvcloud via Acfun's API
# Created: 07/17/2014


import urllib2, urllib
import sys
import os
import json
import subprocess
import hashlib
import getopt
import logging
import traceback
from io import open

global VER
VER = u'0.05 Py2'
global cookiepath
cookiepath = u'./accookies'
global vu_list
vu_list = []
global ACUPLOAD_UA
ACUPLOAD_UA = u'AcUpload / ' + unicode(VER) + u' (cnbeining@gmail.com)'

#----------------------------------------------------------------------
def check_upload(source_id):
    u""""""
    request_info = urllib2.Request(u'http://api.letvcloud.com/gpc.php?&sign=signxxxxx&cf=html5&vu='+source_id+'&ver=2.1&ran=0.6220391783863306&qr=2&format=xml&uu=a04808d307')
    try:
        response = urllib2.urlopen(request_info)
        data = response.read()
        return json.loads(data.decode(u'utf-8'))[u'message']
    except:
        return u'Cannot check '+source_id+u' !'

########################################################################
class LetvUploadAPICannotReachException(Exception):

    u'''Deal with LetvUploadAPICannotReach to stop the main() function.'''
    #----------------------------------------------------------------------

    def __init__(self, value):
        self.value = value
    #----------------------------------------------------------------------

    def __str__(self):
        return repr(self.value)

########################################################################
class LetvUploadAPICannotReadException(Exception):

    u'''Deal with LetvUploadAPICannotReach to stop the main() function.'''
    #----------------------------------------------------------------------

    def __init__(self, value):
        self.value = value
    #----------------------------------------------------------------------

    def __str__(self):
        return repr(self.value)

########################################################################
class LetvUploadAPIErrorException(Exception):

    u'''Deal with LetvUploadAPIError to stop the main() function.'''
    #----------------------------------------------------------------------

    def __init__(self, value):
        self.value = value
    #----------------------------------------------------------------------

    def __str__(self):
        return repr(self.value)

########################################################################
class NotFileException(Exception):

    u'''Deal with NotFile to stop the main() function.'''
    #----------------------------------------------------------------------

    def __init__(self, value):
        self.value = value
    #----------------------------------------------------------------------

    def __str__(self):
        return repr(self.value)

#----------------------------------------------------------------------
def upload(file2Upload, proxytype = u'', proxy_address = u'', curl_args = u'', cookies = u''):
    u""""""
    #Read Cookie.....Damn it I didn't have my supper!
    #Damn why I still didn't have my supper when I edit it 6 months later!!!!!!!!!
    #Get filename
    filename = file2Upload.split(u'/')[-1].strip()
    #print(filename)
    if not os.path.isfile(file2Upload):
        raise NotFileException(u'Not file!')
    #Calculate Filesize
    #Not used to upload extreme large file, may cause problem
    filesize = os.path.getsize(file2Upload)
    #print(filesize)
    #Fetch UploadUrl
    request_full = urllib2.Request(u'http://www.acfun.tv/video/createVideo.aspx?type=letv&filesize=100000', headers={ u'User-Agent' : ACUPLOAD_UA, u'Cache-Control': u'no-cache', u'Pragma': u'no-cache' , u'Cookie': cookies,})
    try:
        response = urllib2.urlopen(request_full)
    except Exception:
        raise LetvUploadAPICannotReachException(u'Cannot get response from server!')
    data = response.read()
    uploadresponse = json.loads(data.decode(u'utf-8'))
    if uploadresponse[u"success"] is u'false':
        logging.error(u'ERROR: '+ uploadresponse[u'info'])
        raise LetvUploadAPIErrorException(u'ERROR: Not success!')
    #print(uploadresponse['upload_url'])
    try:
        #make filename
        remote_name = uploadresponse[u'sourceId'] + u'|' + unicode(filesize)
        status_url = uploadresponse[u'progress_url']
        source_id = uploadresponse[u'sourceId']
        #start upload
        upload_url = unicode(uploadresponse[u'upload_url'])
    except KeyError:
        logging.error(u'Cannot decode this one!')
        raise LetvUploadAPICannotReadException(u'Cannot decode this one!')
    #print(upload_url)
    print (u'Upload server IP address: ' + status_url.split(u'/')[2])
    proxy_args = u''
    if proxytype == u's':
        proxy_args = u'--socks5 "{proxy_address}"'.format(proxy_address = proxy_address)
    elif proxytype == u'h':
        proxy_args = u'-x "{proxy_address}"'.format(proxy_address = proxy_address)
    curl_cmd = u'curl -A "{ACUPLOAD_UA}" -F "file=@{filename}" {curl_args} {proxy_args} "{upload_url}" | cat #'.format(ACUPLOAD_UA = ACUPLOAD_UA, filename = filename, curl_args = curl_args, proxy_args = proxy_args, upload_url = upload_url)
    #print(curl_cmd)
    #os.system('curl -A \'\'  -F \"file=@'+filename+'\"  \"'+upload_url+'\" | cat #')
    os.system(curl_cmd)
    print (u'\n' + u'Hope everything is fine. {filename} , {source_id}'.format(filename = filename, source_id = source_id))
    vu_list.append([filename, source_id])

#----------------------------------------------------------------------
def cmd_exists(cmd):
    return subprocess.call(u"type " + cmd, shell=True, 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

#----------------------------------------------------------------------
def usage():
    u""""""
    print u'''    AcUpload
    
    https://github.com/cnbeining/Biligrab
    http://www.cnbeining.com/
    
    Beining@ACICFG
    
    Usage:
    
    python3 acupload.py (-h/--help) (-e/--examine) (-c/--cookie ./cookiepath) 
                        (-t/--proxy-type [h/s]) (-p/--proxy-address 127.0.0.1:8080)
                        (-a/--curl-args -V)
    
    -h/help: Default: None
        Print this usage file.
        
    -e/examine: Default: 0
        If enabled, acupload will examine all the uploads via the API.
        May return 404 if the speed is too fast.
    
    -c/cookie: Default:'./accookies'
        Set the path of cookie.
    
    -t/proxy-type: Default: Blank
        Set the type of proxy, if you want to use.
        s: SOCKS
        h: HTTP
    
    -p/proxy-address: Default: Blank
        Set the proxy address, if enabled by -t.
        Format:
        127.0.0.1:8080
    
    -a/curl-args: Default: Blank
        Other arguments you want ot put on curl.'''

#----------------------------------------------------------------------
def read_cookie(cookiepath):
    u"""str->list
    Original target: set the cookie"""
    try:
        cookies_file = open(cookiepath, u'r')
        cookies = cookies_file.readlines()
        cookies_file.close()
        # print(cookies)
        return cookies
    except:
        logging.warning(u'Cannot read cookie!')
        return [u'']

#----------------------------------------------------------------------
if __name__==u'__main__':
    #Test sys encoding
    IS_EXAMINE = 0
    proxytype, proxy_address, curl_args= u'', u'', u''
    if not sys.getdefaultencoding() is u'utf-8':
        os.system(u'export LC_ALL="en_US.UTF-8"')
    #Test curl
    proxytype = u''
    if not cmd_exists(u'curl'):
        logging.fatal(u'We need curl to upload your file! Get one with apt-get, yum or homebrew.')
        exit()
    argv_list = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv_list, u"hec:t:p:a:",
                                   [u'help', u"examine", u'cookie=', u'proxy-type=', u'proxy-address=', u'curl-args='])
    except getopt.GetoptError:
        usage()
        exit()
    for o, a in opts:
        if o in (u'-h', u'--help'):
            usage()
            exit()
        if o in (u'-c', u'--cookie'):
            cookiepath = a
        if o in (u'-e', u'--examine'):
            IS_EXAMINE = 1
        if o in (u'-t', u'--proxy-type'):
            proxytype = a
            print proxytype
            if proxytype != u's' and proxytype != u'h':
                logging.warning(u'Cannot read proxy type, will use no proxy!')
                proxytype = u''
        if o in (u'-p', u'--proxy-address'):
            proxy_address = a
        if o in (u'-a', u'--curl-args'):
            curl_args = a
    total_file_num = len(args)
    if total_file_num == 0:
        logging.fatal(u'No input file to upload!')
        exit()
    try:
        #move here to avoid reading it multiple times
        cookies = open(cookiepath, u'r').readline()
        #print(cookies)
    except:
        logging.fatal(u'I am hungry, please give me your Cookie!')
        exit()
    i = 0
    for file2Upload in args:
        #print(name)
        i = i + 1
        print (u'Uploading '+ unicode(i)+u' in '+unicode(total_file_num)+u' files...')
        try:
            upload(file2Upload, proxytype= proxytype, proxy_address= proxy_address, curl_args = curl_args, cookies = cookies)
        except Exception, e:
            print (u'ERROR: AcUpload failed: %s' % e)
            print u'       If you think this should not happen, please open a issue at https://github.com/cnbeining/acupload/issues .'
            print u'       Make sure you delete all the sensive data before you post it publicly.'
            traceback.print_exc()
            pass
    #os.system('export LC_ALL="en_US.UTF-8"')
    COOKIE = read_cookie(cookiepath)[0]
    if COOKIE == u'':
        logging.error(u'Cannot get upload URL due to lack of cookie!')
        exit()
    #makes this selectable
    if IS_EXAMINE == 1:
        for media in vu_list:
            try:
                print (media[0] + u',' + media[1] + u','+check_upload(media[1]))
            except Exception, e:
                print (u'ERROR: AcUpload examination failed: %s' % e)
                print u'       If you think this should not happen, please open a issue at https://github.com/cnbeining/acupload/issues .'
                print u'       Make sure you delete all the sensive data before you post it publicly.'
                traceback.print_exc()
                pass
