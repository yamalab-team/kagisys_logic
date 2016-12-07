#! /usr/bin/python
# -*- cofing: utf-8 -*-

import yaml

class Config:
	def __init__(self):
		self.SQL_USER_NAME = 22
		#locals()["SQL_USER_NAME"] = 34
		default_config_file_path = 'default-config.yml'
		user_config_file_path = 'user-config.yml'

		# read config files
		default_config_file = open(default_config_file_path, 'r')
		user_config_file = open(user_config_file_path, 'r')
		default_config = yaml.load(default_config_file)
		user_config = yaml.load(user_config_file)
		default_config_file.close()
		user_config_file.close()

		self.config = {}
		config_keys = default_config.keys()
		for i in range(len(default_config)):
			if config_keys[i] in user_config:
				self.config[config_keys[i]] = user_config[config_keys[i]]
			else:
				self.config[config_keys[i]] = default_config[config_keys[i]]

