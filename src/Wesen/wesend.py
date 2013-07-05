"""Copyright 2003-2013 by Konrad Voelkel and Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit https://github.com/reims/wesen for versions > 2013
or http://wesen.sourceforge.net for old versions of 2003,2004."""

from .definition import NAMES, VERSIONS, FORMAT_LOGSTRING;
from .world import World;
from pprint import pprint;
import logging;
import importlib;

class Wesend(object):
	"""Wesend(config, extraArgs="")
		Runs one Wesen game by start(), with given config data.
		This module intruments a World object
		and, if enabled in the config, a Gui object.
	"""

	def __init__(self, config, extraArgs=""):
		"""config should be a dictionary (see loader.py),
		extraArgs are all passed to OpenGL"""
		#TODO change the NAMES,VERSIONS mechanism to something simpler.
		self.infoGeneral = config["general"];
		self.infoGui = config["gui"];
		self.infoWorld = config["world"];
		self.infoWesen = config["wesen"];
		self.infoFood = config["food"];
		self.infoRange = config["range"];
		self.infoTime = config["time"];
		self.uselog = self.infoGeneral["enablelog"];
		self.initLogger(); # sets self.logger
		self.infoWorld["logger"] = self.logger;
		self.infoWesen["sources"] = self.infoWesen["sources"].split(",");
		self.infoWorld["Debug"] = self.Debug;
		infoAllWorld = {"world" : self.infoWorld,
				"wesen" : self.infoWesen,
				"food"  : self.infoFood,
				"range" : self.infoRange,
				"time"  : self.infoTime};
		self.world = World(infoAllWorld);

	def start(self, extraArgs=""):
		if(self.infoGui["enable"]):
			self.initGUI(extraArgs);
		else:
			self.main();

	def initGUI(self, extraArgs):
		"""handing over all control to the gui"""
		GUI = importlib.import_module(".gui."
					      + self.infoGui["source"],
					      __package__).GUI;
		infoGui = {"config":self.infoGeneral, "wesend":self,
			   "world":self.infoWorld, "wesen":self.infoWesen,
			   "food":self.infoFood, "gui":self.infoGui};
		GUI(infoGui, self.mainLoop, self.world, extraArgs);

	def __del__(self):
		"""stops logging."""
		logging.shutdown();
		super(Wesend, self).__del__();

	def initLogger(self):
		"""initializes the logging system."""
		self.logger = logging.getLogger(NAMES["PROJECT"]);
		if(self.uselog):
			logfileh = logging.FileHandler(self.infoGeneral["logfile"]);
			logfileh.setFormatter(logging.Formatter(FORMAT_LOGSTRING));
			self.logger.addHandler(logfileh);
		self.logger.setLevel(logging.INFO);

	def Debug(self, message):
		"""currently just prints the message."""
		#TODO change or remove the Debug mechanism.
		print("debug message: ", message);

	def mainLoop(self):
		"""calls world.main() in gui-mode (returns world descriptor)"""
		self.world.main();
		return self.world.getDescriptor();

	def main(self):
		"""calls world.main() in gui-less mode,
		until KeyboardInterrupt"""
		while(True):
			try:
				self.world.main();
			except KeyboardInterrupt:
				print(" got keyboard interrupt, stopping now.");
				break;
			if((self.world.turns % 1000) == 0):
				print("turn", self.world.turns, "stats:");
				pprint(self.world.stats, indent=3, depth=4, width=80);
