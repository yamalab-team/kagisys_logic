#! /usr/bin/python
# -*- coding: utf-8 -*-

import yaml
from PyQt4 import QtSql

from config import Config

class DataBase:
	def __init__(self):
		self.config = Config().config

		self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
		self.db.setHostName(self.config['SQL_HOST_NAME'])
		self.db.setUserName(self.config['SQL_USER_NAME'])
		self.db.setPassword(self.config['SQL_USER_PASSWORD'])
		self.db.setDatabaseName(self.config['SQL_DATABASE_NAME'])

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
