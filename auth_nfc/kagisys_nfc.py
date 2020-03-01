import nfc
import binascii

from .db import DataBase

class NFC_Reader:
    def __init__(self):
        self.db = DataBase()
        self.clf = nfc.ContactlessFrontend("tty:AMA0:pn532")
        self.target_req = nfc.clf.RemoteTarget("212F") # NFC Type:Felica
        self.target_req.sensf_req = bytearray.fromhex("0000030000")
        
    def recognition(self):
        target_res = self.clf.sense(self.target_req, iterations=10, interval=0.1)
        if target_res == None:
            return None
        tag = nfc.tag.activate(self.clf,target_res)
        tag.sys = 3
        idm = binascii.hexlify(tag.idm)
        return self.authorization(idm)

    def authorization(self, idm):
        # db check idm
        if self.db.checkIDm(idm):
            return self.db.getUsername(idm)
        else:
            return False