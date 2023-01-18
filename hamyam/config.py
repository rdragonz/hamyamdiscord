import json

class Configuration:

	def __init__(self, config_file):

		self.config_file = config_file
		with open(config_file) as jsonfile:
   	 		self.config = json.load(jsonfile)