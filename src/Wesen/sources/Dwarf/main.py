from . import helper;
from ...defaultwesensource import DefaultWesenSource;
from numpy.random import randint, uniform;

class WesenSource(DefaultWesenSource):

	globalScanVector = (uniform(-1,1),uniform(-1,1));

	def __init__(self, infoAllSource):
		"""Do all initialization stuff."""
		DefaultWesenSource.__init__(self, infoAllSource);
		self.infoAllSource = infoAllSource;
		self.minimalTime = 20; #TODO should be something to prevent infinite loops!!
		self.minimumEnergyToEat = 1;
		self.minimalGardenAge = 15;
		self.minimumEnergyToReproduce = 1600;
		self.minimumEnergyToFight = 300;
		self.target = None;
		self.targetType = None;
		self.forbiddenTargets = [];

	def __str__(self):
		return "<Dwarf Fighter, coming out of the Broken Drum>";

	def main(self):
		# save age death and reproduce
		if(self.energy() > self.minimumEnergyToReproduce):
			self.Reproduce();
			for i in range(6):
				helper.ScannerMove(self, scanVector=[__class__.globalScanVector[1],__class__.globalScanVector[0]]);
		helper.recoverAge(self);
		lookRange = self.closerLook(); # could be done in-loop...
		# action loop
		while(self.time() > self.minimalTime):
			# try to finish something that already started:
			if(self.targetType == "food"):
				helper.lookForFoodTarget(self, lookRange);
			elif(self.targetType == "wesen"):
				helper.lookForEnemyTarget(self, lookRange);
			#TODO the 4 lines above this comment are wrong.
			helper.HandleTarget(self);
			# nothing to do? OK, find something to do.
			if(not self.target):
				foundFood = helper.lookForFoodTarget(self, lookRange);
				if(foundFood):
					# fine, this will be handled next loop iteration!
					pass;
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
