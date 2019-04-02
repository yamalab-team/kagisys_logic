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
from oled import OLED_Display


class NFC_Kagisys():
	"""サーボモータの制御"""
	def __init__(self):
		self.BUTTON_ON=19
		self.BUTTON_OFF=26
		self.BUTTON_SET=21
		self.MODE = "Default"
		"""基本設定とスレッドの呼び出し"""
		#基本的なセッティング
		self.db = DataBase()
		self.oled = OLED_Display()
		self.oled.display([self.MODE], ["en"])
		signal.signal(signal.SIGINT, self.exit_handler)
		th = threading.Thread(target=self.run, name="th", args=())
		th.setDaemon(True)
		th.start()
		GPIO.setmode(GPIO.BCM)
		self.errLED = [16]
		GPIO.setup(self.errLED, GPIO.OUT)
		GPIO.setup(self.BUTTON_ON, GPIO.IN)
		GPIO.setup(self.BUTTON_OFF, GPIO.IN)
		GPIO.setup(self.BUTTON_SET, GPIO.IN)
		GPIO.add_event_detect(self.BUTTON_ON, GPIO.RISING, callback=self.pushed_on, bouncetime=3000)
		GPIO.add_event_detect(self.BUTTON_OFF, GPIO.RISING, callback=self.pushed_off, bouncetime=3000)
		GPIO.add_event_detect(self.BUTTON_SET, GPIO.RISING, callback=self.pushed_register, bouncetime=3000)

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
		# toggleの受け取り
                toggle = self.get_toggle()

		if self.MODE == "Default":
			if not self.db.checkIDm(tag_id):
				#データが正しいidと異なっていた場合
				self.write_not_auth_id(tag_id)
				self.led(toggle)
				self.oled.display([self.MODE, tag_id], ["en", "ja"])
				print("No matching Key")
				print("setting OK.")
				return
			if toggle == "lock":
				#鍵の解錠
				os.system("open_kagi")
				self.oled.display([self.MODE, "OPEN"], ["en", "en"])
			elif toggle == "open":
				#鍵の施錠
				os.system("lock_kagi")
				self.oled.display([self.MODE, "LOCK"], ["en", "en"])
			else:
				print("error ! please check file path")
		elif self.MODE == "Register":
			if self.db.checkIDm(tag_id):
				self.MODE = "Authorization"
				self.oled.display([self.MODE, "登録するカードをタッチ"], ["en", "ja"])
			else:
				self.MODE = "Default"
				self.oled.display([self.MODE, "登録失敗"], ["en", "ja"])
		elif self.MODE == "Authorization":
			if not self.db.checkIDm(tag_id):
				self.MODE = "Default"
				self.db.addNewIDm(tag_id, "TestUser")
				self.oled.display([self.MODE, "登録成功"], ["en", "ja"])
			else:
				self.MODE = "Default"
				self.oled.display([self.MODE, "登録失敗"], ["en", "ja"])

	def pushed_on(self, sw):
		print("bbbbbbbb")
		toggle = self.get_toggle()
		if toggle == "lock":
			#鍵の解錠
			os.system("open_kagi")
			self.oled.display([self.MODE, "OPEN"], ["en", "en"])
		elif toggle == "open":
			os.system("lock_kagi")
			self.oled.display([self.MODE, "LOCK"], ["en", "en"])

	def pushed_off(self, sw):
		print("aaaaaaaaaa")
		toggle = self.get_toggle()
		if toggle == "open":
			#鍵の施錠
			os.system("lock_kagi")
			self.oled.display([self.MODE, "LOCK"], ["en", "en"])

	def pushed_register(self, sw):
		self.MODE = "Register"
		self.oled.display([self.MODE, "登録済みカードをタッチ"], ["en", "ja"])

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

	def led(self, toggle):
		for i in range(8):
			if(i%2==0):
				GPIO.output(self.errLED, 0)
			else:
				GPIO.output(self.errLED, 1)
			time.sleep(0.5)
		if toggle == "lock":
			GPIO.output(self.errLED, 1)
		else:
			GPIO.output(self.errLED, 0)

if __name__ == '__main__':
	NFC_Kagisys()
