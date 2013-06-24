from . import helper;
from ...defaultwesensource import DefaultWesenSource;
from ...point import *;
from numpy.random import randint, uniform;
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
		self.minimalGardenAge = 15;
		self.minimumEnergyToReproduce = 1800;
		self.minimumEnergyToFight = 300;
		self.target = None;
		self.targetType = None;
		self.forbiddenTargets = [];

	def main(self):
		# save age death and reproduce
		if(self.energy() > self.minimumEnergyToReproduce):
			self.Reproduce();
		helper.recoverAge(self);
		lookRange = self.closerLook(); # could be done in-loop...
		# action loop
		while((self.time() > self.minimalTime) and self.active):
			# try to finish something that already started:
			helper.HandleTarget(self);
			# nothing to do? OK, find something to do.
			if(not self.target):
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
								decision = randint(0,9);
								if(decision==0): #TODO move magic number to constants above
									# seed out!
									helper.seedOut(self);
								elif(decision <= 5):
									# move away!
									helper.ScannerMove(self, scanVector=__class__.globalScanVector);
								else:
									# move back!
									helper.ScannerMove(self, scanVector=[-c for c in __class__.globalScanVector]);
