# -*- coding: utf-8 -*-
from lib import Kagi, Led, OLED_Display, Slack

from auth_nfc.kagisys_nfc import NFC_Reader

class Kagisys:
    __DEFAULT = "defalut"
    __AUTHORIZE = "auhorize"
    __ADDNEWUSER = "addnewuser"
    MODE = __DEFAULT
    
    def migration_to_authorization(self):
        self.MODE = self.__AUTHORIZE
    def migration_to_adduser(self, u_id):
        self.MODE = self.__ADDNEWUSER
        self.authorization_uid = u_id
    def migration_to_default(self):
        self.MODE = self.__DEFAULT
        self.authorization_uid = None


def main():
    k = Kagi()
    kagisys = Kagisys()
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
        if kagisys.MODE == kagisys.__DEFAULT:
            if not res:
                # 登録されていないもの
                s.post("未登録のNFCカード：" + idm)
                continue
            (u_id, u_name) = res
            if k.isOpen:
                k.lock(u_name=u_name)
            else:
                k.open(u_name=u_name)
        elif kagisys.MODE == kagisys.__AUTHORIZE:
            # 認証処理
            if not res:
                kagisys.migration_to_default()
                continue
            (u_id, u_name) = res
            kagisys.migration_to_adduser(u_id=u_id)
        elif kagisys.MODE == kagisys.__ADDNEWUSER:
            # 追加処理
            if not res:
                n.addUser(idm=idm, u_id=kagisys.authorization_uid)
            kagisys.migration_to_default()


if __name__ == "__main__":
    main()