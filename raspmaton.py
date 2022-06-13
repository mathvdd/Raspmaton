#!/usr/bin/env python3

'''
https://github.com/mathvdd/Raspmaton
'''

import os
import RPi.GPIO as GPIO 
import time
from picamera import PiCamera

## some parameters
path_www = os.path.join(os.path.expanduser('~'), 'www') #path to the www directory
drive_name = 'USBdrive'
path_drive = os.path.join(os.path.expanduser('~'), drive_name)
pin_button = 10 # pin to receive the button input
pin_led = 12 # pin to controle the LEDs

pwm_frequency = 2000 # The PWM frequecy is high to have a nice fading with the loop bellow
feed_out_frequency = pwm_frequency/10

GPIO.setwarnings(False)	# disable warnings
GPIO.setmode(GPIO.BOARD) # set the pin numbering system
GPIO.setup(pin_led,GPIO.OUT) # set pin_led as an output
pi_pwm = GPIO.PWM(pin_led,pwm_frequency) #create PWM instance.

GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin pin_button as input starting in a low state

camera = PiCamera()

## initiating file system

# generates the www dir if not exists and write the config file if not exists
config_path = os.path.join(path_www, 'config.txt')
if not os.path.isdir(path_www):
    os.mkdir(path_www) #creating the www folder
if not os.path.isfile(config_path): # creating the config file if not exists
    with open(config_path, 'w') as f:
        f.write('event_name:noname')
        event_name = 'noname'

#import parameters from the config file generated by config.html      
param = {} # will old the info given in config.txt written by config.html
with open(config_path, 'r') as f: 
    contents = f.readlines()
    for line in contents:
        param[line.split(':')[0]] = line.split(':')[1]

#creates the picture directory for the event
path_pictures = os.path.join(path_drive, param['event_name'])
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
    
    GPIO.wait_for_edge(pin_button, GPIO.FALLING) #wait for the button to be pushed
    # takes the picture with lighting effects
    camera.start_preview() # open the camera in preview mode (need to be open for at least 2sec before taking the picture for luminosity adjustment)
    pi_pwm.start(0)	# start PWM
    for j in range(2): #makes 2 fade cycles before taking the picture, corresponding roughly to 
        for i in range(1,101,1): # gradually light up
            pi_pwm.ChangeDutyCycle(i)
            time.sleep(1/feed_out_frequency)
        for i in range(99,-1,-1):
            pi_pwm.ChangeDutyCycle(i) # fade-out
            time.sleep(1/feed_out_frequency)
    for j in range(2): #makes 2 fade cycles before taking the picture, corresponding roughly to 
        for i in range(1,101,1): # gradually light up
            pi_pwm.ChangeDutyCycle(i)
    time.sleep(1)
    naming_count += 1
    naming_count_str = str(naming_count)
    path_picture = os.path.join(path_pictures, param['event_name'] + '_' + f'{naming_count:04d}' + '.jpg')
    camera.capture(path_picture) #take the picture and save it on the external drive
    time.sleep(0.2)
    pi_pwm.stop()
    
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
          </head>
          <body>
    '''
    foot = '''
                </body>
        </html>
    '''
    content =''
    for filename in sorted(os.listdir(path_pictures), reverse=True):
        if filename.endswith('.jpg'): #just some checks
            path_file = os.path.join(path_pictures, filename)
            try:
                file_count = int(filename[-8:-4])
                content += '''<div class="imgbox">
                    <img class="center-fit" loading="lazy" src='{}'>
                </div>'''.format(drive_name + path_file.split(path_drive)[1])
            except:
                pass
    
    with open(os.path.join(path_www, 'raspmaton.html'), 'w') as f: # write the html page
        f.write(head+content+foot)