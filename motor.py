#!/usr/bin/python
# -*- coding: utf-8 -*-

import signal
import time
import sys
import RPi.GPIO as GPIO

class Motor:
	def __init__(self, PIN_number):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(PIN_number, GPIO.OUT)

	def exit_handler(self):
		print("Exit motor")
		GPIO.cleanup()

	def open(self):
			servo = GPIO.PWM(12, 50)
				servo.start(7.7)
				time.sleep(0.5)
				toggle = False
		servo.stop()

	def close(self):
		servo = GPIO.PWM(12, 50)
		servo.start(2.5)
		time.sleep(0.5)
		servo.stop()

