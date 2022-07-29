#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
https://github.com/mathvdd/Raspmaton
'''

from ftplib import FTP


with open("parameters.txt") as f:
    param = dict(i.rstrip().split(':') for i in f if i.startswith('#') == False)

def connect():
    ftp = FTP(param.get('domain'))
    ftp.login(user=param.get('username'), passwd = param.get('password'))
    return ftp

def check_content(ftp_object):
    # check if the remote directory exists and create it
    if len(ftp.nlst(param.get('ftp_www'))) == 0:
        ftp.mkd(param.get('ftp_www'))
    # go into the directory
    ftp.cwd(param.get('ftp_www'))
    ftp.retrlines('LIST')
    

# filename = 'qr.svg'
# ftp.storbinary('STOR '+filename, open(filename, 'rb'))
ftp = connect()
check_content(ftp)
ftp.quit()
