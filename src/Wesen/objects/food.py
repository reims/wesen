"""The Food class, which is present in every simulation."""

from .base import WorldObject
from ..point import getRandomPositionInRadius
from numpy.random import uniform


class Food(WorldObject):

    """unlike wesen, who are programmable and capable of intelligence,
    food can only grow every turn and reproduce over distance.
    """

    def __init__(self, infoAllWorld):
        WorldObject.__init__(self, infoAllWorld)
        self.source = "food"
        self.seedrate = self.infoObject["seedrate"]
        self.growrate = self.infoObject["growrate"]
        self.rangeseed = self.infoRange["seed"]
        self.maxamount = self.infoObject["maxamount"]
        self.maxage = self.infoObject["maxage"]

    def __repr__(self):
        return ("<food id=%s growrate=%s pos=%s energy=%s>" %
                (id(self), self.growrate, self.position, self.energy))

    def getDescriptor(self):
        """currently doing nothing than returning the WorldObjects getDescriptor."""
        return WorldObject.getDescriptor(self)

    def persist(self):
        """returns JSON serializable object with all information
        needed to restore the state of the object"""
        d = WorldObject.persist(self)
        d.update({"seedrate": self.seedrate,
                  "growrate": self.growrate,
                  "rangeseed": self.rangeseed,
                  "maxamount": self.maxamount,
                  "maxage": self.maxage})
        return d

    def restore(self, obj):
        """restores the state of the food object"""
        WorldObject.restore(self, obj)
        self.seedrate = obj["seedrate"]
        self.growrate = obj["growrate"]
        self.rangeseed = obj["rangeseed"]
        self.maxamount = obj["maxamount"]
        self.maxage = obj["maxage"]

    def getEaten(self):
        """dies and returns previous energy amount.
        """
        energy = self.energy
        if(not self.dead):
            self.Die()
        return energy

    def Grow(self):
        """increment energy by some amount."""
        self.energy += int(uniform(0, 2) * self.growrate)

    def Seed(self):
        """create a new Food instance in seedrange."""
        infoFood = self.infoObject
        infoFood["energy"] = 1
        infoFood["position"] = getRandomPositionInRadius(self.position,
                                                         self.rangeseed,
                                                         self.infoWorld["length"])
        return self.AddObject(infoFood)

    def _AgeCheck(self):
        WorldObject._AgeCheck(self)
        if(self.age >= self.infoObject["maxage"]):
            self.Die()

    def _EnergyCheck(self):
        WorldObject._EnergyCheck(self)
        if(self.energy >= self.infoObject["maxamount"]):
            self.energy = self.infoObject["maxamount"]
        elif(self.energy < 0):
            self.energy = 0
            # this happens only if one manipulates food via the GUI
            # TODO the GUI should be more careful and this raise an Error.
            print("warning: food energy lower than zero detected")

    def _hasTooMuchFoodNearby(self):
        """return True as soon as there is a lot of food nearby."""
        for i, _ in enumerate(self.getRangeIterator(self.rangeseed,
                                                    condition=lambda o: o.objectType == b"food")):
            if(i == 10):  # TODO make this number configurable!
                return True
        return False

    def main(self):
        """randomly grow or seed, based on growrate and seedrate.
        When too old, die."""
        WorldObject.main(self)
        # handles age and low-energy death
        if(not self.dead):
            if(self.age > 10):  # TODO numbers should be a config option
                if(uniform(0, 1) < self.seedrate):
                    if(not self._hasTooMuchFoodNearby()):
                        self.Seed()
            self.Grow()
