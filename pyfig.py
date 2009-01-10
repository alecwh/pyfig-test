"""
pyfig.py
Pyfig is an easy and quick way for you to open, parse, and return values of config files.
$author: alecwh
$version: 1.2
$date: Aug 2008

Copyright 2008 Alec Henriksen
This software is released under the GNU GPL v2, see the COPYING file.
"""
import sys

# important seperator/comment variables
comment_characters = ['#', ';']  # items must be 1 char long
config_seperator = '\n'
individual_seperator = '='

class ConfigError(Exception):
	# used if an error was found while parsing
	pass
	
class Config404Error(Exception):
	# used if files are not found/wrong permissions
	pass

class Pyfig:
	"""contains attributes and methods for the configuration file provided."""
	
	def __init__(self, config_file=None):
		"""init vars and config_file check/parsing"""
		# init vars
		self.config_file = config_file
		self.raw = "" # raw file, string
		self.count = 0 # how many configurations
		self.keys = [] # stores the config keys found
		self.config = {} # the actual dict of configurations
		self.config_temp = [] # for temp storing
		
		# is config file existant?
		if self.config_file == None:
			raise Config404Error("No file path was given for config file")
		
		# try opening the file
		# if error, raise ConfigError
		try:
			config_file = open(self.config_file)
			self.raw = config_file.read().strip()
		except IOError:
			raise Config404Error("The config file could not be opened")
			
		# split file with config_seperator
		self.config_temp = self.raw.split(config_seperator)
		
		# remove blanks (list filtering)
		self.config_temp = [line for line in self.config_temp if line]
		
		# iterate through the new dict
		# skip over any lines that begin with comment_character
		for item in self.config_temp:
			if str(item.strip())[0] not in comment_characters:
				# may be a faulty line, with no sep
				try:
					name, value = item.split(individual_seperator, 1)
					
					# add to config dict and keys list
					self.config[name.strip()] = value.strip()
					self.keys.append(name.strip())
					self.count += 1
				except ValueError:
					raise ConfigError("Improper seperator found in config file")
					
			# close file, we're done
			config_file.close()
			
	def grab(self, name):
		"""grabs the value of a provided name (of a config pair)"""
		# check to see if dict[name] exists
		try:
			return self.config[name]
		except KeyError:
			raise ConfigError("Specified config name was not found while grabbing")
			
	def change(self, name, value):
		"""used to change/add a single configuration for whatever reason"""
		self.config[name] = value
		return self.config[name]
		
if __name__ == "__main__":
	error_message = "File not found (or bad permissions), try again."
	# try to parse file,
	# with given argument (if present), or asking for it
	if len(sys.argv) > 1:
		try:
			pyfig = Pyfig(sys.argv[1])
		except Config404Error:
			print error_message
			sys.exit()
	else:
		while True:
			file_ = raw_input("Enter the config filename: ")
			# try parsing with given input
			try:
				pyfig = Pyfig(file_)
				break
			except Config404Error:
				print error_message
				
	print pyfig.config
