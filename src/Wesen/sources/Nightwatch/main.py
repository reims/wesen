from . import helper;
from ...defaultwesensource import DefaultWesenSource;

class WesenSource(DefaultWesenSource):

	def __init__(self, infoAllSource):
		"""Do all initialization stuff."""
		DefaultWesenSource.__init__(self, infoAllSource);
		self.infoAllSource = infoAllSource;
		self.minimumEnergyToEat = 0;
		self.minimumEnergyToReproduce = 300;
		self.minimumEnergyToFight = self.minimumEnergyToReproduce * 0.75;
		self.target = None;
		self.targetType = None;
		self.forbiddenTargets = [];

	def main(self):
		while(self.time() >= self.infoTime["reproduce"]):
			helper.recoverAge(self);
			if(self.energy() > self.minimumEnergyToReproduce):
				self.Reproduce();
			helper.HandleTarget(self);
			if(not self.target):
				lookRange = self.closerLook();
				if(self.energy() < self.minimumEnergyToFight):
					lookFunction = helper.lookForFoodTarget;
				else:
					lookFunction = helper.lookForEnemyTarget;
				if(not lookFunction(self, lookRange=lookRange)):
					helper.ScannerMove(self);
