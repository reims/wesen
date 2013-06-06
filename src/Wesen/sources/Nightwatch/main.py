from Wesen.sources.Nightwatch import helper;
from Wesen.defaultwesensource import DefaultWesenSource;
from Wesen.point import *;
from random import randint;
from sys import exit;

class WesenSource(DefaultWesenSource):

	def __init__(self, infoAllSource):
		"""Do all initialization stuff."""
		DefaultWesenSource.__init__(self, infoAllSource);
		self.infoAllSource = infoAllSource;
		self.active = True;
		reprFactor = 0.9;
		self.minimumTime = 10;
		self.minimumEnergyToEat = 0;
		self.minimumEnergyToReproduce = 300 * reprFactor;
		#self.minimumEnergyToReproduce = (reprFactor * 2 * self.infoWesen["count"] *\
                #                                 self.infoWesen["energy"]) / self.infoFood["count"];
		self.minimumEnergyToFight = self.minimumEnergyToReproduce * 0.75;
		self.target = None;
		self.targetType = None;
		self.forbiddenTargets = [];

	def main(self):
		while(self.hasTime("reproduce") and self.active):
			if(self.energy() > self.minimumEnergyToReproduce):
				self.Reproduce();
			helper.recoverAge(self);
			helper.HandleTarget(self);
			if(not self.target):
				lookRange = self.closerLook();
				if(self.energy() < self.minimumEnergyToFight):
					lookFunction = helper.lookForFoodTarget;
				else:
					lookFunction = helper.lookForEnemyTarget;
				if(not lookFunction(self, lookRange=lookRange)):
					helper.ScannerMove(self);
