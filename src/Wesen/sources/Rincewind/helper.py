from random import randint


def DrunkenSailor(self):
    self.Move([randint(-1, 1), randint(-1, 1)])


def recoverAge(self):
    if(self.age() + 5 > self.infoWesen["maxage"]):
        child = self.Reproduce()
        self.Donate(self.energy(), child)


def CatchTarget(self, Action, actionTime):
    result = False
    self.MoveToPosition(self.target["position"])
    if(self.target["position"] == self.position() and self.time() >= actionTime):
        result = Action(self, self.target)
        if(not result):
            if(not self.target["id"] in self.forbiddenTargets):
                self.forbiddenTargets.append(self.target["id"])
        self.target = None
    return result


def EatObject(self, object):
    return self.Eat(object["id"]) or True


def AttackObject(self, object):
    return self.Attack(object["id"]) or True


def EatTarget(self):
    return CatchTarget(self, EatObject, self.infoTime["attack"] + 1)


def AttackTarget(self):
    return CatchTarget(self, AttackObject, self.infoTime["eat"] + 1)


def lookForTarget(self, lookRange, objectType, objectCondition, objectFitness):
    matchingObjects = []
    for object in lookRange:
        if(object["type"] == objectType):
            if(objectCondition(self, object)):
                matchingObjects.append(object)
    if(matchingObjects):
        matchingObjects.sort(key=objectFitness)
        self.target = matchingObjects[0]
        self.targetType = objectType
        return True
    else:
        return False


def acceptableFood(self, object):
    if(object["energy"] >= self.minimumEnergyToEat):
        if(object["id"] in self.forbiddenTargets):
            del self.forbiddenTargets[
                self.forbiddenTargets.index(object["id"])]
        return True
    else:
        return False


def foodFitness(a):
    return a["energy"]


def acceptableEnemy(self, object):
    if(object["source"] != self.source):
        if(object["energy"] <= (self.energy() + self.minimumEnergyToFight)):
            return True
        else:
            self.minimumEnergyToFight = int(
                ((self.energy() + self.minimumEnergyToFight) + object["energy"]) / 2)
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
    return self.Move([2, int(randint(0, 3) / 2)])
