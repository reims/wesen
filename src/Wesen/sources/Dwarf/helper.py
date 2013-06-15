from random import randint, uniform;

#TODO try to extract a sensible helper.py and move some of this back to the main source...

def DrunkenSailor(self):
	self.Move([randint(-1,1),randint(-1,1)]);

def recoverAge(self):
	if(self.age()+5 > self.infoWesen["maxage"]):
		child = self.Reproduce();
		self.Donate(self.energy(),child);

def CatchTarget(self, Action, actionTime):
	result = False;
	self.MoveToPosition(self.target["position"]);
	if(self.target["position"] == self.position() and self.time() >= actionTime):
		result = Action(self, self.target);
		if(not result):
			if(not self.target["id"] in self.forbiddenTargets):
				self.forbiddenTargets.append(self.target["id"]);
		self.target = None;
	return result;

def EatObject(self, object): #TODO one shouldn't use the variable name object anywhere ... :-(
	return self.Eat(object["id"]) or True;

def AttackObject(self, object):
	return self.Attack(object["id"]) or True;

def EatTarget(self):
	return CatchTarget(self, EatObject, self.infoTime["eat"]+1);

def AttackTarget(self):
	return CatchTarget(self, AttackObject, self.infoTime["attack"]+1);

def lookForTarget(self, lookRange, objectType, objectCondition, objectFitness):
	matchingObjects = [];
	for object in lookRange:
		if(object["type"] == objectType):
			if(objectCondition(self, object)):
				matchingObjects.append(object);
	if(matchingObjects):
		matchingObjects.sort(key = objectFitness);
		self.target = matchingObjects[0];
		self.targetType = objectType;
		return True;
	else:
		return False;

def acceptableFood(self, object):
	if(object["energy"] >= self.minimumEnergyToEat):
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

def lookAtGarden(self, lookRange=None):
	if(not lookRange):
		lookRange = self.closerLook();
	foodCount = 0;
	for o in lookRange:
		if(o["type"] == "food"):
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
