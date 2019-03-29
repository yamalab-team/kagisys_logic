# -*- coding: utf-8 -*-

import signal
import RPi.GPIO as GPIO
import time


class LED():
    """This class contral servo motor."""

    def __init__(self):
        """Set gpio and exit handler."""
        # set exit handler
        signal.signal(signal.SIGINT, self.exit_handler)
	self.OPENs = [20, 21]
	self.CLOSEs = [16, 13]
        # set gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.OPENs, GPIO.OUT)
	GPIO.setup(self.CLOSEs, GPIO.OUT)

    def exit_handler(self):
        """Exit handler."""
        GPIO.cleanup()

    def open(self):
        """Open servo moter."""
        # contral servo
        GPIO.output(self.OPENs, 1)
	GPIO.output(self.CLOSEs, 0)

    def lock(self):
        """Lock servo moter."""
        # contral servo
        GPIO.output(self.OPENs, 0)
        GPIO.output(self.CLOSEs, 1)
