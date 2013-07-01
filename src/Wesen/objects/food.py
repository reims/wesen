"""The Food class, which is present in every simulation."""

from .base import WorldObject;
from ..point import getRandomPositionInRadius;
from ..strings import STRING_LOGGER;
from numpy.random import uniform;

class Food(WorldObject):
	"""unlike wesen, who are programmable and capable of intelligence,
	food can only grow every turn and reproduce over distance.
	"""

	def __init__(self, infoAllWorld):
		WorldObject.__init__(self, infoAllWorld);
		self.source = "food";
		self.seedrate = self.infoObject["seedrate"];
		self.growrate = self.infoObject["growrate"];
		self.rangeseed = self.infoRange["seed"];
		self.maxamount = self.infoObject["maxamount"];

	def __repr__(self):
		return ("<food id=%s growrate=%s pos=%s energy=%s>" %
			(self.id, self.growrate, self.position, self.energy));

	def getDescriptor(self):
		"""currently doing nothing than returning the WorldObjects getDescriptor."""
		return WorldObject.getDescriptor(self);

	def getEaten(self):
		"""dies and returns previous energy amount.
		"""
		energy = self.energy;
		if(energy):
			self.Die();
		return energy;

	def Grow(self):
		"""increment energy by some amount."""
		self.energy += int(uniform(0,2)*self.growrate);

	def Seed(self):
		"""create a new Food instance in seedrange."""
		infoFood = self.infoObject;
		infoFood["energy"] = 1;
		infoFood["position"] = getRandomPositionInRadius(self.position,
								 self.rangeseed,
								 self.infoWorld["length"]);
		return self.AddObject(infoFood);

	def AgeCheck(self):
		if(self.age >= self.infoObject["maxage"]):
			self.logger.info(STRING_LOGGER["DEATHFOOD"]["AGE"] % self.id);
			self.Die();

	def EnergyCheck(self):
		if(self.energy >= self.infoObject["maxamount"]):
			self.energy = self.infoObject["maxamount"];
		elif(self.energy < 0):
			self.energy = 0;
			# this happens only if one manipulates food via the GUI
			#TODO the GUI should be more careful and this raise an Error.
			print("warning: food energy lower than zero detected");

	def getNearbyFoodCount(self):
		return len(self.getRange(self.worldObjects,
					 self.rangeseed,
					 condition = lambda o : o.source == "food"));

	def main(self):
		"""randomly grow or seed, based on growrate and seedrate.
		When too old, die."""
		WorldObject.main(self); # handles age and low-energy death
		if(self.age > 10): #TODO numbers should be a config option
			if(uniform(0,1) < self.seedrate):
				if(self.getNearbyFoodCount() <= 10):
					self.Seed();
		self.Grow();
