#!/usr/bin/env python3

'''
https://github.com/mathvdd/Raspmaton
'''

import RPi.GPIO as GPIO
import time

print('--- Testing the LED strip ---')

pwm_frequency = 1000 # The PWM frequecy is high to have a nice fading with the loop bellow
feed_out_frequency = pwm_frequency/10

GPIO.setwarnings(False)	# disable warnings
pin_led = 12 # pin connected to the transistor base
GPIO.setmode(GPIO.BOARD) # set the pin numbering system
GPIO.setup(pin_led,GPIO.OUT) # set pin_led as an output
pi_pwm = GPIO.PWM(pin_led,pwm_frequency) #create PWM instance. See https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/

pi_pwm.start(0)	# start PWM

print('Starting fading')
print('pwm_frequency =', pwm_frequency, ', feed_out_frequency =', feed_out_frequency)

while True:
    for i in range(1,101,1): # gradually light up
        pi_pwm.ChangeDutyCycle(i)
        time.sleep(1/feed_out_frequency)
    for i in range(99,-1,-1):
        pi_pwm.ChangeDutyCycle(i) # fade-out
        time.sleep(1/feed_out_frequency)