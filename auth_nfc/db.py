#! /usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import yaml
import time
import MySQLdb


class DataBase:
	def __init__(self):
		# get url from kagisys.conf
		self.config = configparser.SafeConfigParser()
		self.config.read('/home/pi/project/kagisys_logic/kagisys.conf')
		url = self.config.get('Slack', 'url')

	def __open(self):
		try:
			ret = MySQLdb.connect(host=self.config.get('SQL','host_name'),
					user=self.config.get('SQL','user_name'),
					passwd=self.config.get('SQL','user_password'),
					db=self.config.get('SQL','database_name'))
			return ret
		except:
			print('***error*** database can\'t open!')
			exit()

	def checkIDm(self, IDm):
		conn = self.__open()
		cursor = conn.cursor()
		cursor.execute("select * from nfctag where IDm=%s", (IDm,))
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
		cursor.execute("select * from nfctag where IDm=%s", (IDm,))
		result = cursor.fetchall()
		cursor.close()
		conn.close()
		print(result)
		return result[0][1]

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
