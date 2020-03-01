import nfc
import binascii

from .db import DataBase

class NFC_Reader:
    def __init__(self):
        self.db = DataBase()
        # self.clf = nfc.ContactlessFrontend("tty:AMA0:pn532")
        self.clf = nfc.ContactlessFrontend("usb")
        self.target_req = nfc.clf.RemoteTarget("212F") # NFC Type:Felica
        self.target_req.sensf_req = bytearray.fromhex("0000030000")
        
    def recognition(self):
        target_res = self.clf.sense(self.target_req, iterations=10, interval=0.1)
        if not target_res:
            return None
        tag = nfc.tag.activate(self.clf,target_res)
        tag.sys = 3
        idm = binascii.hexlify(tag.idm)
        print(idm.decode("utf-8"))
        return self.authorization(idm)

    def authorization(self, idm):
        # db check idm
        if self.db.checkIDm(idm):
            uname = self.db.getUsername(idm)
            return (uname, self.db.getSlackId(uname))
        else:
            return False