#!/usr/bin/env python3

'''
https://github.com/mathvdd/Raspmaton
'''

from picamera import PiCamera
import time
import os

export_path = os.path.join(os.path.expanduser('~'), 'test_camera.jpg')
print('--- Testing the Pi Camera ---')
camera = PiCamera()
print('starting the previex mode')
camera.start_preview()
print('waiting 2 secondes for light adjustment')
time.sleep(2)
print('taking the picture')
camera.capture(export_path)
print('Picture saved as ', export_path)
