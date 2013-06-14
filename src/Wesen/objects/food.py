"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

from .base import WorldObject;
from ..point import *;
from ..strings import STRING_LOGGER;
from random import randint, uniform;

class Food(WorldObject):
	"""unlike wesen, who are programmable and capable of intelligence,
	food can only grow every turn and reproduce by seeds.
	"""

	def __init__(self, infoAllWorld):
		WorldObject.__init__(self, infoAllWorld);
		self.seedrate = self.infoObject["seedrate"];
		self.growrate = self.infoObject["growrate"];
		self.rangeseed = self.infoRange["seed"];
		self.maxamount = self.infoObject["maxamount"];
		#self.marange = self.getMarange();

	def __repr__(self):
		return "<food id=%s static=%s pos=%s energy=%s>" % (id(self), (self.growrate==0), self.position, self.energy);

	def getDescriptor(self):
		"""currently doing nothing than returning the WorldObjects getDescriptor."""
		return WorldObject.getDescriptor(self);

	def getEaten(self):
		"""(seeds new food) * seedrate,
		dies and returns energy amount before.
		"""
		energy = self.energy;
		if(energy):
			self.Die();
		return energy;

	def Grow(self):
		"""increment energy by growrate."""
		self.energy += self.growrate;

	def Seed(self):
		"""create a new Food instance in seedrange."""
		infoFood = self.infoObject;
		infoFood["energy"] = 1;
		infoFood["position"] = getRandomPositionInRadius(self.position, self.rangeseed, self.infoWorld["length"]);
		return self.AddObject(infoFood);

	def AgeCheck(self):
		if(self.age >= self.infoObject["maxage"]):
			self.logger.info(STRING_LOGGER["DEATHFOOD"]["AGE"] % id(self));
			self.Die();

	def EnergyCheck(self):
		if(self.energy >= self.infoObject["maxamount"]):
			self.energy = self.infoObject["maxamount"];
			self.growrate = 0;
		if(self.energy < 0):
			self.energy = 0;
			print("warning: food energy lower than zero detected");
                        
	#def getMarange(self):
	#	return self.getRangeObject(self.worldObjects, self.rangeseed);

	def main(self):
		"""randomly grow or seed, based on growrate and seedrate.
		When too old, die."""
		WorldObject.main(self);
		range = self.getRange(2);
		food_count = 0;
		for o in range:
			if o["type"] == food:
				food_count += 1;
		if uniform(0,1) < self.seedrate and self.age > 5 and food_count < 40: #TODO 5 and 20 should be a config option
			self.Seed();
		self.Grow();
