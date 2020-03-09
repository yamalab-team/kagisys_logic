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
        config.read(str(current / "conf/kagisys.config"))
        self.url = config.get("Slack", "url")

    def update(self, kagi):
        msg = ""
        if type(kagi.currentName) == str:
            # msg = f"<@{kagi.currentSlackId}>が"
            msg = kagi.currentName + "が"
        if kagi.isOpen:
            msg += "開けました"
            self.post(msg)
        else:
            msg += "閉めました"
            self.post(msg)
    
    def post(self, msg):
        res = requests.post(
            self.url,
            data=json.dumps({
                "text": u"7505:" + msg,
                "username": u"kagisys"
            })
        )
