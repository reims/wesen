from . import helper;
from ...defaultwesensource import DefaultWesenSource;
from ...point import *;
from random import randint;
from sys import exit;
from math import cos, sin, pi, atan2;

class WesenSource(DefaultWesenSource):

	def __init__(self, infoAllSource):
		"""Do all initialization stuff."""
		DefaultWesenSource.__init__(self, infoAllSource);
		self.infoAllSource = infoAllSource;
		self.active = True;
		reprFactor = 0.9;
		self.minimumTime = 10;
		self.minimumEnergyToEat = 0;
		self.minimumEnergyToReproduce = 300 * reprFactor;
		#self.minimumEnergyToReproduce = (reprFactor * 2 * self.infoWesen["count"] *\
		#				  self.infoWesen["energy"]) / self.infoFood["count"];
		self.minimumEnergyToFight = self.minimumEnergyToReproduce * 0.75;
		self.target = None;
		self.targetType = None;
		self.forbiddenTargets = [];
		self.angle = 0.0;
		self.first_move = True;
		self.mid_point = [0,0];

	def main(self):
		r = 50;
		if self.first_move:
			self.mid_point = [int(self.position()[0] + r) % self.infoAllSource["world"]["length"],
					  self.position()[1]];
			self.first_move = False;
		range = self.look();
		delta_angle = 2*pi/200;
		while self.hasTime("move"):
			move_pos = [int(self.mid_point[0] + r*cos(self.angle)) % self.infoAllSource["world"]["length"], 
				    int(self.mid_point[1] + r*sin(self.angle)) % self.infoAllSource["world"]["length"]];
			old_pos = self.position();
			self.MoveToPosition(move_pos);
			if self.position() == old_pos:
				break;
			radius = getShortestTranslation(self.mid_point, self.position(), self.infoAllSource["world"]["length"]);
			self.angle = atan2(radius[1], radius[0])+delta_angle;
			print("main:", move_pos, old_pos, self.angle, self.mid_point, radius);			

