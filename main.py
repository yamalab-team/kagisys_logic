# -*- coding: utf-8 -*-
from lib import Kagi, Led, OLED_Display, Slack

from auth_nfc.kagisys_nfc import NFC_Reader

def main():
    k = Kagi()
    n = NFC_Reader()
    # led_module = Led()
    # display_module = OLED_Display()
    s = Slack()

    k.attach(s)
    # k.attach(led_module)
    # k.attach(display_module)
    while(True):
        idm = n.recognition()
        # 在室管理に投げる
        if not idm:
            continue
        res = n.authorization(idm=idm)
        if not res:
            # 登録されていないもの
            s.post("未登録のNFCカード：" + idm)
            continue
        (u_name, slack_id) = res
        if k.isOpen:
            k.lock(slackid=slack_id)
        else:
            k.open(slackid=slack_id)


if __name__ == "__main__":
    main()