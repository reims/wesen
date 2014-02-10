"""The world in which Wesen takes place"""

from .objects.wesen import Wesen, RuleException;
from .objects.food import Food;
from .objects.base import TurnOverException;

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

	def __init__(self, infoAllWorld = None, createObjects = True, callbacks = {}):
		"""infoAllWorld is a dictionary of dictionaries"""
		#TODO the infoSomething mechanism is very intransparent.
		#     either document it very well or change it
		#     to something more evident...
		#     maybe at least hand over the config as one dictproxy,
		#     without any changes...
		self.callbacks = callbacks;
		if not infoAllWorld is None:
			self.map = [[{} for _ in range(infoAllWorld["world"]["length"])]
				      for _ in range(infoAllWorld["world"]["length"])];
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
						   "UpdatePos":self.UpdatePos,
						   "objects":self.objects,
						   "map":self.map});
		self.infoAllWorld["food"]["type"] = "food";
		self.infoAllWorld["wesen"]["type"] = "wesen";
		self.infoAllWorld["wesen"]["sources"].sort();

	def setCallbacks(self, callbacks):
		self.callbacks = callbacks;

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
		pos = self.objects[objectid].position;
		del self.map[pos[0]][pos[1]][objectid];
		del self.objects[objectid];
		#print("Deleted object with id", objectid);
		self.callbacks.get("DeleteObject", lambda _id: None)(objectid);
		return True;

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
		self.map[newObject.position[0]][newObject.position[1]][newObject.id] = newObject;
		#print("Added new", infoObject["type"], "with id", newObject.id, "at", newObject.position);
		self.callbacks.get("AddObject", lambda _id,obj: None)(newObject.id, newObject.getDescriptor());
		return newObject;

	def UpdatePos(self, _id, oldPos, obj):
		del self.map[oldPos[0]][oldPos[1]][_id];
		newPos = obj["position"];
		self.map[newPos[0]][newPos[1]][_id] = self.objects[_id];
		#print("Moved object with id", _id, "from", oldPos, "to", newPos);
		self.callbacks.get("UpdatePos", lambda _id,obj: None)(_id,obj);

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
		d["world"].pop("Debug", None);
		d["world"].pop("DeleteObject", None);
		d["world"].pop("AddObject", None);
		d["world"].pop("objects", None);
		d["world"].pop("UpdatePos", None);
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
			try:
				o.main();
			except TurnOverException: pass
			except RuleException: pass #TODO: make offending source loose
		stats["global"] = {"count":len(self.objects),
				   "energy":sum(objectType["energy"]
						for objectType
						in stats.values())};
		self.stats = stats;
