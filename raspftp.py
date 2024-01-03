#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
https://github.com/mathvdd/Raspmaton
'''

from ftplib import FTP
import os
#from raspmaton import import_params

def import_params():
    with open(os.path.expanduser('parameters.txt')) as f:
        param = {i.rstrip().split(':',1)[0]:os.path.expanduser(i.rstrip().split(':',1)[1]) for i in f if i.startswith('#') == False}
    return param

def set_FTPstatus(status):
    with open(param.get('path_FTP_status'), 'w') as file:
        file.write(status)

def connect(timeout=None):

    ftp = FTP(host=param.get('domain'), user=param.get('username'), passwd=param.get('password'), timeout=timeout)
    # ftp = FTP(param.get('domain'))
    # ftp.login(user=param.get('username'), passwd = param.get('password'))
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
def update_git_update(ftp, local_dir):
   ftp.storbinary('STOR '+'git_update.conf', open(os.path.join(local_dir,'git_update.conf'), 'rb'))

def disconnect(ftp):
    ftp.quit()


#if __name__ == "__main__":
   # filename = 'qr.svg'
   # ftp.storbinary('STOR '+filename, open(filename, 'rb'))
#   ftp = connect()
#   remote_filelist = check_content(ftp, 'test')
#   print(remote_filelist)
   #upload_content(ftp, 'noname')
   # update_index(ftp, os.path.expanduser('~/www'))
#   disconnect(ftp)

if __name__ == "__main__":
    import time
    min_refresh_rate = 1 #in seconds

    param = import_params()
    head = '''
    <!DOCTYPE html>
        <html>
          <head>
            <title>
              Raspmaton gallery
            </title>
            <style>
              * {
                  margin: 0;
                  padding: 0;
                  margin-bottom: 1vh;
              }
              .imgbox {
                  display: grid;
                  height: 100%;
              }
              .center-fit {
                  max-width: 100%;
                  margin: auto;
              }
            </style>
            <script src="lazysizes.min.js" async=""></script>
          </head>
          <body>
    '''
    foot = '''
                </body>
        </html>
    '''

    set_FTPstatus('Wait')
    #wait for the raspmaton script to be started
    time.sleep(5)
    #have to wait for the status to be first change since it is "ready" when booted
    while True:
        tnow = time.time()
        with open(os.path.join(os.path.expanduser('~'), 'Raspmaton', 'status'), 'r') as file:
            status = file.read().rstrip('\n')
        if status == 'Ready!':
            break
        else:
            try:
                time.sleep(0.1 - ((time.time() - tnow)))
            except:
                pass

    set_FTPstatus('1st connect')
    #get folder name that was setup by raspmaton.py
    foldparam_path = os.path.join(param['path_www'], 'fold_name.conf')
    with open(foldparam_path, 'r') as f:
        foldname = f.rstrip('\n')

    # start with a first check and look what is on the server
    try:
        ftp = connect()
        remote_files = check_content(ftp, foldname)
        if len(remote_files) == 0:
            ftp.mkd(foldname)
        disconnect(ftp)
        #blink green led
        #led(blue=False,green=True,red=False)
        sleep(0.5)
        #led(blue=False,green=False,red=False)
    except:
        #blink red led
        set_FTPstatus('Error')
        remote_files = []
        #led(blue=False,green=False,red=True)
        sleep(0.5)
        #led(blue=False,green=False,red=False)

    while True:
        tnow = time.time()

        #check if the server is up to date
        set_FTPstatus('Checking')
        local_files_path = os.path.join(param.get('path_drive'), foldname)
        local_files = os.listdir(local_files_path)
        diff = set(local_files) - set(remote_files)

        if len(diff) > 0:
            # generates the website
            set_FTPstatus('Generate website')
            content =''
            not_lazy = 0 #this is ised for not lazy loadeing the first images in the viewport
            for filename in sorted(local_files, reverse=True):
                if filename.endswith('.jpg'): #just some checks
                    path_file = os.path.join(local_files_path, filename)
                    if not_lazy <3: #load the first 3 images
                        try:
                            file_count = int(filename[-8:-4])
                            content += '''<div class="imgbox">
                                <img class="center-fit" src='{}'>
                            </div>'''.format('.' + path_file.split(param.get('path_drive'))[1])
                            #</div>''.format(drive_name + path_file.split(path_drive)[1])
                            not_lazy +=1
                        except:
                            pass
                    else:
                        try: # lazy load the other images
                            file_count = int(filename[-8:-4])
                            content += '''<div class="imgbox">
                                <img class="center-fit lazyload" data-src='{}'>
                            </div>'''.format('.' + path_file.split(param.get('path_drive'))[1])
                            #</div>''.format(drive_name + path_file.split(path_drive)[1])
                        except:
                            pass
            #write the index page
            with open(os.path.join(param['path_www'], 'raspmaton.html'), 'w') as f: # write the html page
                f.write(head+content+foot)

            #upload
            try:
                set_FTPstatus('Uploading')
                ftp = connect()
                if len(remote_files) == 0:
                    ftp.mkd(foldname)
                raspftp.update_index(ftp, param.get('path_www'))
                for im in sorted(diff):
                    ftp.storbinary('STOR '+os.path.join(foldname,im), open(os.path.join(param.get('path_drive'), foldname, im), 'rb'))
                remote_files = check_content(ftp, foldname)
                disconnect(ftp)
                set_FTPstatus('Wait')

            except:
                #blink red led
                set_FTPstatus('Error')
                #led(blue=False,green=False,red=True)
                sleep(0.5)
                #led(blue=False,green=False,red=False)
        else:
            set_FTPstatus('Wait')

        try:
            tempime.sleep(min_refresh_rate - ((time.time() - tnow)))
        except:
            pass
