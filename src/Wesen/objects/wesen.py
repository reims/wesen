"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

from ..strings import STRING_LOGGER;
from .base import WorldObject;
import sys;
import importlib;

class RuleException(Exception):
	def __init__(self, ruleDescription):
		super(RuleException, self).__init__(ruleDescription);

class Wesen(WorldObject):
	"""Wesen(infoObject) creates a new Wesen instance.
	infoObject is a Dictionary of Dictionaries, time,range,world,etc.
	"""

	# initialization

	def __init__(self, infoAllObject):
		"""imports the sourcecode of WesenSource and links the capabilities."""
		WorldObject.__init__(self, infoAllObject);
		self.infoTime = self.infoAllObject["time"];
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
		result = importlib.import_module("..sources."+self.source+".main", __package__).WesenSource;
		return result;

	def __repr__(self):
		return "<wesen id=%s pos=%s energy=%s source=%s>" % (self.id, self.position, self.energy, str(self.wesenSource));

	def PutInterface(self, source):
		"""maps the source functions to the corresponding wesen functions."""
		source.id = self.getId;
		source.age = self.getAge;
		source.position = self.getPosition;
		source.energy = self.getEnergy;
		source.time = self.getTime;
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

	def getId(self): return self.id;

	def getAge(self): return self.age;

	# standard capabilities

	def look(self):
		"""returns a list of dictionaries with all visible WorldObjects position,
		objecttype and python id.
		"""
		if(self.UseTime("look")):
			return [dict(position=o.position, type=o.objectType, id=o.id)
				for o in self.getRangeObjectWithCondition(self.maxRange, self.infoRange["look"], condition = lambda x : self != x).values()];
		else:
			return [];

	def closerLook(self):
		"""returns look() and a few more information, as
		energy, age, time, source (which equals to friend/foe).
		"""
		if(self.UseTime("closerlook")):
			return [dict(position=o.position, type=o.objectType, id=o.id,
				     energy=o.energy, age=o.age, time=o.time, source=o.source)
				for o in self.getRangeObjectWithCondition(self.maxRange, self.infoRange["closer_look"], condition = lambda x : self != x).values()];
		else:
			return [];

	def Move(self, direction):
		"""moves the wesen into a specified direction, returns true if any position change happened."""
		direction = [int(dc) for dc in direction];
		# the following code is a more time-efficient way to do
		#usedTime = self.infoTime["move"]*(abs(direction[0])+abs(direction[1]));
		if(direction[0] < 0):
			if(direction[1] < 0):
				usedTime = (self.infoTime["move"]
					    * -1 * (direction[0] + direction[1]));
			elif(direction[1] > 0):
				usedTime = (self.infoTime["move"]
					    * (direction[1] - direction[0]));
			else:
				usedTime = (self.infoTime["move"]
					    * -1 * direction[0]);
		elif(direction[0] > 0):
			if(direction[1] < 0):
				usedTime = (self.infoTime["move"]
					    * (direction[0] - direction[1]));
			elif(direction[1] > 0):
				usedTime = (self.infoTime["move"]
					    * (direction[1] + direction[0]));
			else:
				usedTime = (self.infoTime["move"]
					    * direction[0]);
		else:
			if(direction[1] < 0):
				usedTime = (self.infoTime["move"]
					    * -1 * direction[1]);
			elif(direction[1] > 0):
				usedTime = (self.infoTime["move"]
					    * direction[1]);
			else:
				return False;
		if(self.time >= usedTime):
			self.time -= usedTime;
			self.position =  [(pc+dc) % self.infoWorld["length"] for (pc,dc) in zip(self.position,direction)]
			return True;
		else:
			return False;

	def MoveToPosition(self, newPosition):
		"""moves the wesen to a specified position"""
		newPosition = [int(pc) for pc in newPosition];
		while(self.position != newPosition):
			if not self.Move([-1 if nc < pc else 1 if nc > pc else 0
					   for (nc,pc) in zip(newPosition, self.position)]):
				return False;
		return True;

	def Talk(self, wesenid, message):
		"""calls Receive(message) in the wesen specified by wesenid when in range."""
		if(self.UseTime("talk")):
			for o in self.getRangeObjectWithCondition(self.maxRange, self.infoRange["look"], condition = lambda x : ((o.id == wesenid) and (o.objectType == "wesen"))):
				object.wesenSource.Receive(message);
				return True;
		return False;

	def Eat(self, foodid):
		"""if it's at the same position, eat the food with python object id foodid."""
		if(foodid in self.maxRange.keys()):
			o = self.maxRange[foodid];
#		for o in self.maxRange.values():
			if((o.position == self.position) and
#			   (o.id == foodid) and 
			   (o.objectType == "food")):
				if(self.UseTime("eat")):
					self.energy += o.getEaten();
					return True;
			else:
				if(o.position != self.position):
					raise RuleException("In order to eat something, one has to be at the same position. Keep in mind that wesen move and you have to look where they are each turn, as the information from looking around becomes stale quickly!");
				if(o.objectType != "food"):
					raise RuleException("In order to eat something, it has to be food.");
		return False;

	def Reproduce(self):
		"""Create a new Wesen instance with the same source and the specified energy
		which is then subtracted from the reproducing wesen.
		"""
		if(self.UseTime("reproduce")):
			childEnergy = int(self.energy / 2);
			infoWesen = self.infoObject.copy();
			infoWesen["energy"] = childEnergy;
			infoWesen["source"] = self.source;
			infoWesen["position"] = self.position;
			child = self.AddObject(infoWesen);
			self.maxRange[child.id] = child;
			self.energy -= childEnergy;
			self.age = 0;
			self.EnergyCheck();
			return child.id;
		return False;

	def Attack(self, wesenid):
		"""attacks the wesen specified by wesenid when it's at the same position.
		the energy of the enemy is subtracted from the own energy,
		so the one who had more energy than his enemy can survive.
		The other Wesen dies.
		"""
		if(wesenid in self.maxRange.keys()):
			o = self.maxRange[wesenid];
			if((o.objectType == "wesen") and
			   (o.position == self.position)):
				if(self.UseTime("attack")):
					self.energy -= int(o.getAttacked(self.energy)*0.5);
					return (not self.EnergyCheck());
#		for o in self.maxRange:
#			if(o.id == wesenid):
#				if((o.objectType == "wesen") and (o.position == self.position)):
#					if(self.UseTime("attack")):
#						self.energy -= int(o.getAttacked(self.energy)*0.5);
#						return (not self.EnergyCheck());
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
		if(wesenid in self.maxRange.keys()):
			o = self.maxRange[wesenid];
#		for o in self.maxRange:
			if((o.objectType == "wesen") and
#			   (o.id==wesenid) and
                           (o.position == self.position)):
				if(self.UseTime("donate")):
					if(energy > self.energy):
						energy = self.energy;
					if(not energy <= 0):
						o.energy += energy;
						self.energy -= energy;
						self.EnergyCheck();
						return True;
		return False;

	def Broadcast(self, message):
		"""calls Talk(message) with all wesen in range"""
		if(self.UseTime("broadcast")):
			for o in self.getRangeObjectWithCondition(self.maxRange, self.infoRange["talk"], condition = lambda x : self != x and x.objectType == "wesen"):
				o.Receive(message);
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

	def main(self):
		"""runs one turn of wesen code and it's AI code"""
		WorldObject.main(self);
		self.energy -= 1;
		self.time = min(self.time + self.infoTime["init"], self.infoTime["max"]);
		self.maxRange = self.getRangeObject(self.worldObjects,
						    (self.infoRange["look"]
						     + (self.time / self.infoTime["move"])));
		self.wesenSource.main();
