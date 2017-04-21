#! /usr/bin/python
# -*- cofing: utf-8 -*-

import yaml
import os

class Config:
	def __init__(self):
		default_config_file_path = 'default-config.yml'
		user_config_file_path = 'user-config.yml'

		# read config files
		is_user_config_file_exist = os.path.exists(user_config_file_path)

		default_config_file = open(default_config_file_path, 'r')
		default_config = yaml.load(default_config_file)
		default_config_file.close()
		if is_user_config_file_exist:
			user_config_file = open(user_config_file_path, 'r')
			user_config = yaml.load(user_config_file)
			user_config_file.close()

		self.config = {}
		if is_user_config_file_exist:
			config_keys = default_config.keys()
			for i in range(len(default_config)):
				if config_keys[i] in user_config:
					self.config[config_keys[i]] = user_config[config_keys[i]]
				else:
					self.config[config_keys[i]] = default_config[config_keys[i]]
		else:
			self.config = default_config

