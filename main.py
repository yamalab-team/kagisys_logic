# -*- coding: utf-8 -*-
from lib import Kagi, Led, OLED_Display, Slack

from auth_nfc.kagisys_nfc import NFC_Reader

def main():
    k = Kagi()
    n = NFC_Reader()
    led_module = Led()
    display_module = OLED_Display()

    k.attach(Slack())
    k.attach(led_module)
    k.attach(display_module)
    while(True):
        user_id = n.recognition()
        # 在室管理に投げる
        if not user_id:
            continue
        if k.isOpen:
            k.lock()
        else:
            k.open()


if __name__ == "__main__":
    main()