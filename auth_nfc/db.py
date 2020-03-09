#! /usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import time
import mysql.connector
# from pathlib import Path

class DataBase:
	def __init__(self):
		# current = Path().resolve()
		print("db", current)
		# get url from kagisys.conf
		self.config = configparser.SafeConfigParser()
		# self.config.read(current / "conf/kagisys.config")
		self.config.read("/home/pi/project/kagisys_logic/conf/kagisys.config")

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

	def getUserId(self, IDm):
		conn = self.__open()
		cursor = conn.cursor()
		cursor.execute("select userid from Nfctags where idm=%s", (IDm,))
		result = cursor.fetchall()
		cursor.close()
		conn.close()
		return result[0][0]

	def addNewIDm(self, IDm, account_id):
		userid = account_id
		idm = IDm
		conn = self.__open()
		cursor = conn.cursor()
		cursor.execute('insert into Nfctags VALUES (%s, %s)',(idm, userid))
		conn.commit()
		cursor.close()
		conn.close()

	def addTouchedLog(self, IDm):
		time_stamp = time.strftime('%Y-%m-%d %H:%M:%S')
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

	def getUserName(self, userid):
		conn = self.__open()
		cursor = conn.cursor()
		cursor.execute("select username from Users where userid=%s", (userid,))
		result = cursor.fetchall()
		cursor.close()
		conn.close()
		return result[0][0]
