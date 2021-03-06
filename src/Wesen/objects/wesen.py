"""The class for all data and operations a single Wesen has"""

from .base import WorldObject
import importlib


class RuleException(Exception):

    """This exception is thrown whenever a wesen source
    violates the rules of the game."""

    def __init__(self, ruleDescription):
        super(RuleException, self).__init__(ruleDescription)


class Wesen(WorldObject):

    """Wesen(infoObject) creates a new Wesen instance.
    infoObject is a Dictionary of Dictionaries, time,range,world,etc.
    """

    # initialization

    def __init__(self, infoAllObject):
        """imports the sourcecode of WesenSource and links the capabilities."""
        WorldObject.__init__(self, infoAllObject)
        self.infoTime = infoAllObject["time"]
        self.source = self.infoObject["source"]
        # TODO one can probably avoid multiple imports (if not already)
        WesenSource = importlib.import_module("..sources."
                                              + self.source
                                              + ".main",
                                              __package__).WesenSource
        infoSource = {"source": self.source}
        infoSourceWorld = self.infoWorld.copy()
        del infoSourceWorld["objects"]
        del infoSourceWorld["AddObject"]
        del infoSourceWorld["DeleteObject"]
        infoAllSource = {"world": infoSourceWorld, "source": infoSource,
                         "time": self.infoTime, "range": self.infoRange,
                         "wesen": self.infoObject, "food": infoAllObject["food"]}
        self.wesenSource = WesenSource(infoAllSource)
        self.Receive = None
        self.PutInterface(self.wesenSource)

    def __repr__(self):
        return ("<wesen id=%s pos=%s energy=%s source=%s>" %
                (id(self), self.position, self.energy, str(self.wesenSource)))

    def PutInterface(self, source):
        """maps the source functions to the corresponding wesen functions."""
        source.id = self.getId
        source.age = self.getAge
        source.position = self.getPosition
        source.energy = self.getEnergy
        source.time = self.getTime
        source.look = self.look
        source.closerLook = self.closerLook
        source.Move = self.Move
        source.MoveToPosition = self.MoveToPosition
        source.Talk = self.Talk
        source.Eat = self.Eat
        source.Reproduce = self.Reproduce
        source.Attack = self.Attack
        source.Vomit = self.Vomit
        source.Donate = self.Donate
        source.Broadcast = self.Broadcast
        self.Receive = source.Receive

    # small capabilites, no time cost

    def getTime(self):
        """returns time left to do stuff (for free)"""
        return self.time

    def getEnergy(self):
        """returns energy left (for free)"""
        return self.energy

    def getPosition(self):
        """returns own position (for free)"""
        return self.position

    def getId(self):
        """returns own object id (for free)"""
        return id(self)

    def getAge(self):
        """returns own age (for free)"""
        return self.age

    # standard capabilities

    def look(self):
        """returns a list of dictionaries with all visible WorldObjects position,
        objecttype and python id.
        """
        if(self._UseTime("look")):
            return [{"position": o.position, "type": o.objectType, "id": oid}
                    for oid, o in self.getRangeIterator(
                        self.infoRange["look"],
                        condition=lambda x: self != x)]
        else:
            return []

    def closerLook(self):
        """returns look() and a few more information, as
        energy, age, time, source (which equals to friend/foe).
        """
        if(self._UseTime("closerlook")):
            return [{"position": o.position, "type": o.objectType,
                     "id": oid, "energy": o.energy,
                     "age": o.age, "time": o.time,
                     "source": o.source}
                    for oid, o in self.getRangeIterator(
                        self.infoRange["closer_look"],
                        condition=lambda x: self != x)]
        else:
            return []

    def Move(self, direction):
        """moves the wesen into a specified direction,
        returns true if any position change happened."""
        if(self.dead):
            return False
        direction = [int(dc) for dc in direction]
        # the following code is a more time-efficient way to do
        #usedTime = self.infoTime["move"]*(abs(direction[0])+abs(direction[1]));
        if(direction[0] < 0):
            if(direction[1] < 0):
                usedTime = (self.infoTime["move"]
                            * -1 * (direction[0] + direction[1]))
            elif(direction[1] > 0):
                usedTime = (self.infoTime["move"]
                            * (direction[1] - direction[0]))
            else:
                usedTime = (self.infoTime["move"]
                            * -1 * direction[0])
        elif(direction[0] > 0):
            if(direction[1] < 0):
                usedTime = (self.infoTime["move"]
                            * (direction[0] - direction[1]))
            elif(direction[1] > 0):
                usedTime = (self.infoTime["move"]
                            * (direction[1] + direction[0]))
            else:
                usedTime = (self.infoTime["move"]
                            * direction[0])
        else:
            if(direction[1] < 0):
                usedTime = (self.infoTime["move"]
                            * -1 * direction[1])
            elif(direction[1] > 0):
                usedTime = (self.infoTime["move"]
                            * direction[1])
            else:
                return False
        if(self.time >= usedTime):
            self.time -= usedTime
            oldPos = self.position
            self.position = [(pc + dc) % self.infoWorld["length"]
                             for (pc, dc) in zip(self.position, direction)]
            self.UpdatePos(id(self), oldPos, self.getDescriptor())
            return True
        else:
            return False

    def MoveToPosition(self, newPosition):
        """moves the wesen to a specified position"""
        newPosition = [int(pc) for pc in newPosition]
        while(self.position != newPosition):
            if not self.Move([-1 if nc < pc else 1 if nc > pc else 0
                              for (nc, pc) in zip(newPosition, self.position)]):
                return False
        return True

    def Talk(self, wesenid, message):
        """calls Receive(message) in the wesen specified by wesenid when in range."""
        if(self._UseTime("talk")):
            for oid, o in self.getRangeIterator(
                    self.infoRange["look"],
                    condition=lambda x: ((oid == wesenid) and
                                         (o.objectType == "wesen"))):
                o.wesenSource.Receive(message)
                return True
        return False

    def Eat(self, foodid):
        """if it's at the same position, eat the food with python object id foodid."""
        if(self.dead):
            return False
        if not foodid in self.worldObjects:
            raise RuleException("Tried to eat non-existing food")
        o = self.worldObjects[foodid]
        if((o.position == self.position) and
           (o.objectType == "food")):
            if(self._UseTime("eat")):
                self.energy += o.getEaten()
                return True
        else:
            if(o.position != self.position):
                raise RuleException(
                    "In order to eat something, one has to be at the same position. Keep in mind that wesen move and you have to look where they are each turn, as the information from looking around becomes stale quickly!")
            if(o.objectType != "food"):
                raise RuleException(
                    "In order to eat something, it has to be food.")
        return False

    def Reproduce(self):
        """Create a new Wesen instance with the same source and the specified energy
        which is then subtracted from the reproducing wesen.
        """
        if(self.dead):
            return False
        if(self._UseTime("reproduce")):
            childEnergy = self.energy // 2
            infoWesen = self.infoObject.copy()
            infoWesen["energy"] = childEnergy
            infoWesen["source"] = self.source
            infoWesen["position"] = self.position
            child = self.AddObject(infoWesen)
            self.energy -= childEnergy
            self.age = 0
            self._EnergyCheck()
            return id(child)
        return False

    def Attack(self, wesenid):
        """attacks the wesen specified by wesenid when it's at the same position.
        the energy of the enemy is subtracted from the own energy,
        so the one who had more energy than his enemy can survive.
        The other Wesen dies.
        """
        if(self.dead):
            return False
        try:
            o = self.worldObjects[wesenid]
        except KeyError:
            raise RuleException(
                "May not attack non-existent enemy with id '%s'" % (wesenid))
        if((o.objectType == "wesen") and
           (o.position == self.position)):
            if(self._UseTime("attack")):
                self.energy -= int(o.getAttacked(self.energy) * 0.5)
                return (not self._EnergyCheck())
        return False

    def getAttacked(self, energy):
        """called when this Wesen is attacked"""
        previousEnergy = self.energy
        self.energy -= int(energy * 0.75)
        self._EnergyCheck()
        return previousEnergy

    # advanced capabilites

    def Vomit(self, energy, deathOnLowEnergy=True):
        """turns the given energy into strange food
        (other growing and seeding behaviour).
        the energy is subtracted from the wesen"""
        if(self.dead):
            return False
        if(self._UseTime("vomit")):
            if(energy > self.energy):
                energy = self.energy
                if(deathOnLowEnergy):
                    self.Die()
            if(not energy <= 0):
                # TODO the magic numbers here should be configurable
                infoFood = {"energy": energy, "position": self.position,
                            "growrate": 1, "seedrate": 0.001,
                            "maxamount": energy + 1000, "maxage": 1000,
                            "type": "food"}
                self.AddObject(infoFood)
                self.energy -= energy
                return True
        return False

    def Donate(self, energy, wesenid):
        """transfer energy from this wesen to another specified by wesenid"""
        if(self.dead):
            return False
        o = self.worldObjects[wesenid]
        if((o.objectType == "wesen") and
           (o.position == self.position)):
            if(self._UseTime("donate")):
                if(energy > self.energy):
                    energy = self.energy
                if(not energy <= 0):
                    o.energy += energy
                    self.energy -= energy
                    self._EnergyCheck()
                    return True
        return False

    def Broadcast(self, message):
        """calls Talk(message) with all wesen in range"""
        if(self.dead):
            return False
        if(self._UseTime("broadcast")):
            for _, o in self.getRangeIterator(
                    self.infoRange["talk"],
                    condition=lambda x: (self != x and
                                         x.objectType == "wesen")):
                o.Receive(message)
            return True
        return False

    def Die(self):
        if(self.energy):
            self.Vomit(self.energy, deathOnLowEnergy=False)
        WorldObject.Die(self)

    # general methods

    def getDescriptor(self):
        """returns a dictionary
        with descriptive information about the wesen for the GUI"""
        descriptor = {"source": self.source,
                      "sourcedescriptor": self.wesenSource.getDescriptor()}
        descriptor.update(WorldObject.getDescriptor(self))
        return descriptor

    def persist(self):
        """returns JSON serializable object with all information
        needed to restore the state of the object"""
        d = WorldObject.persist(self)
        d.update({"wesensource": self.wesenSource.persist(),
                  "maxage": self.infoObject["maxage"]})
        return d

    def restore(self, obj):
        """restores the state of the wesen object"""
        WorldObject.restore(self, obj)
        self.wesenSource.restore(obj)

    def _UseTime(self, function):
        """if the wesen has enough time,
        return true and subtract the time needed for function;
        else return false.
        """
        usedTime = self.infoTime[function]
        if(self.time >= usedTime):
            self.time -= usedTime
            return True
        return False

    def _AgeCheck(self):
        """kills the wesen if it's too old"""
        WorldObject._AgeCheck(self)
        if(self.age > self.infoObject["maxage"]):
            self.Die()

    def _EnergyCheck(self):
        """kills the Wesen when energy <= 0"""
        WorldObject._EnergyCheck(self)
        if(self.energy <= 0):
            self.Die()
            return True
        return False

    def main(self):
        """runs one turn of wesen code and it's AI code"""
        WorldObject.main(self)
        if(not self.dead):
            self.energy -= 1
            self.time = min(
                self.time + self.infoTime["init"], self.infoTime["max"])
            self.wesenSource.main()
