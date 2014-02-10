"""model and controller for single objects in the simulation"""

from ..point import getRandomPosition;

class WorldObject(object):
	"""this class is an abstraction to all world objects,
	as Wesen, Food and maybe some day something else.
	"""

	def __init__(self, infoAllObject):
		#self.infoAllObject = infoAllObject;
		self.infoWorld = infoAllObject["world"];
		self.infoObject = infoAllObject["object"];
		self.infoRange = infoAllObject["range"];
		self.objectType = self.infoObject["type"];
		self.energy = self.infoObject["energy"];
		self.DeleteObject = self.infoWorld["DeleteObject"];
		self.AddObject = self.infoWorld["AddObject"];
		self.worldObjects = self.infoWorld["objects"];
		self.map = self.infoWorld["map"];
		self.UpdatePos = self.infoWorld["UpdatePos"];
		self.age = 0;
		self.time = 0;
		self.source = "";
		self.dead = False;
		self.id = id(self);
		self.position = self.infoObject.get("position",
						    getRandomPosition(self.infoWorld["length"]));

	def __repr__(self):
		return ("<worldobject id=%s pos=%s energy=%s>" %
			(self.id, self.position, self.energy));

	def getRangeIterator(self, radius, condition):
		"""returns an iterator of pairs (id, object)
		with all objects from objectIterator in radius
		that match the condition.
		The radius is taken in the maximum metric,
		where norm(v) = max(abs(v[0]),abs(v[1]))"""
		#HINT: as this is the most time-consuming function,
		#      timeit-testing has been used to select the
		#      most efficient implementation here.
		#      There is still room for improvement.
		#SEE testradius.py and testrange.py
		#TODO: apparently this comment is outdated already?
		(x, y) = self.position;
		minX = max(0, x-radius);
		maxX = min(self.infoWorld["length"], x+radius+1); #+1 since upper bound of range is exclusive
		minY = max(0, y-radius)
		maxY = min(self.infoWorld["length"], y+radius+1);
		#print(minX, maxX, maxY, maxY, self.infoWorld["length"]);
		return ((i, o)
			for x1 in range(minX, maxX)
			for y1 in range(minY, maxY)
			for (i, o) in self.map[x1][y1].items()
			if (condition is None or condition(o)));

	def Die(self):
		"""deletes WorldObject instance from world."""
		self.dead = True
		self.DeleteObject(self.id);

	def getDescriptor(self):
		"""return descriptive data for the gui,
		included by the world in World.getDescriptor.
		"""
		return {"position":self.position,
			"id":self.id,
			"energy":self.energy,
			"age":self.age,
			"type":self.objectType};

	def persist(self):
		"""returns JSON serializable object with all information
		needed to restore the state of the object"""
		return {"type":self.objectType,
			"energy":self.energy,
			"age":self.age,
			"position":self.position,
			"source":self.source,
			"time":self.time};

	def restore(self, obj):
		"""restores state of this objects from obj"""
		self.age = obj["age"];
		self.energy = obj["energy"];
		self.position = obj["position"];
		self.time = obj["time"];

	def AgeCheck(self):
		"""virtual function, look in wesen or food"""
		pass;

	def EnergyCheck(self):
		"""virtual function, look in wesen or food"""
		pass;

	def main(self):
		"""run one turn of object code"""
		if(not self.dead):
			self.EnergyCheck();
			self.age += 1;
			self.AgeCheck();
