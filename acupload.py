#!/usr/bin/env python3
#coding:utf-8
# Author:  Beining --<ACICFG>
# Purpose:  Upload to Letvcloud via Acfun's API
# Created: 07/17/2014


import urllib.request
import sys
import os
import json
import subprocess
import hashlib
import getopt
import logging
import traceback

global VER
VER = '0.04 Py3'
global cookiepath
cookiepath = './accookies'
global vu_list
vu_list = []
global ACUPLOAD_UA
ACUPLOAD_UA = 'AcUpload / ' + str(VER) + ' (cnbeining@gmail.com)'

#----------------------------------------------------------------------
def check_upload(source_id):
    """"""
    str2Hash = 'cfflashformatjsonran0.7214574650861323uu2d8c027396ver2.1vu' + source_id + 'bie^#@(%27eib58'
    sign = hashlib.md5(str2Hash.encode('utf-8')).hexdigest()
    request_info = urllib.request.Request('http://api.letvcloud.com/gpc.php?&sign='+sign+'&cf=flash&vu='+source_id+'&ver=2.1&ran=0.7214574650861323&qr=2&format=json&uu=2d8c027396')
    try:
        response = urllib.request.urlopen(request_info)
        data = response.read()
        return json.loads(data.decode('utf-8'))['message']
    except:
        return 'Cannot check '+source_id+' !'

########################################################################
class LetvUploadAPICannotReachException(Exception):

    '''Deal with LetvUploadAPICannotReach to stop the main() function.'''
    #----------------------------------------------------------------------

    def __init__(self, value):
        self.value = value
    #----------------------------------------------------------------------

    def __str__(self):
        return repr(self.value)

########################################################################
class LetvUploadAPICannotReadException(Exception):

    '''Deal with LetvUploadAPICannotReach to stop the main() function.'''
    #----------------------------------------------------------------------

    def __init__(self, value):
        self.value = value
    #----------------------------------------------------------------------

    def __str__(self):
        return repr(self.value)

########################################################################
class LetvUploadAPIErrorException(Exception):

    '''Deal with LetvUploadAPIError to stop the main() function.'''
    #----------------------------------------------------------------------

    def __init__(self, value):
        self.value = value
    #----------------------------------------------------------------------

    def __str__(self):
        return repr(self.value)

########################################################################
class NotFileException(Exception):

    '''Deal with NotFile to stop the main() function.'''
    #----------------------------------------------------------------------

    def __init__(self, value):
        self.value = value
    #----------------------------------------------------------------------

    def __str__(self):
        return repr(self.value)

#----------------------------------------------------------------------
def upload(file2Upload, proxytype = '', proxy_address = '', curl_args = '', cookies = ''):
    """"""
    #Read Cookie.....Damn it I didn't have my supper!
    #Damn why I still didn't have my supper when I edit it 6 months later!!!!!!!!!
    #Get filename
    filename = file2Upload.split('/')[-1].strip()
    #print(filename)
    if not os.path.isfile(file2Upload):
        raise NotFileException('Not file!')
    #Calculate Filesize
    #Not used to upload extreme large file, may cause problem
    filesize = os.path.getsize(file2Upload)
    #print(filesize)
    #Fetch UploadUrl
    request_full = urllib.request.Request('http://www.acfun.tv/video/createVideo.aspx?type=letv&filesize=100000', headers={ 'User-Agent' : ACUPLOAD_UA, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache' , 'Cookie': cookies,})
    try:
        response = urllib.request.urlopen(request_full)
    except Exception:
        raise LetvUploadAPICannotReachException('Cannot get response from server!')
    data = response.read()
    uploadresponse = json.loads(data.decode('utf-8'))
    if uploadresponse["success"] is 'false':
        logging.error('ERROR: '+ uploadresponse['info'])
        raise LetvUploadAPIErrorException('ERROR: Not success!')
    #print(uploadresponse['upload_url'])
    try:
        #make filename
        remote_name = uploadresponse['sourceId'] + '|' + str(filesize)
        status_url = uploadresponse['progress_url']
        source_id = uploadresponse['sourceId']
        #start upload
        upload_url = str(uploadresponse['upload_url'])
    except KeyError:
        logging.error('Cannot decode this one!')
        raise LetvUploadAPICannotReadException('Cannot decode this one!')
    #print(upload_url)
    print('Upload server IP address: ' + status_url.split('/')[2])
    proxy_args = ''
    if proxytype == 's':
        proxy_args = '--socks5 "{proxy_address}"'.format(proxy_address = proxy_address)
    elif proxytype == 'h':
        proxy_args = '-x "{proxy_address}"'.format(proxy_address = proxy_address)
    curl_cmd = 'curl -A "{ACUPLOAD_UA}" -F "file=@{filename}" {curl_args} {proxy_args} "{upload_url}" | cat #'.format(ACUPLOAD_UA = ACUPLOAD_UA, filename = filename, curl_args = curl_args, proxy_args = proxy_args, upload_url = upload_url)
    #print(curl_cmd)
    #os.system('curl -A \'\'  -F \"file=@'+filename+'\"  \"'+upload_url+'\" | cat #')
    os.system(curl_cmd)
    print('\n' + 'Hope everything is fine. {filename} , {source_id}'.format(filename = filename, source_id = source_id))
    vu_list.append([filename, source_id])

#----------------------------------------------------------------------
def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

#----------------------------------------------------------------------
def usage():
    """"""
    print('''    AcUpload
    
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
        Other arguments you want ot put on curl.''')

#----------------------------------------------------------------------
def read_cookie(cookiepath):
    """str->list
    Original target: set the cookie"""
    try:
        cookies_file = open(cookiepath, 'r')
        cookies = cookies_file.readlines()
        cookies_file.close()
        # print(cookies)
        return cookies
    except:
        logging.warning('Cannot read cookie!')
        return ['']

#----------------------------------------------------------------------
if __name__=='__main__':
    #Test sys encoding
    IS_EXAMINE = 0
    proxytype, proxy_address, curl_args= '', '', ''
    if not sys.getdefaultencoding() is 'utf-8':
        os.system('export LC_ALL="en_US.UTF-8"')
    #Test curl
    proxytype = ''
    if not cmd_exists('curl'):
        logging.fatal('We need curl to upload your file! Get one with apt-get, yum or homebrew.')
        exit()
    argv_list = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv_list, "hec:t:p:a:",
                                   ['help', "examine", 'cookie=', 'proxy-type=', 'proxy-address=', 'curl-args='])
    except getopt.GetoptError:
        usage()
        exit()
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            exit()
        if o in ('-c', '--cookie'):
            cookiepath = a
        if o in ('-e', '--examine'):
            IS_EXAMINE = 1
        if o in ('-t', '--proxy-type'):
            proxytype = a
            print(proxytype)
            if proxytype != 's' and proxytype != 'h':
                logging.warning('Cannot read proxy type, will use no proxy!')
                proxytype = ''
        if o in ('-p', '--proxy-address'):
            proxy_address = a
        if o in ('-a', '--curl-args'):
            curl_args = a
    total_file_num = len(args)
    if total_file_num == 0:
        logging.fatal('No input file to upload!')
        exit()
    try:
        #move here to avoid reading it multiple times
        cookies = open(cookiepath, 'r').readline()
        #print(cookies)
    except:
        logging.fatal('I am hungry, please give me your Cookie!')
        exit()
    i = 0
    for file2Upload in args:
        #print(name)
        i = i + 1
        print('Uploading '+ str(i)+' in '+str(total_file_num)+' files...')
        try:
            upload(file2Upload, proxytype= proxytype, proxy_address= proxy_address, curl_args = curl_args, cookies = cookies)
        except Exception as e:
            print('ERROR: AcUpload failed: %s' % e)
            print('       If you think this should not happen, please open a issue at https://github.com/cnbeining/acupload/issues .')
            print('       Make sure you delete all the sensive data before you post it publicly.')
            traceback.print_exc()
            pass
    #os.system('export LC_ALL="en_US.UTF-8"')
    COOKIE = read_cookie(cookiepath)[0]
    if COOKIE == '':
        logging.error('Cannot get upload URL due to lack of cookie!')
        exit()
    #makes this selectable
    if IS_EXAMINE == 1:
        for media in vu_list:
            try:
                print(media[0] + ',' + media[1] + ','+check_upload(media[1]))
            except Exception as e:
                print('ERROR: AcUpload examination failed: %s' % e)
                print('       If you think this should not happen, please open a issue at https://github.com/cnbeining/acupload/issues .')
                print('       Make sure you delete all the sensive data before you post it publicly.')
                traceback.print_exc()
                pass
