"""Copyright 2003-2013 by Konrad Voelkel and Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit https://github.com/reims/wesen for versions > 2013
or http://wesen.sourceforge.net for old versions of 2003,2004."""

from .defaults import DEFAULT_GAME_STATE_FILE;
from .world import World;
from pprint import pprint;
from os.path import exists;
import importlib;
import json;

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
		self.infoGui = config["gui"];
		self.infoWorld = config["world"];
		self.infoWesen = config["wesen"];
		self.infoFood = config["food"];
		self.infoRange = config["range"];
		self.infoTime = config["time"];
		self.infoWesen["sources"] = self.infoWesen["sources"].split(",");
		self.infoWorld["Debug"] = self.Debug;
		infoAllWorld = {"world" : self.infoWorld,
				"wesen" : self.infoWesen,
				"food"  : self.infoFood,
				"range" : self.infoRange,
				"time"  : self.infoTime};
		if (config.pop("resume", False) and 
		    exists(DEFAULT_GAME_STATE_FILE)):
			with open(DEFAULT_GAME_STATE_FILE, "r") as f:
				string = f.read();
				d = json.loads(string);
				infoAllWorld.update(d);
				self.world = World(infoAllWorld, False);
				self.world.restore(infoAllWorld);
		else:
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
		infoGui = {"wesend":self, "world":self.infoWorld,
			   "wesen":self.infoWesen, "food":self.infoFood,
			   "gui":self.infoGui};
		GUI(infoGui, self.mainLoop, self.world, extraArgs);

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
				self.world.DumpGameState()
				break;
			if((self.world.turns % 1000) == 0):
				print("turn", self.world.turns, "stats:");
				pprint(self.world.stats, indent=3, depth=4, width=80);
