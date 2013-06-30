from ..point import getRandomPosition;

class WorldObject(object):
	"""this class is an abstraction to all world objects,
	as Wesen, Food and maybe some day something else.
	"""

	def __init__(self, infoAllObject):
		self.infoAllObject = infoAllObject;
		self.infoWorld = self.infoAllObject["world"]
		self.infoObject = self.infoAllObject["object"];
		self.infoRange = self.infoAllObject["range"];
		self.objectType = self.infoObject["type"];
		self.logger = self.infoWorld["logger"];
		self.Debug = self.infoWorld["Debug"];
		self.energy = self.infoObject["energy"];
		self.DeleteObject = self.infoWorld["DeleteObject"];
		self.AddObject = self.infoWorld["AddObject"];
		self.worldObjects = self.infoWorld["objects"];
		self.age = 0;
		self.time = 0;
		self.source = "";
		self.id = id(self);
		self.position = self.infoObject.get("position", getRandomPosition(self.infoWorld["length"]));

	def __repr__(self):
		return "<worldobject id=%s pos=%s energy=%s>" % (self.id, self.position, self.energy);

	def getRangeObjectWithCondition(self, objects, radius, condition):
		"""returns a list with all objects in objectlist in radius,
		   which match the condition"""
		(x,y) = self.position;
		return {i:o for (i,o) in objects.items()
		# the following is a more efficient but equivalent to that:
		#	if ((abs(o.position[0] - x) <= radius) and
		#	    (abs(o.position[1] - y) <= radius))];
			if(condition(o)
			   and (    (((o.position[0] < x) and (x-o.position[0] <= radius))
				     or ((o.position[0] > x) and (o.position[0]-x <= radius))
				     or ((o.position[0] == x)))
				and (((o.position[1] < y) and (y-o.position[1] <= radius))
				     or ((o.position[1] > y) and (o.position[1]-y <= radius))
				     or ((o.position[1] == y)))))};


	def getRangeObject(self, objects, radius):
		"""returns a list with all objects in objectlist in radius."""
		return self.getRangeObjectWithCondition(objects, radius, lambda x : True);

	def Die(self):
		"""deletes WorldObject instance from world."""
		self.DeleteObject(self.id);

	def getDescriptor(self):
		"""return descriptive data for the gui,
		included by the world in World.getDescriptor.
		"""
		return {"position":self.position,
			"energy":self.energy,
			"age":self.age,
			"type":self.objectType};

	def AgeCheck(self):
		"""virtual function, look in wesen or food"""
		pass;

	def EnergyCheck(self):
		"""virtual function, look in wesen or food"""
		pass;

	def main(self):
		"""run one turn of object code"""
		self.EnergyCheck();
		self.age += 1;
		self.AgeCheck();
