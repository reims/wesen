"""This is a place to collect helpful functions,
which sometimes are more like methods,
such that the AI main method
contains more high-level strategy.

Beware: this code is likely to move somewhere else."""

from numpy.random import randint


def DrunkenSailor(self):
    self.Move([randint(-1, 1), randint(-1, 1)])


def recoverAge(self):
    if(self.age() + 5 > self.infoWesen["maxage"]):
        child = self.Reproduce()
        self.Donate(self.energy(), child)


def CatchTarget(self, Action, actionTime):
    targ = self.target
    if(self.MoveToPosition(targ["position"])):
        if(targ["position"] == self.position()
           and self.time() >= actionTime):
            self.target = None
            if(Action(self, targ)):
                return True
            elif(not targ["id"] in self.forbiddenTargets):
                self.forbiddenTargets.append(targ["id"])
    return False


def EatObject(self, o):
    return self.Eat(o["id"])


def AttackObject(self, o):
    return self.Attack(o["id"])


def EatTarget(self):
    return CatchTarget(self, EatObject, self.infoTime["eat"] + 1)


def AttackTarget(self):
    return CatchTarget(self, AttackObject, self.infoTime["attack"] + 1)


def lookForTarget(self, lookRange, objectType, objectCondition, objectFitness):
    matchingObjects = [o for o in lookRange
                       if (o["type"] == objectType
                           and objectCondition(self, o))]
    if(matchingObjects):
        if(self.target and
           self.targetType == objectType):
            for o in matchingObjects:
                if(o["id"] == self.target["id"]):
                    self.target = o
                    return True
        matchingObjects.sort(key=objectFitness)
        self.target = matchingObjects[0]
        self.targetType = objectType
        return True
    else:
        self.target = None
        self.targetType = None
        return False


def acceptableFood(self, o):
    if(o["energy"] >= self.minimumEnergyToEat):
        if(o["id"] in self.forbiddenTargets):
            del self.forbiddenTargets[self.forbiddenTargets.index(o["id"])]
        return True
    else:
        return False


def foodFitness(a):
    return a["energy"]


def acceptableEnemy(self, o):
    if(o["source"] != self.source):
        if(o["energy"] <= (self.energy() + self.minimumEnergyToFight)):
            return True
        else:
            self.minimumEnergyToFight = (self.energy()
                                         + self.minimumEnergyToFight
                                         + o["energy"]) // 2
            return False
    else:
        return False


def enemyFitness(a):
    return a["energy"]


def lookForFoodTarget(self, lookRange=None):
    if(not lookRange):
        lookRange = self.closerLook()
    return lookForTarget(self, lookRange, "food", acceptableFood, foodFitness)


def lookForEnemyTarget(self, lookRange=None):
    if(not lookRange):
        lookRange = self.closerLook()
    return lookForTarget(self, lookRange, "wesen", acceptableEnemy, enemyFitness)


def HandleTarget(self):
    if(self.target):
        if(self.targetType == "food"):
            return EatTarget(self)
        elif(self.targetType == "wesen"):
            return AttackTarget(self)
        else:
            return False
    else:
        return False


def ScannerMove(self):
    self.Move([2, int(randint(0, 3) / 2)])
