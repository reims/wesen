"""The world in which Wesen takes place"""

from .objects.wesen import Wesen;
from .objects.food import Food;

#BEGIN code for dictproxys:
from ctypes import pythonapi, py_object;
from _ctypes import PyObj_FromPtr;
import json;

DICT_PROXY = pythonapi.PyDictProxy_New;
DICT_PROXY.argtypes = (py_object,);
DICT_PROXY.rettype = py_object;

def make_dictproxy(obj):
	"""takes a dictionary and returns an immutable proxy of it,
	which is more performant than creating a copy."""
	assert isinstance(obj, dict);
	print ("in make_dictproxy");
	return PyObj_FromPtr(DICT_PROXY(obj));
#END code for dictproxys.

class World(object):
	"""A World object contains a single Wesen simulation,
	In the MVC paradigm it is M+C.
	The main() method runs a single simulation turn.
	The getDescriptor() method returns descriptive data for viewers.
	Via AddObject(info) and DeleteObject(id)
	one can manipulate the simulation."""

	def __init__(self, infoAllWorld = None, createObjects = True):
		"""infoAllWorld is a dictionary of dictionaries"""
		#TODO the infoSomething mechanism is very intransparent.
		#     either document it very well or change it
		#     to something more evident...
		#     maybe at least hand over the config as one dictproxy,
		#     without any changes...
		if not infoAllWorld is None:
			self.setInfoAllWord(infoAllWorld);
			if createObjects:
				self.createDefaultObjects();
			self.initStats();

	def setInfoAllWord(self, infoAllWorld):
		"""sets the infoAllWorld and initializes member variables"""
		# copy everything that will be modified
		self.infoAllWorld = infoAllWorld.copy();
		self.infoAllWorld.update({"wesen" : infoAllWorld["wesen"].copy(),
					  "world" : infoAllWorld["world"].copy(),
					  "food" : infoAllWorld["food"].copy()});
		self.objects = {};
		self.turns = 0;
		self.stats = {}; # is initialized depending on sources in initStats()
		self.infoAllWorld["world"].update({"DeleteObject":self.DeleteObject,
						   "AddObject":self.AddObject,
						   "objects":self.objects});
		self.infoAllWorld["food"]["type"] = "food";
		self.infoAllWorld["wesen"]["type"] = "wesen";
		self.infoAllWorld["wesen"]["sources"].sort();

	def createDefaultObjects(self):
		"""creates all objects (wesen and food) as specified by self.infoAllWorld"""
		self.objects = {};
		for entry in self.infoAllWorld["wesen"]["sources"]:
			for _ in range(self.infoAllWorld["wesen"]["count"]):
				#maybe this is preferable to make_dictproxy, since the dict is modified
				#if any wesen looks at this value again after creation, it could see a different source
				temp = self.infoAllWorld["wesen"].copy();#make_dictproxy(self.infoAllWorld["wesen"]);
				temp["source"] = entry;
				self.AddObject(temp);
		for _ in range(self.infoAllWorld["food"]["count"]):
			self.AddObject(self.infoAllWorld["food"]);

	def initStats(self):
		"""resets self.stats to count and energy 0 for all object-types"""
		stats = {"food":{"count":0, "energy":0},
			 "global":{"count":0, "energy":0}};
		for source in self.infoAllWorld["wesen"]["sources"]:
			stats[source] = {"count":0, "energy":0};
		self.stats = stats;

	def DeleteObject(self, objectid):
		"""removes an object from the world."""
		if(objectid in self.objects.keys()):
			del self.objects[objectid];
			return True;
		else:
			return False;

	def AddObject(self, infoObject):
		"""adds an object to the world."""
		infoAllObject = {"world":self.infoAllWorld["world"],
				 "range":self.infoAllWorld["range"],
				 "time":self.infoAllWorld["time"],
				 "food":self.infoAllWorld["food"],
				 "object":infoObject};
		infoAllObject["world"].update({"objects":self.objects});
		if(infoObject["type"] == "wesen"):
			newObject = Wesen(infoAllObject);
		elif(infoObject["type"] == "food"):
			newObject = Food(infoAllObject);
		else:
			raise Exception("invalid objectType: "+infoObject["type"]);
		self.objects[newObject.id] = newObject;
		return newObject;

	def getDescriptor(self):
		"""returns a list of descriptive information for the GUI"""
		return [o.getDescriptor() for o in self.objects.values()];

	def persist(self):
		"""returns a JSON serializable object.

		This object contains all information needed to restore the exact same
		state of the world."""
		d = {"world" : self.infoAllWorld["world"].copy(), #need to copy, since we are modifying it
		     "wesen" : self.infoAllWorld["wesen"],
		     "range" : self.infoAllWorld["range"],
		     "time" : self.infoAllWorld["time"],
		     "food" : self.infoAllWorld["food"],
		     "objects" : [o.persist() for o in self.objects.values()]};
		d["world"].pop("Debug",None);
		d["world"].pop("DeleteObject",None);
		d["world"].pop("AddObject",None);
		d["world"].pop("objects",None);
		return d;

	def restore(self, obj):
		"""restores the state of the world represented by obj"""
		self.objects = {};
		for infoObj in obj["objects"]:
			newObj = self.AddObject(infoObj);
			newObj.restore(infoObj);

	def persistToJSON(self):
		"""returns the persistency info as a JSON string"""
		d = self.persist();
		return json.dumps(d);


	def restoreFromJson(self, string):
		"""restores the state of the world from a JSON string"""
		obj = json.loads(string);
		self.setInfoAllWord(obj);
		self.restore(obj);

	def main(self):
		"""runs one turn of Game code (and all objects code, including the AI)"""
		self.turns += 1;
		self.initStats();
		stats = self.stats;
		# in the following, the self.objects.copy() is inevitable,
		# as the o.main() might modify self.objects.
		for o in self.objects.copy().values():
			if(o.objectType == "wesen"):
				stats[o.source]["count"] += 1;
				stats[o.source]["energy"] += o.energy;
				#stillActive = True;
			else:
				stats["food"]["count"] += 1;
				stats["food"]["energy"] += o.energy;
			o.main();
		stats["global"] = {"count":len(self.objects),
				   "energy":sum(objectType["energy"]
						for objectType
						in stats.values())};
		self.stats = stats;
