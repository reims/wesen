"""
the drunken sailor is a simple implementation of random movement.
"""

from Wesen.defaultwesensource import DefaultWesenSource;
from random import choice;

class WesenSource(DefaultWesenSource):

	def __init__(self, infoAllSource):
		"""Do all initialization stuff."""
		DefaultWesenSource.__init__(self, infoAllSource);
		self.randRange = [-1,0,1];

	def main(self):
		while(self.time() > self.infoTime["move"]):
			self.Move([choice(self.randRange),choice(self.randRange)]);
