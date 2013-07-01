from . import helper;
from ...defaultwesensource import DefaultWesenSource;

class WesenSource(DefaultWesenSource):

	def __init__(self, infoAllSource):
		"""Do all initialization stuff."""
		DefaultWesenSource.__init__(self, infoAllSource);
		self.minimumEnergyToEat = 0;
		self.minimumEnergyToReproduce = 500;
		self.minimumEnergyToFight = self.minimumEnergyToReproduce * 0.75;
		self.target = None;
		self.targetType = None;
		self.lookFunction = helper.lookForFoodTarget;
		self.forbiddenTargets = [];

	def __str__(self):
		return "<Nightwatch protects the city>";

	def main(self):
		"""reproduces as soon as an energy limit is reached,
		if it is low on energy,
		it looks for food,
		otherwise for enemies.
		If nothing is found, it scans the world."""
		while(self.time() >= self.infoTime["reproduce"]):
			helper.recoverAge(self);
			if(self.energy() > self.minimumEnergyToReproduce):
				self.Reproduce();
			lookRange = self.closerLook();
			if(not self.lookFunction(self, lookRange=lookRange)):
				helper.ScannerMove(self);
			helper.HandleTarget(self);
			if(not self.target):
				if(self.energy() < self.minimumEnergyToFight):
					self.lookFunction = helper.lookForFoodTarget;
				else:
					self.lookFunction = helper.lookForEnemyTarget;
