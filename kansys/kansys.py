# coding:utf-8
import RPi.GPIO as GPIO

import cv2
import configparser
from slacker import Slacker

import time


class Kansys():
    '''Kansys用クラス'''
    def __init__(self):
        '''セッティング'''
        # config
        config = configparser.SafeConfigParser()
        config.read('/home/pi/project/kagisys.conf')

        # gpio
        self.pin = config.get('Kansys', 'gpio-pin')
        GPIO.setup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

        # slack
        token = config.get('Kansys', 'slack-url')
        self.channel_id = config.get('Kansys', 'channel_id')
        self.channel_name = config.get('Kansys', 'channel_name')

        self.slack = Slacker(token)

    def run(self):
        while True:
            status = GPIO.input(self.pin)
            if(status):
                time.sleep(1)
                self.take_picture()
                self.send_to_slack()

    def send_to_slack(self):
        '''ファイルの送信＆ピン止め'''
        result = self.slack.files.upload(
            './picture.jpg',
            channels=[self.channel_id]
        )
        self.slack.pins.add(
            channel=self.channel_id,
            file_=result.body['file']['id']
        )

    def take_picture():
        '''写真を取ってファイルの保存'''
        camera = cv2.VideoCapture(0)
        r, img = camera.read()
        cv2.imwrite('picture.jpg', img)
