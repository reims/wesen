from .definition import *;
from .defaults import *;
from .strings import *;
from configparser import SafeConfigParser;
from sys import argv;
import os.path;

def upper(str):
        return str.upper()

class ConfigEd(object):
	"""ConfigEd(filename) creates a full powered config editor for wesen"""

	def __init__(self,filename):
		self.configfile = filename;
		self.configParser = SafeConfigParser();
		self.alwaysDefaults = False;

	def def_input(self,default,msg):
		"""derived from raw_input,
		def_input(default,prompt) returns a user input or, if blank, the specified default.
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

	def printConfig(self):
		"""prints the configfile to screen"""
		print(("%s:" % self.configfile));
		for line in open(self.configfile).readlines():
			print((line[:-1])); # for \n removal
		print(".");


	def getConfig(self):
		return self.getConfigGeneric([\
			["general", [("enablelog",bool), ("logfile",str)]],\
			["gui", [("enable",bool), ("source",str), ("size",int),\
					("pos",str), ("map",bool), ("graph",bool),\
					("text",bool)]],\
			["world", [("length",int)]],\
			["wesen", [("sources",str), ("count",int), ("energy",int),\
					("maxage",int)]],\
			["food", [("count",int), ("energy",int), ("maxamount",int),\
					("seedrate",float), ("growrate",int),\
					("maxage",int)]],\
			["range", [("look",int), ("closer_look", int), ("talk",int), ("seed",int)]],\
			["time", [("init",int), ("max",int), ("look",int),\
					("closerlook",int), ("move",int),\
					("eat",int), ("talk",int), ("vomit",int),\
					("broadcast",int), ("attack",int),\
					("donate",int), ("reproduce",int)]]]);

	def getConfigGeneric(self, which):
		"""getConfigGeneric(which) returns the config dict.

		if a section, option or value is wrong formatted or does not exist,
		the default values will be returned.
		"""
		if(os.path.exists(self.configfile)):
			self.configParser.read(self.configfile);
			result = {};
			for entry in which:
				value = None;
				exec("result[\"%s\"] = {};" % entry[0]);
				if(self.configParser.has_section(entry[0])):
					for option in entry[1]:
						if(option[1] == str):
							value = self.configParser.get(entry[0],option[0]);
						elif(option[1] == int):
							value = self.configParser.getint(entry[0],option[0]);
						elif(option[1] == bool):
							value = self.configParser.getboolean(entry[0],option[0]);
						elif(option[1] == float):
							value = self.configParser.getfloat(entry[0], option[0]);
						if(value == None):
							exec("value = DEFAULT_%s_%s;" % (upper(entry[0]), upper(option[0])));
						exec("result[\"%s\"][option[0]] = value;" % entry[0]);
			return result;
		else:
			self.writeDefaults();
			return self.getConfig(which);

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
			overwrite = True;
		elif(os.path.exists(self.configfile)):
			if(input(STRING_ERROR_FILEEXISTS % self.configfile)=="y"):
				overwrite = True;
			else:
				overwrite = False;
		else:
			overwrite = True;
		if overwrite:
			self.configParser.read(self.configfile);
			print((self.configfile));
			if(not self.configParser.has_section("wesen")):
				self.configParser.add_section("wesen");
			print("[wesen]");
			self.configParser.set("wesen","sources",
					      str(self.def_input(DEFAULT_WESEN_SOURCES,
								 STRING_CONFIGED["WESEN"]["SOURCES"])));
			self.configParser.set("wesen","count", str(self.def_input(DEFAULT_WESEN_COUNT,
                             STRING_CONFIGED["WESEN"]["COUNT"])));
			self.configParser.set("wesen","energy", str(self.def_input(DEFAULT_WESEN_ENERGY,
                             STRING_CONFIGED["WESEN"]["ENERGY"])));
			self.configParser.set("wesen","maxage", str(self.def_input(DEFAULT_WESEN_MAXAGE,
                             STRING_CONFIGED["WESEN"]["MAXAGE"])));
			if(not self.configParser.has_section("gui")):
				self.configParser.add_section("gui");
			print("[gui]");
			self.configParser.set("gui","enable",
					      str(self.def_input(DEFAULT_GUI_ENABLE,
								 str(STRING_CONFIGED["GUI"]["ENABLE"]))));
			self.configParser.set("gui","source",
					      str(self.def_input(DEFAULT_GUI_SOURCE,
								 STRING_CONFIGED["GUI"]["SOURCE"])));
			self.configParser.set("gui","size", str(self.def_input(DEFAULT_GUI_SIZE,
                             STRING_CONFIGED["GUI"]["SIZE"])));
			self.configParser.set("gui","pos", str(self.def_input(DEFAULT_GUI_POS,
                             STRING_CONFIGED["GUI"]["POS"])));
			self.configParser.set("gui","map", str(self.def_input(DEFAULT_GUI_MAP,
                             STRING_CONFIGED["GUI"]["MAP"])));
			self.configParser.set("gui","graph", str(self.def_input(DEFAULT_GUI_GRAPH,
                             STRING_CONFIGED["GUI"]["GRAPH"])));
			self.configParser.set("gui","text", str(self.def_input(DEFAULT_GUI_TEXT,
                             STRING_CONFIGED["GUI"]["TEXT"])));
			if(not self.configParser.has_section("general")):
				self.configParser.add_section("general");
			print("[general]");
			self.configParser.set("general","enablelog",
                             str(self.def_input(DEFAULT_GENERAL_ENABLELOG,STRING_CONFIGED["GENERAL"]["ENABLELOG"])));
			self.configParser.set("general","logfile", str(self.def_input(DEFAULT_GENERAL_LOGFILE,
                             STRING_CONFIGED["GENERAL"]["LOGFILE"])));
			if(not self.configParser.has_section("world")):
				self.configParser.add_section("world");
			print("[world]");
			self.configParser.set("world","length", str(self.def_input(DEFAULT_WORLD_LENGTH,
                             STRING_CONFIGED["WORLD"]["LENGTH"])));
			if(not self.configParser.has_section("food")):
				self.configParser.add_section("food");
			print("[food]");
			self.configParser.set("food","count", str(self.def_input(DEFAULT_FOOD_COUNT,
                             STRING_CONFIGED["FOOD"]["COUNT"])));
			self.configParser.set("food","energy", str(self.def_input(DEFAULT_FOOD_AMOUNT,
                             STRING_CONFIGED["FOOD"]["AMOUNT"])));
			self.configParser.set("food","maxamount", str(self.def_input(DEFAULT_FOOD_MAXAMOUNT,
                             STRING_CONFIGED["FOOD"]["MAXAMOUNT"])));
			self.configParser.set("food","maxage", str(self.def_input(DEFAULT_FOOD_MAXAGE,
                             STRING_CONFIGED["FOOD"]["MAXAGE"])));
			self.configParser.set("food","seedrate", str(self.def_input(DEFAULT_FOOD_SEEDRATE,
                             STRING_CONFIGED["FOOD"]["SEEDRATE"])));
			self.configParser.set("food","growrate", str(self.def_input(DEFAULT_FOOD_GROWRATE,
                             STRING_CONFIGED["FOOD"]["GROWRATE"])));
			if(not self.configParser.has_section("range")):
				self.configParser.add_section("range");
			print("[range]");
			self.configParser.set("range","look", str(self.def_input(DEFAULT_RANGE_LOOK,
                             STRING_CONFIGED["RANGE"]["LOOK"])));
			self.configParser.set("range","closer_look", str(self.def_input(DEFAULT_RANGE_CLOSER_LOOK,
                             STRING_CONFIGED["RANGE"]["CLOSER_LOOK"])));
			self.configParser.set("range","talk", str(self.def_input(DEFAULT_RANGE_TALK,
                             STRING_CONFIGED["RANGE"]["TALK"])));
			self.configParser.set("range","seed", str(self.def_input(DEFAULT_RANGE_SEED,
                             STRING_CONFIGED["RANGE"]["SEED"])));
			if(not self.configParser.has_section("time")):
				self.configParser.add_section("time");
			print("[time]");
			self.configParser.set("time","init", str(self.def_input(DEFAULT_TIME_INIT,
                             STRING_CONFIGED["TIME"]["INIT"])));
			self.configParser.set("time","max", str(self.def_input(DEFAULT_TIME_MAX,
                             STRING_CONFIGED["TIME"]["MAX"])));
			self.configParser.set("time","look", str(self.def_input(DEFAULT_TIME_LOOK,
                             STRING_CONFIGED["TIME"]["LOOK"])));
			self.configParser.set("time","closerlook", str(self.def_input(DEFAULT_TIME_CLOSERLOOK,
                             STRING_CONFIGED["TIME"]["CLOSERLOOK"])));
			self.configParser.set("time","move", str(self.def_input(DEFAULT_TIME_MOVE,
                             STRING_CONFIGED["TIME"]["MOVE"])));
			self.configParser.set("time","eat", str(self.def_input(DEFAULT_TIME_EAT,
                             STRING_CONFIGED["TIME"]["EAT"])));
			self.configParser.set("time","talk", str(self.def_input(DEFAULT_TIME_TALK,
                             STRING_CONFIGED["TIME"]["TALK"])));
			self.configParser.set("time","vomit", str(self.def_input(DEFAULT_TIME_VOMIT,
                             STRING_CONFIGED["TIME"]["VOMIT"])));
			self.configParser.set("time","attack", str(self.def_input(DEFAULT_TIME_ATTACK,
                             STRING_CONFIGED["TIME"]["ATTACK"])));
			self.configParser.set("time","broadcast", str(self.def_input(DEFAULT_TIME_BROADCAST,
                             STRING_CONFIGED["TIME"]["BROADCAST"])));
			self.configParser.set("time","Donate", str(self.def_input(DEFAULT_TIME_DONATE,
                             STRING_CONFIGED["TIME"]["DONATE"])));
			self.configParser.set("time","reproduce", str(self.def_input(DEFAULT_TIME_REPRODUCE,
                             STRING_CONFIGED["TIME"]["REPRODUCE"])));
			print(".");
			self.configParser.write(open(self.configfile,"w"));
			print((STRING_MESSAGE_WROTE % self.configfile));
		else:
			print((STRING_ERROR_NOTWROTE % self.configfile));
