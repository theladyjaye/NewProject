import os
import ConfigParser

class Config(object):
	
	def __init__(self, filename):
		"""Initialize the NewProject Config"""
		self.data = ConfigParser.ConfigParser()
		self.data.read(filename);
		options = list(self.data.items("User"))
		options.extend(self.data.items("Apache"))
		
		for item in options:
			key, value = item
			self.__dict__[key] = value
