"""defines an interface for AI code"""

class DefaultWesenSource(object):
	"""each AI code should subclass this class."""

	def __init__(self, infoAllSource):
		"""links a few variables to infoAllSource contents."""
		self.infoSource = infoAllSource["source"];
		self.infoWesen = infoAllSource["wesen"];
		self.infoFood = infoAllSource["food"];
		self.infoWorld = infoAllSource["world"];
		self.infoTime = infoAllSource["time"];
		self.infoRange = infoAllSource["range"];
		self.worldlength = self.infoWorld["length"];
		self.Debug = self.infoWorld["Debug"];
		self.logger = self.infoWorld["logger"];
		self.source = self.infoSource["source"];

	def getDescriptor(self):
		"""currently unused, designed for debugging"""
		return {};

	def Receive(self, message):
		"""message should be a dict"""
		pass;

	def main(self):
		"""called every turn"""
		pass;
