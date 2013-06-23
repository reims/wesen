"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

from ..strings import STRING_LOGGER;
from ..point import getZeroPosition, getNewPosition, positionToDirection;
from .base import WorldObject;
import sys;
import importlib;
from math import copysign

class Wesen(WorldObject):
	"""Wesen(infoObject) creates a new Wesen instance.
	infoObject is a Dictionary of Dictionaries, time,range,world,etc.
	"""

	# initialization

	def __init__(self, infoAllObject):
		"""imports the sourcecode of WesenSource and links the capabilities."""
		WorldObject.__init__(self, infoAllObject);
		self.infoTime = self.infoAllObject["time"];
		self.time = 0;
		self.source = self.infoObject["source"];
		WesenSource = self.getSource();
		infoSource = dict(source=self.source);
		infoSourceWorld = self.infoWorld.copy();
		del infoSourceWorld["objects"];
		del infoSourceWorld["AddObject"];
		del infoSourceWorld["DeleteObject"];
		infoAllSource = dict(world=infoSourceWorld, source=infoSource, time=self.infoTime, range=self.infoRange, wesen=self.infoObject, food=self.infoAllObject["food"]);
		self.wesenSource = WesenSource(infoAllSource);
		self.PutInterface(self.wesenSource);

	def getSource(self): #TODO this might import multiple times...?
		try:
			result = importlib.import_module("..sources."+self.source+".main", __package__).WesenSource;
		except ImportError as e:
			print(("%s could not been loaded:\n%s" % (self.source, e)));
			sys.exit();
		return result;

	def __repr__(self):
		return "<wesen id=%s pos=%s energy=%s source=%s %s>" % (id(self), self.position, self.energy,
                                                                        self.source, repr(self.wesenSource));

	def PutInterface(self, source):
		"""maps the source functions to the corresponding wesen functions."""
		source.id = self.getId;
		source.age = self.getAge;
		source.position = self.getPosition;
		source.energy = self.getEnergy;
		source.time = self.getTime;
		source.hasTime = self.hasTime;
		source.look = self.look;
		source.closerLook = self.closerLook;
		source.Move = self.Move;
		source.MoveToPosition = self.MoveToPosition;
		source.Talk = self.Talk;
		source.Eat = self.Eat;
		source.Reproduce = self.Reproduce;
		source.Attack = self.Attack;
		source.Vomit = self.Vomit;
		source.Donate = self.Donate;
		source.Broadcast = self.Broadcast;
		self.Receive = source.Receive;

	# small capabilites, no time cost

	def getTime(self): return self.time;

	def getEnergy(self): return self.energy;

	def getPosition(self): return self.position;

	def getId(self): return id(self);

	def getAge(self): return self.age;

	def hasTime(self, actions):
		"""hasTime(actions) returns True if there is enough time for all actions"""
		timeneed = 0;
		if(type(actions) != list):
			actions = [actions];
		for action in actions:
			timeneed += self.infoTime[action];
		return (self.time >= timeneed);

	# standard capabilities

	def look(self):
		"""returns a list of dictionaries with all visible WorldObjects position,
		objecttype and python id.
		"""
		lookRange = [];
		if(self.UseTime("look")):
			for object in self.getRange(self.infoRange["look"]):
				if(self != object):
					lookRange.append(dict(position=object.position, type=object.objectType, id=id(object)));
		return lookRange;

	def closerLook(self):
		"""returns look() and a few more information, as
		energy, age, time, source (which equals to friend/foe).
		"""
		closerLookRange = [];
		if(self.UseTime("closerlook")):
			for object in self.getRange(self.infoRange["closer_look"]):
				if(self != object):
					closerLookRange.append(dict(position=object.position, type=object.objectType,
                                                                    id=id(object), energy=object.energy, age=object.age));
					if(object.objectType == "wesen"):
						closerLookRange[-1]["time"] = object.time;
						closerLookRange[-1]["source"] = object.source;
		return closerLookRange;

	def Move(self, direction):
		"""moves the wesen into a specified direction"""
		real_direction = [min(int(c), int(copysign(int(self.getTime() / self.infoTime["move"]), c)), key=abs) for c in direction];
		if real_direction == getZeroPosition():
			return False;
		for i in range(abs(max(real_direction, key=abs))):
			self.UseTime("move");
		self.ChangePosition(getNewPosition(self.position, real_direction, self.infoWorld["length"]));
		return True;

	def MoveToPosition(self, position):
		"""moves the wesen to a specified position"""
		return self.Move(positionToDirection(self.position, position));

	def Talk(self, wesenid, message):
		"""calls Receive(message) in the wesen specified by wesenid when in range."""
		for object in self.getRange(self.infoRange["look"]):
			if((id(object) == wesenid) and (object.objectType == "wesen")):
				if(self.UseTime("talk")):
					object.wesenSource.Receive(message);
					return True;
		return False;

	def Eat(self, foodid):
		"""if it's at the same position, eat the food with python object id foodid."""
		for object in self.maxRange:
			if((id(object) == foodid) and (object.position == self.position) and
                           (object.objectType == "food")):
				if(self.UseTime("eat")):
					self.energy += object.getEaten();
					return True;
		return False;

	def Reproduce(self):
		"""Create a new Wesen instance with the same source and the specified energy
		which is then subtracted from the reproducing wesen.
		"""
		if(self.UseTime("reproduce")):
			childEnergy = int(self.energy / 2.0 + 0.5);
			infoWesen = self.infoObject.copy();
			infoWesen["energy"] = childEnergy;
			infoWesen["source"] = self.source;
			infoWesen["position"] = self.position;
			child = self.AddObject(infoWesen);
			child.RoundInit();
			self.maxRange.append(child);
			self.energy = childEnergy;
			self.age = 0;
			self.EnergyCheck();
			return id(child);
		return False;

	def Attack(self, wesenid):
		"""attacks the wesen specified by wesenid when it's at the same position.
		the energy of the enemy is subtracted from the own energy,
		so the one who had more energy than his enemy can survive.
		The other Wesen dies.
		"""
		for object in self.maxRange:
			if((object.objectType == "wesen") and (object != self) and
                           (object.position == self.position) and (id(object) == wesenid)):
				if(self.UseTime("attack")):
					self.energy -= int(object.getAttacked(self.energy)*0.5);
					return (not self.EnergyCheck());
		return False;

	def getAttacked(self, energy):
		"""called when this Wesen is attacked"""
		self.logger.info(STRING_LOGGER["DEATHWESEN"]["ATTACK"] % (repr(self), energy));
		previousEnergy = self.energy;
		self.energy -= int(energy*0.75);
		self.EnergyCheck();
		return previousEnergy;

	# advanced capabilites

	def Vomit(self, energy, deathOnLowEnergy=True):
		"""turns the given energy into static food (not growing, moving, seeding or anything like this).
		the energy is subtracted from the wesen"""
		if(self.UseTime("vomit")):
			if(energy > self.energy):
				energy = self.energy;
				if(deathOnLowEnergy):
					self.Die();
			if(not energy <= 0):
				#TODO the magic numbers here should be configurable
				infoFood = dict(energy=energy, position=self.position, growrate=2,
                                            seedrate=0.005, maxamount=energy+1000, maxage=1000, type="food");
				self.AddObject(infoFood);
				self.energy -= energy;
				return True;
		return False;

	def Donate(self, energy, wesenid):
		"""transfer energy from this wesen to another specified by wesenid"""
		for object in self.maxRange:
			if((id(object)==wesenid) and (object.objectType == "wesen") and
                           (object.position == self.position)):
				if(self.UseTime("donate")):
					if(energy > self.energy):
						energy = self.energy;
					if(not energy <= 0):
						object.energy += energy;
						self.energy -= energy;
						self.EnergyCheck();
						return True;
		return False;

	def Broadcast(self, message):
		"""calls Talk(message) with all wesen in range"""
		if(self.UseTime("broadcast")):
			for object in self.getRange(self.infoRange["talk"]):
				if(self != object):
					if(object.objectType == "wesen"):
						object.Receive(message);
			return True;
		return False;

	def Die(self):
		if(self.energy):
			self.Vomit(self.energy, deathOnLowEnergy=False);
		WorldObject.Die(self);

	# general methods

	def getDescriptor(self):
		"""returns a dictionary with descriptive information about the wesen for the GUI"""
		descriptor = dict(source=self.source, sourcedescriptor=self.wesenSource.getDescriptor());
		descriptor.update(WorldObject.getDescriptor(self));
		return descriptor;

	def UseTime(self, function):
		"""if the wesen has enough time,
		return true and subtract the time needed for function;
		else return false.
		"""
		usedTime = self.infoTime[function];
		if(self.time >= usedTime):
			self.time -= usedTime;
			return True;
		return False;

	def AgeCheck(self):
		"""kills the wesen if it's too old"""
		if(self.age > self.infoObject["maxage"]):
			self.logger.info(STRING_LOGGER["DEATHWESEN"]["AGE"] % (repr(self)));
			self.Die();

	def EnergyCheck(self):
		"""kills the Wesen when energy <= 0"""
		if(self.energy <= 0):
			self.logger.info(STRING_LOGGER["DEATHWESEN"]["ENERGY"] % (repr(self)));
			self.Die();
			return True;
		return False;

	def getMaxRange(self):
		"""returns the maximal reachable range in this turn"""
		return self.getRangeObject(self.worldObjects,
                                           (self.infoRange["look"] + (self.time / self.infoTime["move"])));

	def RoundInit(self):
		WorldObject.RoundInit(self);
		self.time += self.infoTime["init"];
		if(self.time > self.infoTime["max"]):
			self.time = self.infoTime["max"];

	def main(self):
		"""runs one turn of wesen code and it's AI code"""
		WorldObject.main(self);
		self.wesenSource.main();
		self.energy -= 1;
