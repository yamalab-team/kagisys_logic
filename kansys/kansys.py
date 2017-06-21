# coding:utf-8
import RPi.GPIO as GPIO

import cv2
import configparser
from slacker import Slacker

import time
import os

class Kansys():
    '''Kansys用クラス'''
    def __init__(self):
        '''セッティング'''
        # config
        config = configparser.SafeConfigParser()
        config.read('/home/pi/project/kagisys.conf')

        # gpio
        self.output_pin = config.get('Kansys', 'output-pin')
        self.input_pin = config.get('Kansys', 'input-pin')
	self.output_pin = int(self.output_pin)
	self.input_pin = int(self.input_pin)

        # slack
        token = config.get('Kansys', 'token')
        self.channel = config.get('Kansys', 'channel')

        self.slack = Slacker(token)

    def setup(self):
	'''GPIOイベントのセット'''
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(self.output_pin, GPIO.OUT)
	GPIO.output(self.output_pin,1)

	GPIO.setup(self.input_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(self.input_pin, GPIO.RISING)
	GPIO.add_event_callback(self.input_pin, self.opened_door)

    def opened_door(self, event_gpio):
	'''ドアが空いたときの処理'''
	if(self.get_toggle() == 'lock'):
	    time.sleep(2)
	    self.take_picture()
	    self.send_to_slack()
	    time.sleep(5)

    def send_to_slack(self):
        '''ファイルの送信'''
	os.chdir("/home/pi/project/")
	self.slack.files.upload('photo.jpg',filename="photo.jpg",channels=self.channel)

    def take_picture(self):
        '''写真を取ってファイルの保存'''
	os.chdir("/home/pi/project/")
        camera = cv2.VideoCapture(0)
        r, img = camera.read()
        cv2.imwrite('photo.jpg', img)

    def get_toggle(self):
	'''toggleデータの取得'''
	os.chdir("/home/pi/project/kagisys_logic/")
	file_ = open("kagisys.toggle")
	result = file_.read()
	file_.close()
	return result


if __name__ == '__main__':
    kansys = Kansys()
    kansys.setup()
	
    while True:
	time.sleep(1)	
