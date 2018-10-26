#!/usr/bin/python

import os
import urllib3
from urllib3 import PoolManager
from urllib.parse import urlparse
from ftplib import FTP
import shutil
from datetime import date

#DEFINE SUPPORTING FUNCTIONS
def getDateFromFirstLineOfDataFile_YYYYMMDD(file_name):
        _f = open(file_name, 'r')
        _line = _f.readline()
        _f.close()
        _fields = _line.split(' ')
        i = 0
        while i < len(_fields):
                if _fields[i] == 'AS' and _fields[i+1] == 'OF':
                        dateString = _fields[i+2]
                        _parts = dateString.split('/')
                        return '20' + _parts[2] + _parts[0] + _parts[1]
                i += 1
        #OTHERWISE
        return "ERRRRROR"

#DELETE TEMP DIRECTORY IF IT EXISTS
temp_dir = '../settlement_data_files/temp'
if os.path.exists(temp_dir): shutil.rmtree(temp_dir)

#RECREATE TEMP DIRECTORY
os.mkdir(temp_dir)

# READ URL LIST FROM CONFIG FILE
urlFile = '../config/url_list.txt'
block_sz = 8192
f = open(urlFile, 'r')
url_list = f.readlines()
f.close()

#DOWNLOAD EACH OF THE FILES TO THE TEMP DIRECTORY
for url in url_list:
    url = url.strip().split(',')[0]
    file_name = url.split('/')[-1]
    url_obj = urlparse(url)
    host  = url_obj.netloc
    path = url_obj.path

    #print ('Downloading ' + url)
    print (path)
    ftp = FTP()
    port = 21
    ftp.connect(host, port)
    ftp.login('anonymous','')


    ftp.retrbinary("RETR " + path ,open(temp_dir + '/' + file_name, 'wb').write)
    # f = open(file_name, 'wb')
    # while 1:
    #     buffer = u.read(block_sz)
    #     if not buffer:
    #         break
    #     f.write(buffer)
    # f.close()

#RENAME TEMP DIRECTORY BASED ON FIRST DATA FILE
url = url_list[0].strip().split(',')[0]
file_name = temp_dir + '/' + url.split('/')[-1]
newPath = '../settlement_data_files/' + getDateFromFirstLineOfDataFile_YYYYMMDD(file_name)
if os.path.exists(newPath): shutil.rmtree(newPath)
os.rename(temp_dir,newPath)
