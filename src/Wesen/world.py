"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

from .objects.wesen import Wesen;
from .objects.food import Food;
from ctypes import pythonapi, py_object;
from _ctypes import PyObj_FromPtr;
DictProxy = pythonapi.PyDictProxy_New;
DictProxy.argtypes = (py_object,);
DictProxy.rettype = py_object;

def make_dictproxy(obj):
	assert isinstance(obj,dict);
	return PyObj_FromPtr(DictProxy(obj));

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
		self.objects = dict();
		self.turns = 0;
		self.infoWorld.update(dict(DeleteObject=self.DeleteObject, AddObject=self.AddObject, objects=self.objects));
		self.infoFood["type"] = "food";
		self.infoWesen["type"] = "wesen";
		for entry in self.infoWesen["sources"]:
			for i in range(self.infoWesen["count"]):
				self.infoWesen["source"] = entry;
				self.AddObject(make_dictproxy(self.infoWesen));
		for i in range(self.infoFood["count"]):
			self.AddObject(self.infoFood);

	def DeleteObject(self, objectid):
		"""removes an object from the world."""
		if(objectid in self.objects.keys()):
			del self.objects[objectid];
			return True;
		else:
			return False;
		#for o in self.objects.values():
		#	if(o.id == objectid):
		#		del(self.objects[self.objects.index(o)]);
		#		return True;
		#return False;

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
		self.objects[newObject.id] = newObject;
		return newObject;

	def getDescriptor(self):
		"""returns a list of description information for the GUI,
		[{"finished":Boolean}[...]]
		where [...] is a list of all objects descriptors in the world."""
		return [dict(finished=self.finished), [object.getDescriptor() for object in self.objects.values()]];

	def getEnergy(self):
		return self.energy;

	def main(self):
		"""runs one turn of Game code (and all objects code, including the AI)"""
		stillActive = False;
		self.turns += 1;
		sources = dict(food=dict(count=0,energy=0));
		for source in self.infoWesen["sources"]:
			sources[source]=dict(count=0,energy=0);
		globalEnergy = 0;
		for o in self.objects.copy().values():
			globalEnergy += o.energy;
			if(o.objectType == "wesen"):
				sources[o.source]["count"] += 1;
				sources[o.source]["energy"] += o.energy;
				stillActive = True;
			else:
				sources["food"]["count"] += 1;
				sources["food"]["energy"] += o.energy;
			o.main();
		self.energy = globalEnergy;
		self.stats = sources;
		#if(len(list(sources.keys())) == 2):
                #        self.winner = [s for s in sources if s != "food"][0]
		if(not (stillActive)):
			self.finished = True;
