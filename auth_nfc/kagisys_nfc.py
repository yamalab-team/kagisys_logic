import nfc
import sys
import signal
import binascii

from .db import DataBase

class NFC_Reader:
    def __init__(self):
        self.db = DataBase()
        self.clf = nfc.ContactlessFrontend("tty:AMA0:pn532")
        # self.clf = nfc.ContactlessFrontend("usb")
        self.target_req = nfc.clf.RemoteTarget("212F") # NFC Type:Felica
        self.target_req.sensf_req = bytearray.fromhex("0000030000")
        signal.signal(signal.SIGINT, self.exit_handler)
    
    def exit_handler(self, signal, frame):
		"""終了時処理"""
		print('Exit nfc')
		self.clf.close()
		sys.exit(0)
        
    def recognition(self):
        target_res = self.clf.sense(self.target_req, iterations=10, interval=0.1)
        if not target_res:
            return None
        tag = nfc.tag.activate(self.clf,target_res)
        tag.sys = 3
        idm_byte = binascii.hexlify(tag.idm)
        idm = idm_byte.decode("utf-8")
        self.db.addTouchedLog(idm)
        print(idm)
        return idm

    def authorization(self, idm):
        # db check idm
        if self.db.checkIDm(idm):
            u_id = self.db.getUserId(idm)
            return (u_id, self.db.getUserName(userid=u_id))
        else:
            return False
    
    def addUser(self, idm, u_id):
        self.db.addNewIDm(IDm=idm, account_id=u_id)