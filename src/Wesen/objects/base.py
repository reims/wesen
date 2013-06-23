"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

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
		self.position = self.infoObject.get("position", getRandomPosition(self.infoWorld["length"]));

	def __repr__(self):
		return "<worldobject id=%s pos=%s energy=%s>" % (id(self), self.position, self.energy);

	def getRangeObject(self, objectList, radius):
		"""returns a list with all objects in objectlist in radius."""
		(x,y) = self.position;
		return [o for o in objectList
			if ((abs(o.position[0] - x) <= radius) and
			    (abs(o.position[1] - y) <= radius))];

	def getRange(self, radius):
		"""returns getRangeObject(MaxRange, radius).
		This is faster than always using a list of all Wesen.
		"""
		return self.getRangeObject(self.maxRange, radius);

	def ChangePosition(self, newPosition):
		"""changes the position to newPosition.
		currently, this function does nothing than
		self.position = newPosition;
		but it could be used for more complex game features.
		"""
		self.position = newPosition;

	def Die(self):
		"""deletes WorldObject instance from world."""
		self.energy = 0;
		self.DeleteObject(id(self));

	def getDescriptor(self):
		"""return descriptive data for the gui,
		included by the world in World.getDescriptor.
		"""
		return dict(position=self.position, energy=self.energy, age=self.age, type=self.objectType);

	def AgeCheck(self):
		"""virtual function, look in wesen or food"""
		pass;

	def EnergyCheck(self):
		"""virtual function, look in wesen or food"""
		pass;

	def getMaxRange(self):
		"""virtual function, look in wesen or food"""
		return [];

	def RoundInit(self):
		self.EnergyCheck();
		self.age += 1;
		self.AgeCheck();
		self.maxRange = self.getMaxRange();

	def main(self):
		"""run one turn of object code"""
		self.RoundInit();
