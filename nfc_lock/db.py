#! /usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import yaml
import time
from PyQt4 import QtSql


class DataBase:
	def __init__(self):
		# get url from kagisys.conf
		self.config = configparser.SafeConfigParser()
		self.config.read('/home/pi/project/kagisys.conf')

		self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
		self.db.setHostName(self.config.get('SQL', 'host_name'))
		self.db.setUserName(self.config.get('SQL', 'user_name'))
		self.db.setPassword(self.config.get('SQL', 'user_password'))
		self.db.setDatabaseName(self.config.get('SQL', 'database_name'))

	def __open(self):
		if not self.db.open():
			print('***error*** database can\'t open!')
			exit()

	def checkIDm(self, IDm):
		self.__open()
		query = QtSql.QSqlQuery()
		query.prepare('select COUNT(*) from nfctag where IDm=:IDm')
		query.bindValue(':IDm', IDm)
		query.exec_()
		query.next()
		if query.value(0).toInt()[0] == 0:
			return False
		else:
			return True

	def addNewIDm(self, IDm, account_id):
		self.__open()
		query = QtSql.QSqlQuery()
		query.prepare('insert into nfctag VALUES (:IDm, :account_id)')
		query.bindValue(':IDm', IDm)
		query.bindValue(':account_id', account_id)
		query.exec_()

	def addTouchedLog(self, IDm):
		now = time.time()

		self.__open()
		query = QtSql.QSqlQuery()
		query.prepare('insert into touchedlog VALUES (:IDm, :timestamp)')
		query.bindValue(':IDm', IDm)
		query.bindValue(':timestamp', now)
		query.exec_()
