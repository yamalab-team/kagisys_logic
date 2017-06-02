#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import signal
import sys
import nfc
import threading
import os

from config import Config
from db import DataBase


class NFC_Kagisys():
	"""サーボモータの制御"""
	def __init__(self):
		"""基本設定とスレッドの呼び出し"""
		#基本的なセッティング
		config = Config().config
		self.db = DataBase()
		signal.signal(signal.SIGINT, self.exit_handler)
		th = threading.Thread(target=self.run, name="th", args=())
		th.setDaemon(True)
		th.start()

		while True:
			time.sleep(1000)

	def exit_handler(self, signal, frame):
		"""終了時処理"""
		print('Exit nfc')
		self.clf.close()
		sys.exit(0)

	def run(self):
		"""メイン"""
		self.clf = nfc.ContactlessFrontend('tty:AMA0:pn532')

		#繰り返し
		while True:
			self.clf.connect(rdwr={'on-connect': self.touched,'interval': 0.01})
			time.sleep(3)
			print("relese")

	def touched(self,tag):
		"""タッチされたときの処理"""
		#idの照合
		tag_id = tag.identifier.encode("hex").upper()
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

	def get_toggle(self):
		"""toggleデータの取得"""
		os.chdir("/home/pi/project/neo_kagisys/")
		file_ = open("kagisys.toggle")
		result = file_.read()
		file_.close()
		return result


	def write_not_auth_id(self,id):
		"""write not to auth id"""
		write_string = "not authed : " + id

		os.chdir("/home/pi/project/neo_kagisys/")
                file_ = open('not_auth.log', 'a')		
		file_.write(write_string)
		file_.close() 


if __name__ == '__main__':
	NFC_Kagisys()
