# -*- coding: utf-8 -*-
import signal
import RPi.GPIO as GPIO
import time

class Led():
	def __init__(self):
		# ledのBCM番号
		self.OPENs = [21]
		self.LOCKs = [13]
		"""Set gpio and exit handler."""
		# set exit handler
		signal.signal(signal.SIGINT, self.exit_handler)
		# set gpio
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.OPENs, GPIO.OUT)
		GPIO.setup(self.LOCKs, GPIO.OUT)

	def exit_handler(self):
		"""Exit handler."""
		GPIO.cleanup()

	def open(self):
		GPIO.output(self.OPENs, 1)
		GPIO.output(self.LOCKs, 0)

	def lock(self):
		GPIO.output(self.OPENs, 0)
		GPIO.output(self.LOCKs, 1)
	
	def off(self):
		GPIO.output(self.OPENs, 0)
		GPIO.output(self.LOCKs, 0)
	
	def update(self, kagi):
		if kagi.isOpen:
			self.open()
		else:
			self.lock()
	
	def error(self):
		isOpen = (GPIO.input(self.OPENs) == 1)
		self.off()
		for i in range(8):
			if(i%2==0):
				GPIO.output(self.LOCKs, 1)
			else:
				GPIO.output(self.LOCKs, 0)
			time.sleep(0.5)
		self.off()
		if isOpen:
			self.open()
		else:
			self.lock()
	
	def success(self):
		isOpen = (GPIO.input(self.OPENs) == 1)
		self.off()
		for i in range(8):
			if(i%2==0):
				GPIO.output(self.OPENs, 1)
			else:
				GPIO.output(self.OPENs, 0)
			time.sleep(0.5)
		self.off()
		if isOpen:
			self.open()
		else:
			self.lock()
