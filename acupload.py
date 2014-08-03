#!/usr/bin/env python3
#coding:utf-8
# Author:  Beining --<ACICFG>
# Purpose:  Upload to Letv via Acfun's API
# Created: 07/17/2014

#python3 acup.py 0.flv 1.flv

import urllib.request
import sys
import os
import json
import subprocess
import hashlib

global cookiepath
cookiepath = './accookies'
global vu_list
vu_list = []

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


#----------------------------------------------------------------------
def upload(file2Upload):
    """"""
    #Read Cookie.....Damn it I didn't have my supper!
    try:
        cookies = open(cookiepath, 'r').readline()
        #print(cookies)
    except:
        print('I am hungry, please give me your Cookie!')
        exit()
    #Get filename
    filename = file2Upload.split('/')[-1].strip()
    #print(filename)
    if not os.path.isfile(file2Upload):
        print('Not file!')
        pass
    #Calculate Filesize
    #Not used to upload extreme large file, may cause problem
    #filesize = os.path.getsize(file2Upload)
    #print(filesize)
    #Fetch UploadUrl
    request_full = urllib.request.Request('http://www.acfun.tv/video/createVideo.aspx?type=letv&filesize=100000', headers={ 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', 'Cache-Control': 'no-cache', 'Pragma': 'no-cache' , 'Cookie': cookies,})
    try:
        response = urllib.request.urlopen(request_full)
    except:
        print('Cannot get response from server!')
        pass
    data = response.read()
    uploadresponse = json.loads(data.decode('utf-8'))
    if uploadresponse["success"] is 'false':
        print('ERROR: '+ uploadresponse['info'])
        exit()
    #print(uploadresponse['upload_url'])
    #make filename
    remote_name = uploadresponse['sourceId'] + '|' + str(filesize)
    status_url = uploadresponse['progress_url']
    source_id = uploadresponse['sourceId']
    #start upload
    upload_url = str(uploadresponse['upload_url'])
    #print(upload_url)
    os.system('curl   -F \"file=@'+filename+'\"  \"'+upload_url+'\" | cat #')
    print('\n'+'Hope everything is fine. '+source_id)
    vu_list.append([filename, source_id])

#----------------------------------------------------------------------
def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

#----------------------------------------------------------------------
if __name__=='__main__':
    #Test sys encoding
    if not sys.getdefaultencoding() is 'utf-8':
        os.system('export LC_ALL="en_US.UTF-8"')
    #Test curl
    if not cmd_exists('curl'):
        print ('We need curl to upload your file! Get one with apt-get or yum.')
        exit()

    total_file_num = len(sys.argv[1:])
    i = 0
    for name in sys.argv[1:]:
        #print(name)
        i = i + 1
        print('Uploading '+ str(i)+' in '+str(total_file_num)+' files...')
        upload(name)
    #os.system('export LC_ALL="en_US.UTF-8"')
    for media in vu_list:
        print(media[0] + ',' + media[1] + ','+check_upload(media[1]))
