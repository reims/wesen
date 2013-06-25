from numpy.random import randint, uniform;

#TODO try to extract a sensible helper.py and move some of this back to the main source...

def DrunkenSailor(self):
	self.Move([randint(-1,1),randint(-1,1)]);

def recoverAge(self):
	if(self.age()+5 > self.infoWesen["maxage"]):
		child = self.Reproduce();
		self.Donate(self.energy(),child);

def CatchTarget(self, Action, actionTime):
	if(self.MoveToPosition(self.target["position"])):
		if(self.target["position"] == self.position() and self.time() >= actionTime):
			if(Action(self, self.target)):
				return True; 
			elif(not self.target["id"] in self.forbiddenTargets):
				self.forbiddenTargets.append(self.target["id"]);
			self.target = None;
	return False;

def EatObject(self, o):
	return self.Eat(o["id"]);

def AttackObject(self, o):
	return self.Attack(o["id"]);

def EatTarget(self):
	return CatchTarget(self, EatObject, self.infoTime["eat"]+1);

def AttackTarget(self):
	return CatchTarget(self, AttackObject, self.infoTime["attack"]+1);

def lookForTarget(self, lookRange, objectType, objectCondition, objectFitness):
	matchingObjects = [o for o in lookRange if (o["type"]==objectType and objectCondition(self, o))];
	if(matchingObjects):
		#matchingObjects.sort(key = objectFitness);
		self.target = matchingObjects[randint(len(matchingObjects))];
		self.targetType = objectType;
		return True;
	else:
		return False;

def acceptableFood(self, object):
	if(object["age"] >= self.minimalGardenAge):
		if(object["id"] in self.forbiddenTargets):
			del self.forbiddenTargets[self.forbiddenTargets.index(object["id"])];
		return True;
	else:
		return False;

def foodFitness(a):
        return a["energy"]

def acceptableEnemy(self, object):
	if(object["source"] != self.source):
		if(object["energy"] <= (self.energy() + self.minimumEnergyToFight)):
			return True;
		else:
			self.minimumEnergyToFight = int(((self.energy() + self.minimumEnergyToFight) + object["energy"]) / 2); #TODO improve magic 
			return False;
	else:
		return False;

def threateningEnemy(self, object):
	if(object["source"] == self.source):
		return False;
	else:
		return object["energy"] > self.energy()*1.2; #TODO remove magic

def enemyFitness(a):
	return a["energy"]

def lookForFoodTarget(self, lookRange=None):
	if(not lookRange):
		lookRange = self.closerLook();
	return lookForTarget(self, lookRange, "food", acceptableFood, foodFitness);

def lookForEnemyTarget(self, lookRange=None):
	if(not lookRange):
		lookRange = self.closerLook();
	return lookForTarget(self, lookRange, "wesen", acceptableEnemy, enemyFitness);

def lookForThreat(self, lookRange=None):
	if(not lookRange):
		lookRange = self.closerLook();
	return lookForTarget(self, lookRange, "wesen", threateningEnemy, enemyFitness);

def lookAtYoungGarden(self, lookRange=None):
	if(not lookRange):
		lookRange = self.closerLook();
	foodCount = 0;
	for o in lookRange:
		if(o["type"] == "food" and o["age"] <= self.minimalGardenAge):
			foodCount += 1;
	return (foodCount > 10); #TODO magic number

def HandleTarget(self):
	if(self.target):
		if(self.targetType == "food"):
			return EatTarget(self);
		elif(self.targetType == "wesen"):
			return AttackTarget(self);
		else:
			return False;
	else:
		return False;

def ScannerMove(self, scanVector=(1,0), scanSpeed=3, randomization=0.2):
	self.Move([int(randomization*uniform(-1,1)+scanSpeed*coordinate) for coordinate in scanVector]);

def Flee(self):
	ScannerMove(self,scanVector=[-4*c for c in self.target["position"]]);

def seedOut(self):
	newFoodObjects = [];
	for i in range(0,3):
		newFoodObjects.append(self.Vomit(1));
		for j in range(0,4):
			DrunkenSailor(self);
	return newFoodObjects;
