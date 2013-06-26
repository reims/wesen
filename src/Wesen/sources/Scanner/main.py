"""
the scanner is a simple wesen, running over the screen like a scanner, eating and reproducing.
"""

from ...defaultwesensource import DefaultWesenSource;

class WesenSource(DefaultWesenSource):

	def __init__(self, infoAllSource):
		"""Do all initialization stuff."""
		DefaultWesenSource.__init__(self, infoAllSource);
		self.movecount = 0;
		self.reproductionEnergy = 500;

	def __str__(self):
		return "<Ordinary Scanner>";

	def Scanner(self):
		for o in self.look():
			if(o["type"] == "food"
			   and o["position"] == self.position()):
				self.Eat(o["id"]);
		if(self.movecount >= self.worldlength):
			self.Move([1,1]);
			self.movecount = 1;
		else:
			self.Move([1,0]);
			self.movecount += 1;

	def main(self):
		while(self.time() > self.infoTime["move"]):
			if(self.energy() >= self.reproductionEnergy):
				self.Reproduce();
			self.Scanner();
