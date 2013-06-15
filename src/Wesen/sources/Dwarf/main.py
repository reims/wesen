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
		reprFactor = 1.2;
		self.minimalTime = 20; #TODO should be something to prevent infinite loops!!
		self.minimumEnergyToEat = 5; # not used
		self.minimumRoundsOfGardening = 3; # not used
		self.minimumEnergyToReproduce = 300 * reprFactor;
		self.minimumEnergyToFight = self.minimumEnergyToReproduce * 0.9;
		self.maximalNoFoodTimeUntilSeeding = 40; # not used
		self.lastTimeSeenFood = self.maximalNoFoodTimeUntilSeeding; # not used
		self.lastTimeSeeded = self.maximalNoFoodTimeUntilSeeding; # not used
		self.target = None;
		self.targetType = None;
		self.forbiddenTargets = []; # not used??

	def main(self):
		#TODO the damn thing doesn't eat up its own garden !!!
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
							if(helper.lookAtGarden(self, lookRange)):
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
