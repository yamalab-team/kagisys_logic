# -*- coding: utf-8 -*-
from .servo import Servo

class Observer:
	def __init__(self):
		self._observers = []
	
	def attach(self, observer):
		if not observer in self._observers:
			self._observers.append(observer)
	
	def detach(self, observer):
		try:
			self._observers.remove(observer)
		except:
			pass

	def notify(self):
		for ob in self._observers:
			ob.update(self)

class Kagi(Observer):
	def __init__(self):
		super().__init__()
		self.isOpen = False
		self.currentSlackId = None
		# 鍵の状態が変わったときに通知する
		self.attach(Servo())

	def open(self, slackid=None):
		if self.isOpen:
			return
		self.currentSlackId = slackid
		self.isOpen = True
		self.notify()
		
	
	def lock(self, slackid=None):
		if not self.isOpen:
			return
		self.currentSlackId = slackid
		self.isOpen = False
		self.notify()

if __name__ == "__main__":
	k = Kagi()
	k.open()
	k.close()