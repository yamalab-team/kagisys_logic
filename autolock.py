"""Kagisys Autolock.

This program lock kagisys key automaticaly
"""

import RPi.GPIO as GPIO
import time


class AutoLock():
    """AutoLock for Kagisys."""

    def __init__(self):
        """Run."""
        # propaty
        self.RelayPIN = 21

        door_open_bool = {
            "before": False,
            "after": False
        }

        # main loop
        while True:
            time.sleep(0.2)

            # check door twice
            door_open_bool["before"] = self.check_open()
            door_open_bool["after"] = self.check_open()

            if door_open_bool["before"] and door_open_bool["after"]:
                print "auto lock"

    def check_open(self):
        """Check open the door."""
        # check gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RelayPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        result = GPIO.input(self.RelayPIN)

        # return bool
        if result == 1:
            return False
        else:
            return True


if __name__ == '__main__':
    AutoLock()

