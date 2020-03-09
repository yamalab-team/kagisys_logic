# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from lib import Kagi, Led, OLED_Display, Slack, Observer
from auth_nfc.kagisys_nfc import NFC_Reader

class Kagisys(Observer):
    _DEFAULT = "defalut"
    _AUTHORIZE = "auhorize"
    _ADDNEWUSER = "addnewuser"
    MODE = __DEFAULT 
    def __init__(self):
        super().__init__()
    
    def migration_to_authorization(self):
        self.MODE = self._AUTHORIZE
        self.notify()
    def migration_to_adduser(self, u_id):
        self.MODE = self._ADDNEWUSER
        self.authorization_uid = u_id
        self.notify()
    def migration_to_default(self):
        self.MODE = self._DEFAULT
        self.authorization_uid = None
        self.notify()

def main():
    while(True):
        idm = n.recognition()
        # 在室管理に投げる
        if not idm:
            continue
        res = n.authorization(idm=idm)
        if kagisys.MODE == kagisys._DEFAULT:
            if not res:
                # 登録されていないもの
                s.post("未登録のNFCカード：" + idm)
                led_module.error()
                continue
            (u_id, u_name) = res
            if k.isOpen:
                k.lock(u_name=u_name)
            else:
                k.open(u_name=u_name)
        elif kagisys.MODE == kagisys._AUTHORIZE:
            # 認証処理
            if not res:
                led_module.error()
                kagisys.migration_to_default()
                continue
            (u_id, u_name) = res
            kagisys.migration_to_adduser(u_id=u_id)
        elif kagisys.MODE == kagisys._ADDNEWUSER:
            # 追加処理
            if not res:
                n.addUser(idm=idm, u_id=kagisys.authorization_uid)
                # TODO: addUserが成功したらに変える
                led_module.success()
            kagisys.migration_to_default()


if __name__ == "__main__":
    k = Kagi()
    kagisys = Kagisys()
    n = NFC_Reader()
    led_module = Led()
    display_module = OLED_Display()
    s = Slack()

    k.attach(s)
    k.attach(led_module)
    kagisys.attach(display_module)

    # GPIO Button Interrupt
    GPIO.setmode(GPIO.BCM)
    B_lock     = 26
    B_open     = 19
    B_register = 20
    GPIO.setup(B_lock, GPIO.IN)
    GPIO.setup(B_open, GPIO.IN)
    GPIO.setup(B_register, GPIO.IN)
    GPIO.add_event_detect(B_lock, GPIO.RISING, callback=k.lock, bouncetime=1000)
    GPIO.add_event_detect(B_open, GPIO.RISING, callback=k.open, bouncetime=1000)
    GPIO.add_event_detect(B_register, GPIO.RISING, callback=kagisys.migration_to_authorization, bouncetime=1000)
    main()