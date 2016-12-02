#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import signal
import sys
import nfc

key_list = ["0114B405B6116944","01010114DD15E70D"]

def exit_handler(signal, frame):
	print("\nExit")
	GPIO.cleanup()
	sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
toggle = True

def touched(tag):
	global toggle
	global key_list
	tag_id = tag.identifier.encode("hex").upper()
	print(tag_id)
	if tag_id not in key_list:
		print("No matching Key")
		return

	servo = GPIO.PWM(12, 50)
	if toggle:
		servo.start(7.7)		
		print("Open")
		time.sleep(0.5)
		toggle = False
	else:
		servo.start(2.5)
		print("Close")
		time.sleep(0.5)
		toggle = True
	servo.stop()

clf = nfc.ContactlessFrontend('usb')

print("setting OK.")
while True:
	clf.connect(rdwr={'on-connect': touched})
	time.sleep(3)
	print("relese")	

	

