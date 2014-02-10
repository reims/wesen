"""The true purpose of the configuration editor ConfigEd is
to provide an explanation of the options in the config file.

See also:
 strings.py for explanations used here,
 defaults.py for defaults used here."""

from .defaults import CONFIG_OPTIONS, CONFIG_DEFAULTS;
from .strings import STRING_ERROR_FILEEXISTS, \
    STRING_MESSAGE_WROTE, \
    STRING_ERROR_NOTWROTE, \
    STRING_CONFIGED;

# import the correct version of ConfigParser:
from sys import version_info;
if version_info.major == 3 and version_info.minor < 2: # pre version 3.2 
	from configparser import SafeConfigParser;
elif version_info.major >= 3: # up to date version
	from configparser import ConfigParser as SafeConfigParser;
else: # python2
	from ConfigParser import SafeConfigParser;
import os.path;

class ConfigEd(object):
	"""ConfigEd(filename) creates a full powered config editor for wesen"""

	def __init__(self, filename):
		self.configfile = filename;
		self.configParser = SafeConfigParser();
		self.alwaysDefaults = False;

	def printConfig(self):
		"""prints the configfile to screen"""
		print(("%s:" % self.configfile));
		for line in open(self.configfile).readlines():
			print(line[:-1]); # -1 for \n removal
		print(".");

	def getConfig(self):
		"""getConfig() returns the config dict.

		if a section, option or value is not found,
		the default values will be returned.
		"""
		if(os.path.exists(self.configfile)):
			self.configParser.read(self.configfile);
			result = {};
			for entry in CONFIG_OPTIONS:
				(section, options) = entry;
				result[section] = {};
				if(self.configParser.has_section(section)):
					for option in options:
						(key, entryType) = option;
						result[section][key] = \
						    self.getEntryFromConfigParser(section, key, entryType);
			return result;
		else:
			self.writeDefaults();
			return self.getConfig();

	def getEntryFromConfigParser(self, section, key, entryType):
		"""depending on entryType,
		calls the appropriate getter from self.configParser"""
		value = None;
		if(entryType == str):
			value = self.configParser.get(section, key);
		elif(entryType == int):
			value = self.configParser.getint(section, key);
		elif(entryType == bool):
			value = self.configParser.getboolean(section, key);
		elif(entryType == float):
			value = self.configParser.getfloat(section, key);
		if(value is None):
			value = CONFIG_DEFAULTS[section][key];
		return value;

	def writeDefaults(self):
		"""write config defaults to file."""
		self.alwaysDefaults = True;
		self.edit();

	def edit(self):
		"""Interactive config-file editing;

		It will ask the user every single option possible,
		always showing the default values and sometimes a comment,
		making it easier to understand the configfile for newbies.
		"""
		if(self.alwaysDefaults):
			write = True;
		elif(os.path.exists(self.configfile)):
			write = (input(STRING_ERROR_FILEEXISTS % self.configfile) == "y");
		else:
			write = True;
		if(write):
			self.configParser.read(self.configfile);
			for entry in CONFIG_OPTIONS:
				(section, options) = entry;
				if(not self.configParser.has_section(section)):
					self.configParser.add_section(section);
				if(not self.alwaysDefaults):
					print("[%s]" % (section));
				for option in options:
					key = option[0];
					self.setDefInputStandard(section, key);
			self.configParser.write(open(self.configfile, "w"));
			print((STRING_MESSAGE_WROTE % self.configfile));
		else:
			print((STRING_ERROR_NOTWROTE % self.configfile));

	def setDefInputStandard(self, section, key):
		"""fetches explanation from .strings
		and default value from .defaults"""
		#TODO why upper? we should have lower-case here.
		explanationString = STRING_CONFIGED[section.upper()][key.upper()];
		self.configParser.set(section, key,
				      str(self.def_input(CONFIG_DEFAULTS[section][key],
							 explanationString)));

	def def_input(self, default, msg):
		"""derived from raw_input,
		def_input(default,prompt) returns a user input or,
		if blank, the specified default.
		"""
		if(not self.alwaysDefaults):
			try:
				result = input("# default: %s\t%s" %\
					(default, msg));
			except EOFError:
				self.alwaysDefaults = True;
				return default;
			print("");
			if(not result):
				return default;
			else:
				return result;
		else:
			return default;
