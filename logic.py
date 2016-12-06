#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import signal
import sys
import nfc
import threading


class ControlServomotor():
	"""サーボモータの制御"""
	#スレッドの呼び出し--------------------------------------------------------------
	def __init__(self):
		th = threading.Thread(target=self.run, name="th", args=())
    		th.start()


	#メイン-----------------------------------------------------------------------
	def run(self):
		#鍵の番号
		self.key_list = ["0114B405B6116944","01010114DD15E70D"]

		#基本的なセッティング
		signal.signal(signal.SIGINT, self.exit_handler)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(12, GPIO.OUT)
		self.toggle = True

		clf = nfc.ContactlessFrontend('usb')

		print("setting OK.")

		#繰り返し
		while True:
			clf.connect(rdwr={'on-connect': self.touched})
			time.sleep(3)
			print("relese")


	#終了の際の処理---------------------------------------------------------------
	def exit_handler(self,signal, frame):
		print("\nExit")
		GPIO.cleanup()
		sys.exit(0)


	#タッチされたときの処理-----------------------------------------------------------
	def touched(self,tag):
		#idの照合
		tag_id = tag.identifier.encode("hex").upper()
		print(tag_id)
		if tag_id not in self.key_list:
		    #データが正しいidと異なっていた場合
			print("No matching Key")
			return

		servo = GPIO.PWM(12, 50)
		if self.toggle:
	        #鍵の解錠
			servo.start(7.7)
			print("Open")
			time.sleep(0.5)
			self.toggle = False
		else:
	        #鍵の施錠
			servo.start(2.5)
			print("Close")
			time.sleep(0.5)
			self.toggle = True
		servo.stop()


#クラスの呼び出し-------------------------------------------------------------------
ControlServomotor()
