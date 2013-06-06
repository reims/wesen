"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

from objects.wesen import Wesen;
from objects.food import Food;

class World(object):
	"""World(infoObject) creates a World instance.
	infoObject is a dictionary of dictionarys: world, food, wesen, range, time, etc.
	"""

	def __init__(self, infoAllWorld):
		self.infoWorld = infoAllWorld["world"];
		self.infoFood = infoAllWorld["food"];
		self.infoWesen = infoAllWorld["wesen"];
		self.infoRange = infoAllWorld["range"];
		self.infoTime = infoAllWorld["time"];
		self.Debug = self.infoWorld["Debug"];
		self.logger = self.infoWorld["logger"];
		self.finished = False;
		self.winner = None;
		self.objects = [];
		self.turns = 0;
		self.infoWorld.update(dict(DeleteObject=self.DeleteObject, AddObject=self.AddObject, objects=self.objects));
		self.infoFood["type"] = "food";
		self.infoWesen["type"] = "wesen";
		for entry in self.infoWesen["sources"]:
			for i in range(self.infoWesen["count"]):
				self.infoWesen["source"] = entry;
				self.AddObject(self.infoWesen.copy());
		for i in range(self.infoFood["count"]):
			self.AddObject(self.infoFood);

	def DeleteObject(self, objectid):
		"""removes an object from the world."""
		for object in self.objects:
			if(id(object) == objectid):
				del(self.objects[self.objects.index(object)]);
				return True;
		return False;

	def AddObject(self, infoObject):
		"""adds an object to the world."""
		infoAllObject = dict(world=self.infoWorld, range=self.infoRange, object=infoObject, time=self.infoTime, food=self.infoFood);
		if(infoObject["type"] == "wesen"):
			newObject = Wesen(infoAllObject);
		elif(infoObject["type"] == "food"):
			newObject = Food(infoAllObject);
		else:
			self.Debug("critical\tWorld.AddObject\tinvalid objectType specified in infoObject", level="error");
			newObject = None;
		self.objects.append(newObject);
		return newObject;

	def getDescriptor(self):
		"""returns a list of description information for the GUI,
		[{"finished":Boolean}[...]]
		where [...] is a list of all objects descriptors in the world."""
		return [dict(finished=self.finished), [object.getDescriptor() for object in self.objects]];

	def getEnergy(self):
		return self.energy;

	def main(self):
		"""runs one turn of Game code (and all objects code, including the AI)"""
		stillActive = False;
		self.turns += 1;
		sources = dict(food=dict(count=0,energy=0));
		globalEnergy = 0;
		for object in self.objects:
			globalEnergy += object.energy;
			if(type(object) is Wesen):
				try:
					sources[object.source];
				except KeyError:
					sources[object.source] = {};
					sources[object.source]["count"] = 0;
					sources[object.source]["energy"] = 0;
				sources[object.source]["count"] += 1;
				sources[object.source]["energy"] += object.energy;
				stillActive = True;
			else:
				sources["food"]["count"] += 1;
				sources["food"]["energy"] += object.energy;
			object.main();
		self.energy = globalEnergy;
		self.stats = sources;
		if(len(sources.keys()) == 2):
                        self.winner = [s for s in sources if s != "food"][0]
                        print("the winner is %s" % self.winner)
		if(not (stillActive)):
			self.finished = True;
