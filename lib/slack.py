# -*- coding: utf-8 -*-
import requests
import json
import configparser
from pathlib import Path

class Slack:
    def __init__(self):
        current = Path().resolve()
        print("slack", current)
        config = configparser.SafeConfigParser()
        # config.read('')
        self.url = "incomming messageのurl"

    def update(self, kagi):
        if kagi.isOpen:
            msg = "開くました"
            self.post(msg)
        else:
            msg = "閉めました"
            self.post(msg)
        print("Kagi -> ", kagi.isOpen)
    
    def post(self, msg):
        res = requests.post(
            self.url,
            data=json.dumps({
                "text": u"7505:" + msg,
                "username": u"kagisys"
            })
        )
        print("slack posted\n", res.text)
