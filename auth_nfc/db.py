#! /usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import time
import mysql.connector
from pathlib import Path

class DataBase:
	def __init__(self):
		current = Path().resolve()
		print("db", current)
		# get url from kagisys.conf
		self.config = configparser.SafeConfigParser()
		self.config.read(current / "conf/kagisys.config")

	def __open(self):
		try:
			ret = mysql.connector.connect(
				host=self.config.get('SQL','host_name'),
				user=self.config.get('SQL','user_name'),
				password=self.config.get('SQL','user_password'),
				database=self.config.get('SQL','database_name'))
			return ret
		except:
			print('***error*** database can\'t open!')
			exit()

	def checkIDm(self, IDm):
		conn = self.__open()
		cursor = conn.cursor()
		cursor.execute("select * from Nfctags where idm=%s", (IDm,))
		cursor.fetchall()
		if cursor.rowcount == 0:
			cursor.close()
			conn.close()
			return False
		else:
			cursor.close()
			conn.close()
			return True

	def getUsername(self, IDm):
		conn = self.__open()
		cursor = conn.cursor()
		cursor.execute("select userid from Nfctags where idm=%s", (IDm,))
		result = cursor.fetchall()
		cursor.close()
		conn.close()
		return result[0][0]

	def addNewIDm(self, IDm, account_id):
		conn = self.__open()
		cursor = conn.cursor()
		cursor.execute('insert into nfctag VALUES (%s, %s)',(IDm, account_id))
		conn.commit()
		cursor.close()
		conn.close()

	def addTouchedLog(self, IDm):
		now = time.time()
		conn = self.__open()
		cursor = conn.cursor()
		cursor.execute('insert into touchedlog VALUES (%s, %s)',(IDm, now))
		conn.commit()
		cursor.close()
		conn.close()

	def getSlackId(self, userid):
		conn = self.__open()
		cursor = conn.cursor()
		cursor.execute("select slackid from Users where userid=%s", (userid,))
		result = cursor.fetchall()
		cursor.close()
		conn.close()
		return result[0][0]