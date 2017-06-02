"""This Program Start Kagisys System."""

import threading
import os


def main():
    """Main."""
    # run slack bot
    th_slack = threading.Thread(target=start_slackbot, name="slackbot", args=())
    th_slack.start()

    # run nfc lock
    th_nfc_lock = threading.Thread(target=start_nef_lock, name="nfc_lock", args=())
    th_nfc_lock.start()


def start_slackbot():
    """Start Slackbot."""
    path = "/home/pi/project/neo_kagisys/slackbot/"
    os.chdir(path)
    os.system("sudo python2 slackbot.py")


def start_nef_lock():
    """Start NFC Lock Sysytem."""
    # Move directry
    path = "/home/pi/project/neo_kagisys/nfc_lock/"
    os.chdir(path)
    os.system("sudo python2 nfc_lock.py")


if __name__ == '__main__':
    main()
