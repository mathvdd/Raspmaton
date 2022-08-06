#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
https://github.com/mathvdd/Raspmaton
'''

from ftplib import FTP
import os

#with open("parameters.txt") as f:
#    param = dict(i.rstrip().split(':') for i in f if i.startswith('#') == False)

def connect():
    with open(os.path.expanduser('~/Raspmaton/parameters.txt')) as f:
        param = dict(i.rstrip().split(':',1) for i in f if i.startswith('#') == False)

    ftp = FTP(param.get('domain'))
    ftp.login(user=param.get('username'), passwd = param.get('password'))
    ftp.cwd(param.get('ftp_www'))
    return ftp

def check_content(ftp_object, subdir):
    # check if the remote directory exists and create it
    #if len(ftp.nlst(param.get('ftp_www'))) == 0:
    #    ftp.mkd(param.get('ftp_www'))
    # go into the directory
    #ftp.cwd(param.get('ftp_www'))
    #ftp.retrlines('LIST')
    return ftp.nlst(subdir)

def upload_content(ftp, subdir):
    remote_list = ftp.nlst(subdir)
    if len(remote_list) == 0:
        ftp.mkd(subdir)
    local_list = os.listdir(os.path.join(os.path.expanduser('~/USBdrive'), subdir))
    for im in local_list:
       if im not in remote_list:
          ftp.storbinary('STOR '+os.path.join(subdir,im), open(os.path.join(os.path.expanduser('~/USBdrive'), subdir, im), 'rb'))

def update_index(ftp, local_dir):
   ftp.storbinary('STOR '+'index.html', open(os.path.join(local_dir,'raspmaton.html'), 'rb'))
   #ftp.storbinary('STOR '+'lazysizes.min.js', open(os.path.join(local_dir,'lazysizes.min.js'), 'rb'))
def disconnect(ftp):
    ftp.quit()

if __name__ == "__main__":
   # filename = 'qr.svg'
   # ftp.storbinary('STOR '+filename, open(filename, 'rb'))
   ftp = connect()
   #remote_filelist = check_content(ftp, 'noname')
   #print(remote_filelist)
   upload_content(ftp, 'noname')
   # update_index(ftp, os.path.expanduser('~/www'))
   disconnect(ftp)
