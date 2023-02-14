import json

class Configuration:
	# Config loader and handler
	def __init__(self, config_file):
		# Initialize and store config
		# Takes: String containing the path to the config file in JSON format
		# Returns: Dict containing config information
		
		self.config_file = config_file
		with open(config_file) as jsonfile:
   	 		self.config = json.load(jsonfile)