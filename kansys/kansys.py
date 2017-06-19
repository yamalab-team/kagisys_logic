# coding:utf-8

import cv2
import configparser
from slacker import Slacker


class Kansys():
    '''Kansys用クラス'''
    def __init__(self):
        '''セッティング'''
        config = configparser.SafeConfigParser()
        config.read('/home/pi/project/kagisys.conf')
        token = config.get('Slack', 'kansys-url')

        self.channel_id = config.get('Slack', 'channel_id')
        self.channel_name = config.get('Slack', 'channel_name')

        self.slack = Slacker(token)

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
