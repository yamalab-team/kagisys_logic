# -*- coding: utf-8 -*-

"""This program is servo motor contral model."""

import signal
import RPi.GPIO as GPIO
import time


class Servo():
    """This class contral servo motor."""

    def __init__(self):
        """Set gpio and exit handler."""
        # set exit handler
        signal.signal(signal.SIGINT, self.exit_handler)

        # set gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)

    def exit_handler(self):
        """Exit handler."""
        print("Exit motor")
        GPIO.cleanup()

    def open(self):
        """Open servo moter."""
        # contral servo
        servo = GPIO.PWM(12, 50)
        servo.start(11.5)
        time.sleep(0.5)
        servo.stop()

    def lock(self):
        """Lock servo moter."""
        # contral servo
        servo = GPIO.PWM(12, 50)
        servo.start(6.3)
        time.sleep(0.5)
        servo.stop()
