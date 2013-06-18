from . import helper;
from ...defaultwesensource import DefaultWesenSource;
from ...point import *;
from random import randint, uniform;
from sys import exit;

class WesenSource(DefaultWesenSource):

	globalScanVector = (uniform(-1,1),uniform(-1,1));

	def __init__(self, infoAllSource):
		"""Do all initialization stuff."""
		DefaultWesenSource.__init__(self, infoAllSource);
		self.infoAllSource = infoAllSource;
		self.active = True;
		self.minimalTime = 20; #TODO should be something to prevent infinite loops!!
		self.minimumEnergyToEat = 1;
		self.minimalGardenAge = 50;
		self.minimumEnergyToReproduce = 800;
		self.minimumEnergyToFight = self.minimumEnergyToReproduce * 0.9;
		self.target = None;
		self.targetType = None;
		self.forbiddenTargets = [];

	def main(self):
		# save age death and reproduce
		if(self.energy() > self.minimumEnergyToReproduce):
			self.Reproduce();
		helper.recoverAge(self);
		# action loop
		while((self.time() > self.minimalTime) and self.active):
			# try to finish something that already started:
			helper.HandleTarget(self);
			# nothing to do? OK, find something to do.
			if(not self.target):
				lookRange = self.closerLook();
				foundFood = helper.lookForFoodTarget(self, lookRange);
				if(foundFood):
					# fine, this will be handled next loop iteration!
					pass;
				else:
					# Mh, no food in sight; maybe move away?
					foundThreat = helper.lookForThreat(self, lookRange);
					if(foundThreat):
						helper.Flee(self);
					else:
						foundEnemy = False;
						if(self.energy() > self.minimumEnergyToFight):
							foundEnemy = helper.lookForEnemyTarget(self, lookRange);
							# if found, this will be handled next loop iteration!
						if(not foundEnemy):
							# nothing to eat, no fights. OK. Time for gardening.
							if(helper.lookAtYoungGarden(self, lookRange)):
								# well, wait for the garden to grow!
								self.target = None; #TODO find out whether necessary
								break;
							else:
								if(randint(0,1)==0): #TODO move magic number to constants above
									# seed out!
									helper.seedOut(self);
								else:
									# move away!
									helper.ScannerMove(self, scanVector=__class__.globalScanVector);
