#!/usr/bin/env python3

'''
https://github.com/mathvdd/Raspmaton
'''

import RPi.GPIO as GPIO 
import time

button_pin = 10
time_between_pushes = 0.2 #set a time between the pushed in seconds so the input is not triggered multiple times for a push

print('--- Testing the button ---')
t0 = time.time()

GPIO.setwarnings(False)	# disable warnings
GPIO.setmode(GPIO.BOARD) # set the pin numbering system
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 as input with pull up 
# GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 as input with pull down

while True:
    # if GPIO.input(button_pin) == GPIO.HIGH: #if the button is pushed
    if GPIO.input(button_pin) == GPIO.LOW: #if the button is pushed
        print("Button pushed at t0 +", round(time.time() -t0,2), 'seconds')
        time.sleep(time_between_pushes)
