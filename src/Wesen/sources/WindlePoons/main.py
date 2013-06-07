from ...defaultwesensource import DefaultWesenSource;
from ...point import *;
from random import randint;
from sys import exit;

class WesenSource(DefaultWesenSource):

	def __init__(self, infoAllSource):
		"""Do all initialization stuff."""
		DefaultWesenSource.__init__(self, infoAllSource);
		self.infoAllSource = infoAllSource;
		self.active = True;
		self.normal = True;

	def main(self):
		while(self.time() >= 20 and self.active):
			if(self.normal and self.position() != [5,5]):
				self.MoveToPosition([5,5]);
			else:
				lookRange = self.closerLook();
				for object in lookRange:
					pass;
				self.normal = False;
