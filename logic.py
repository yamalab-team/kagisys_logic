#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import signal
import sys
import nfc
import threading

from config import Config
from motor import Motor
from db import DataBase


class ControlServomotor():
	"""サーボモータの制御"""
	#スレッドの呼び出し--------------------------------------------------------------
	def __init__(self):
		#基本的なセッティング
		config = Config().config
		self.motor = Motor(config['MOTOR_PIN_NUMBER'])
		self.db = DataBase()
		self.toggle = True

		th = threading.Thread(target=self.run, name="th", args=())
		th.setDaemon(True)
		th.start()

		while True:
			time.sleep(1000)

	#メイン-----------------------------------------------------------------------
	def run(self):

		clf = nfc.ContactlessFrontend('usb')

		print("setting OK.")

		#繰り返し
		while True:
			clf.connect(rdwr={'on-connect': self.touched})
			time.sleep(3)
			print("relese")

	#タッチされたときの処理-----------------------------------------------------------
	def touched(self,tag):
		#idの照合
		tag_id = tag.identifier.encode("hex").upper()
		print(tag_id)
		if self.db.checkIDm(tag_id):
		    #データが正しいidと異なっていた場合
			print("No matching Key")
			return

		if self.toggle:
	        #鍵の解錠
			self.motor.open()
			self.toggle = False
		else:
	        #鍵の施錠
			self.motor.close()
			self.toggle = True


#クラスの呼び出し-------------------------------------------------------------------
ControlServomotor()