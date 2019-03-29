#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import signal
import sys
import nfc
import threading
import os
import binascii

from db import DataBase


class NFC_Kagisys():
	"""サーボモータの制御"""
	def __init__(self):
		self.BUTTON_ON=19
		self.BUTTON_OFF=26
		"""基本設定とスレッドの呼び出し"""
		#基本的なセッティング
		self.db = DataBase()
		signal.signal(signal.SIGINT, self.exit_handler)
		th = threading.Thread(target=self.run, name="th", args=())
		th.setDaemon(True)
		th.start()
		GPIO.setmode(GPIO.BCM)
		#GPIO.setup(self.BUTTON_ON, GPIO.IN)
		#GPIO.setup(self.BUTTON_OFF, GPIO.IN)
		#GPIO.add_event_detect(self.BUTTON_ON, GPIO.FALLING, callback=self.pushed_on, bouncetime=3000)
		#GPIO.add_event_detect(self.BUTTON_OFF, GPIO.FALLING, callback=self.pushed_off, bouncetime=3000)

		while True:
			time.sleep(1000)

	def exit_handler(self, signal, frame):
		"""終了時処理"""
		print('Exit nfc')
		self.clf.close()
		GPIO.cleanup()
		sys.exit(0)

	def run(self):
		"""メイン"""
		self.clf = nfc.ContactlessFrontend('tty:AMA0:pn532')
		#繰り返し
		while True:
			target_req = nfc.clf.RemoteTarget("212F")
	                target_req.sensf_req = bytearray.fromhex("0000030000")
			target_res = self.clf.sense(target_req,iterations=10,interval=0.1)
                	if target_res != None:
                    		tag = nfc.tag.activate(self.clf,target_res)
                    		tag.sys = 3
				idm = binascii.hexlify(tag.idm)
                    		self.touched(idm)
				time.sleep(3)
				print("relese")
			else:
				time.sleep(1)

	def touched(self,tag):
		"""タッチされたときの処理"""
		#idの照合
		#tag_id = tag.identifier.encode("hex").upper()
		tag_id=tag
		print(tag_id)
		self.db.addTouchedLog(tag_id)
		if not self.db.checkIDm(tag_id):
			#データが正しいidと異なっていた場合
			self.write_not_auth_id(tag_id)

			print("No matching Key")
			print("setting OK.")
			return

		# toggleの受け取り
		toggle = self.get_toggle()

		if toggle == "lock":
			#鍵の解錠
			os.system("open_kagi")
		elif toggle == "open":
			#鍵の施錠
			os.system("lock_kagi")
		else:
			print "error ! please check file path"

	def pushed_on(self, sw):
		print("bbbbbbbb")
		toggle = self.get_toggle()
		if toggle == "lock":
                        #鍵の解錠
                        os.system("open_kagi")
		elif toggle == "open":
			os.system("lock_kagi")

	def pushed_off(self, sw):
		print("aaaaaaaaaa")
		toggle = self.get_toggle()
                if toggle == "open":
                        #鍵の施錠
                        os.system("lock_kagi")

	def get_toggle(self):
		"""toggleデータの取得"""
		os.chdir("/home/pi/project/kagisys_logic/")
		file_ = open("kagisys.toggle")
		result = file_.read()
		file_.close()
		print(result)
		return result


	def write_not_auth_id(self,id):
		"""write not to auth id"""
		write_string = "not authed : " + id

		os.chdir("/home/pi/project/kagisys_logic/")
                file_ = open('not_auth.log', 'a')		
		file_.write(write_string)
		file_.close() 


if __name__ == '__main__':
	NFC_Kagisys()
