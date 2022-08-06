#!/usr/bin/env python3

'''
https://github.com/mathvdd/Raspmaton
'''

import os
import RPi.GPIO as GPIO 
import time
from picamera import PiCamera
import raspftp
from time import sleep
import urllib.request

## some parameters
path_www = os.path.join(os.path.expanduser('~'), 'www') #path to the www directory
drive_name = 'USBdrive'
path_drive = os.path.join(os.path.expanduser('~'), drive_name)
pin_button = 10 # pin to receive the button input
pin_led = 12 # pin to controle the LEDs
pin_ledb = 16
pin_ledg = 18
pin_ledr = 22

pwm_frequency = 2000 # The PWM frequecy is high to have a nice fading with the loop bellow
feed_out_frequency = pwm_frequency/10

GPIO.setwarnings(False) # disable warnings
GPIO.setmode(GPIO.BOARD) # set the pin numbering system
GPIO.setup(pin_led,GPIO.OUT) # set pin_led as an output
GPIO.setup(pin_ledb,GPIO.OUT)
GPIO.setup(pin_ledg,GPIO.OUT)
GPIO.setup(pin_ledr,GPIO.OUT)
pi_pwm = GPIO.PWM(pin_led,pwm_frequency) #create PWM instance.

GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin pin_button as input starting in a low state

camera = PiCamera()

## blink blue for on
i = 0
while i < 3:
    sleep(0.2)
    GPIO.output(pin_ledb,GPIO.HIGH)
    sleep(0.2)
    GPIO.output(pin_ledb,GPIO.LOW)
    i +=1

## check if the USB drive is connected
if os.path.isfile(os.path.join(path_drive, 'this_is_the_drive')):
    i = 0
    while i < 2:
        sleep(0.2)
        GPIO.output(pin_ledg,GPIO.HIGH)
        GPIO.output(pin_ledb,GPIO.LOW)
        GPIO.output(pin_ledr,GPIO.LOW)
        sleep(0.2)
        GPIO.output(pin_ledg,GPIO.LOW)
        GPIO.output(pin_ledb,GPIO.LOW)
        GPIO.output(pin_ledr,GPIO.LOW)
        i +=1
else:
    while True:
        sleep(0.2)
        GPIO.output(pin_ledr,GPIO.HIGH)
        GPIO.output(pin_ledg,GPIO.LOW)
        GPIO.output(pin_ledb,GPIO.LOW)
        sleep(0.2)
        GPIO.output(pin_ledr,GPIO.LOW)
        GPIO.output(pin_ledg,GPIO.LOW)
        GPIO.output(pin_ledb,GPIO.LOW)

## try to read config changes on remote website at startup
with open(os.path.expanduser('~/Raspmaton/parameters.txt')) as f:
    param = dict(i.rstrip().split(':',1) for i in f if i.startswith('#') == False)
i=0
while i<3:#trys 3 connection 
    i +=1
    sleep(0.5)
    try: # get the parameters from the remote website
        for line in urllib.request.urlopen(os.path.join(param.get('url_www'), 'git_update.conf')):
            gitparam = line.decode('utf-8')
            break
        
        for line in urllib.request.urlopen(os.path.join(param.get('url_www'), 'fold_name.conf')):
            foldparam = line.decode('utf-8')
            break
        GPIO.output(pin_ledg,GPIO.HIGH)
        GPIO.output(pin_ledb,GPIO.HIGH)
        GPIO.output(pin_ledr,GPIO.LOW)
        sleep(0.5)
        GPIO.output(pin_ledg,GPIO.LOW)
        GPIO.output(pin_ledb,GPIO.LOW)
        GPIO.output(pin_ledr,GPIO.LOW)
        break
    except:
        GPIO.output(pin_ledr,GPIO.HIGH)
        GPIO.output(pin_ledb,GPIO.HIGH)
        GPIO.output(pin_ledr,GPIO.LOW)
        sleep(5)
        GPIO.output(pin_ledr,GPIO.LOW)
        GPIO.output(pin_ledb,GPIO.LOW)
        GPIO.output(pin_ledr,GPIO.LOW)
        gitparam = None
        foldparam = None

## initiating local file system
gitparam_path = os.path.join(path_www, 'git_update.conf')
foldparam_path = os.path.join(path_www, 'fold_name.conf')

if not os.path.isdir(path_www): #creating the www folder if not exists
    os.mkdir(path_www) 

# save params as file so can be kept between boots    
if gitparam != None: #replace the param file or create a new one if not exists, load the file in the last case
    with open(gitparam_path , 'w') as f:
        f.write(gitparam)
elif not os.path.isdir(gitparam_path):
    with open(gitparam_path, 'w') as f:
        f.write('Off')
    gitparam = 'Off'
else: # if cannot connect, no use to do the update, set this to off instead?
    with open(gitparam_path, 'r') as f:
        for line in f:
            gitparam = line.rstrip('\n')
            break
if foldparam != None: #replace the param file or create a new one if not exists, load the file in the last case
    with open(foldparam_path, 'w') as f:
        f.write(foldparam)
elif not os.path.isdir(foldparam_path):
    with open(foldparam_path, 'w') as f:
        f.write('noname')
    foldparam = 'noname'
else:
    with open(foldparam_path, 'r') as f:
        for line in f:
            foldparam = line.rstrip('\n')
            break

## Does a gitupdate and reboot if triggered
if gitparam == "On":
    GPIO.output(pin_ledg,GPIO.HIGH)
    GPIO.output(pin_ledb,GPIO.HIGH)
    GPIO.output(pin_ledr,GPIO.HIGH)
    sleep(0.2)  
    try:
        os(f"cd {os.path.expanduser('~/Raspmaton/')} && git pull")
        with open(gitparam_path, 'w') as f:
            f.write('Off')
        i = 0
        while i < 2:
            sleep(0.5)
            GPIO.output(pin_ledg,GPIO.HIGH)
            GPIO.output(pin_ledb,GPIO.LOW)
            GPIO.output(pin_ledr,GPIO.LOW)
            sleep(0.5)
            GPIO.output(pin_ledg,GPIO.LOW)
            GPIO.output(pin_ledb,GPIO.HIGH)
            GPIO.output(pin_ledr,GPIO.LOW)
            sleep(0.5)
            GPIO.output(pin_ledg,GPIO.LOW)
            GPIO.output(pin_ledb,GPIO.LOW)
            GPIO.output(pin_ledr,GPIO.HIGH)
            i +=1
            
    except:
        i = 0
        while i < 2:
            sleep(0.5)
            GPIO.output(pin_ledg,GPIO.HIGH)
            GPIO.output(pin_ledb,GPIO.HIGH)
            GPIO.output(pin_ledr,GPIO.HIGH)
            sleep(0.5)
            GPIO.output(pin_ledg,GPIO.LOW)
            GPIO.output(pin_ledb,GPIO.LOW)
            GPIO.output(pin_ledr,GPIO.LOW)
            i +=1

#creates the picture directory for the event
path_pictures = os.path.join(path_drive, foldparam)
if not os.path.isdir(path_pictures):
    os.mkdir(path_pictures) #creating the www folder

# get the picture count in the folder
naming_count = 0
for filename in os.listdir(path_pictures):
    if filename.endswith('.jpg'): #just some checks
        try:
            file_count = int(filename[-8:-4])
            if int(file_count) > naming_count:
                naming_count = file_count
        except:
            pass

## main loop
t0 = time.time()

while True:
    # generates the website
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
    content =''
    not_lazy = 0 #this is ised for not lazy loadeing the first images in the viewport
    for filename in sorted(os.listdir(path_pictures), reverse=True):
        if filename.endswith('.jpg'): #just some checks
            path_file = os.path.join(path_pictures, filename)
            if not_lazy <3: #load the first 3 images
                try:    
                    file_count = int(filename[-8:-4])
                    content += '''<div class="imgbox">
                        <img class="center-fit" src='{}'>
                    </div>'''.format('.' + path_file.split(path_drive)[1])
                    #</div>''.format(drive_name + path_file.split(path_drive)[1])
                    not_lazy +=1
                except:
                    pass
            else:
                try: # lazy load the other images
                    file_count = int(filename[-8:-4])
                    content += '''<div class="imgbox">
                        <img class="center-fit lazyload" data-src='{}'>
                    </div>'''.format('.' + path_file.split(path_drive)[1])
                    #</div>''.format(drive_name + path_file.split(path_drive)[1])
                except:
                    pass 
    
    with open(os.path.join(path_www, 'raspmaton.html'), 'w') as f: # write the html page
        f.write(head+content+foot)

    # try to connect to remote dir
    try:
        ftp = raspftp.connect()
        raspftp.upload_content(ftp, foldparam)
        raspftp.update_index(ftp, os.path.expanduser('~/www'))
        raspftp.disconnect(ftp)
        #blink green led
        GPIO.output(pin_ledg,GPIO.HIGH)
        GPIO.output(pin_ledr,GPIO.LOW)
        GPIO.output(pin_ledb,GPIO.LOW)
        sleep(0.5)
        GPIO.output(pin_ledg,GPIO.LOW)
        GPIO.output(pin_ledr,GPIO.LOW)
        GPIO.output(pin_ledb,GPIO.LOW)
    except:
        #blink red led
        GPIO.output(pin_ledr,GPIO.HIGH)
        GPIO.output(pin_ledg,GPIO.LOW)
        GPIO.output(pin_ledb,GPIO.LOW)
        sleep(0.5)
        GPIO.output(pin_ledg,GPIO.LOW)
        GPIO.output(pin_ledr,GPIO.LOW)
        GPIO.output(pin_ledb,GPIO.LOW)
    
    # takes the picture event
    
    GPIO.output(pin_ledb,GPIO.HIGH)
    GPIO.output(pin_ledg,GPIO.LOW)
    GPIO.output(pin_ledr,GPIO.LOW)
    GPIO.wait_for_edge(pin_button, GPIO.FALLING) #wait for the button to be pushed
    camera.start_preview() # open the camera in preview mode (need to be open for at least 2sec before taking the picture for luminosity adjustment)
    pi_pwm.start(0)     # start PWM
    for j in range(2): #makes 2 fade cycles before taking the picture, corresponding roughly to 
        for i in range(1,101,1): # gradually light up
            pi_pwm.ChangeDutyCycle(i)
            time.sleep(1/feed_out_frequency)
        for i in range(99,-1,-1):
            pi_pwm.ChangeDutyCycle(i) # fade-out
            time.sleep(1/feed_out_frequency)
    for j in range(2): #light up one last time before the picture
        for i in range(1,101,1): # gradually light up
            pi_pwm.ChangeDutyCycle(i)
    time.sleep(1)
    naming_count += 1
    naming_count_str = str(naming_count)
    path_picture = os.path.join(path_pictures, foldparam + '_' + f'{naming_count:04d}' + '.jpg')
    #print('took picture', param['event_name'] + '_' + f'{naming_count:04d}' + '.jpg')
    camera.capture(path_picture) #take the picture and save it on the external drive
    time.sleep(0.2)
    pi_pwm.stop()
