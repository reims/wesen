"""Copyright 2003-2013 by Konrad Voelkel and Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit https://github.com/reims/wesen for versions > 2013
or http://wesen.sourceforge.net for old versions of 2003,2004."""

from .definition import NAMES, VERSIONS, FORMAT_LOGSTRING;
from .defaults import DEFAULT_GENERAL_CONFIGFILE;
from .strings import *;
from .world import World;
from .configed import ConfigEd;
from optparse import OptionParser;
from time import time, sleep;
from pprint import pprint;
import re;
import logging;
import importlib;

class Wesend:
	"""Wesend([configfile])
		reads the config if specified (else defaults),
		Runs one Wesen game directly on initialization.
	"""

	def __init__(self, *args):
		#print "%s %s %s %s" % (NAMES["PROJECT"], VERSIONS["PROJECT"], NAMES["WESEND"], VERSIONS["WESEND"]);
		if(len(args) > 0):
			self.configfile = args[0];
		else:
			self.configfile = DEFAULT_GENERAL_CONFIGFILE;
		self.readConfig();
		self.readCommandLine();
		self.uselog = self.infoGeneral["enablelog"];
		self.initLogger();
		self.infoWorld["logger"] = self.logger;
		self.infoWesen["sources"] = self.infoWesen["sources"].split(",");
		self.infoWorld["Debug"] = self.Debug;
		self.running = True;
		self.finished = False;
		infoAllWorld = {"world":self.infoWorld, "wesen":self.infoWesen, "food":self.infoFood,
                                "range":self.infoRange, "time":self.infoTime};
		self.world = World(infoAllWorld);
		if(self.infoGui["enable"]):
			self.usegui = True;
		else:
			self.usegui = False;
		if(self.usegui):
			self.initGUI();
		else:
			self.main();

	def runCondition(self):
		"""returns False if the game or the world stopped"""
		return (not (self.world.finished or self.finished));

	def initGUI(self):
		"""handing over all control to the gui"""
		GUI = importlib.import_module(".gui."+self.infoGui["source"], __package__).GUI;
		infoGui = dict(config=self.infoGeneral, wesend=self, world=self.infoWorld, wesen=self.infoWesen, food=self.infoFood, gui=self.infoGui);
		self.gui = GUI(infoGui, self.mainLoop, self.world);

	def __del__(self):
		"""stops logging."""
		logging.shutdown();
		object.__del__();

	def initLogger(self):
		"""initializes the logging system."""
		self.logger = logging.getLogger(NAMES["PROJECT"]);
		if(self.uselog):
			logfileh = logging.FileHandler(self.infoGeneral["logfile"]);
			logfileh.setFormatter(logging.Formatter(FORMAT_LOGSTRING));
			self.logger.addHandler(logfileh);
		self.logger.setLevel(logging.INFO);

	def readCommandLine(self):
		"""uses optparse class OptionParser;

		overwrites the default values and the specified configfile,
		type "./wesend.py --help" or
		"python wesend.py --help" for usage
		"""
		optionParser = OptionParser(STRING_USAGE_WESEND);
		optionParser.add_option("-d", "--disablegui", dest="enablegui", action="store_false",
                                        help=STRING_USAGE_WESEND_DISABLEGUI);
		optionParser.add_option("-g", "--enablegui", dest="enablegui", action="store_true",
                                        help=STRING_USAGE_WESEND_ENABLEGUI);
		optionParser.add_option("--guisource", dest="guisource", action="store",
                                        help=STRING_USAGE_WESEND_GUISOURCE);
		optionParser.add_option("-q", "--quiet", dest="enablelog", action="store_false",
                                        help=STRING_USAGE_WESEND_QUIET);
		optionParser.add_option("-l", "--logfile", dest="logfile", action="store",
                                        help=STRING_USAGE_WESEND_LOGFILE);
		optionParser.add_option("-c", "--configfile", dest="configfile", action="store",
                                        help=STRING_USAGE_WESEND_CONFIGFILE);
		(options, args) = optionParser.parse_args();
		if(not options.enablegui == None):
			self.infoGeneral["enablegui"] = options.enablegui;
		if(not options.guisource == None):
			self.infoGeneral["guisource"] = options.guisource;
		if(not options.enablelog == None):
			self.infoGeneral["enablelog"] = options.enablelog;
		if(not options.logfile == None):
			self.infoGeneral["logfile"] = options.logfile;
		if(not options.configfile == None):
			self.configfile = options.configfile;
		if(self.configfile != DEFAULT_GENERAL_CONFIGFILE):
			self.readConfig();

	def readConfig(self):
		"""uses ConfigEd method getConfig;

		replaces found configuration by command-line arguments
		and uses defaults when no config values specified.
		"""
		configEd = ConfigEd(self.configfile);
		config = configEd.getConfig([\
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
		self.infoGeneral = config["general"];
		self.infoGui = config["gui"];
		self.infoWorld = config["world"];
		self.infoWesen = config["wesen"];
		self.infoFood = config["food"];
		self.infoRange = config["range"];
		self.infoTime = config["time"];

	def Debug(self, msg, level="info"):
		"""gives the debug message to all debugging systems,
		usually the gui and the logfile.
		"""
		if(self.infoGeneral["enablelog"]):
			if(self.usegui):
				self.gui.Debug(msg);

	def DelayStart(self):
		self.delaystart = time();

	def DelayEnd(self, milliseconds):
		while((time()-self.delaystart) <= (milliseconds/1000)):
			sleep(milliseconds/100);

	def run(self):
		if(self.running):
			self.world.main();

	def mainLoop(self):
		"""run the world and let the GUI draw until world.finished."""
		if(self.runCondition()):
			self.run();
		return self.world.getDescriptor();

	def main(self):
		while(self.runCondition()):
			self.run();
			if((self.world.turns % 50) == 0):
				print("stats:");
				pprint(self.world.stats, indent=2, depth=4, width=80);
		if(self.world.winner):
			print(("Congratulations, \"%s\" has won the game" % (self.world.winner)));
		else:
			print("Sorry, nobody has won the game");
