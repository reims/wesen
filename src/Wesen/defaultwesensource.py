"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

class DefaultWesenSource(object):
	"""default sourcecode for a wesen,
	newly created wesen should be created with
	class WesenSource(DefaultWesenSource):
	to ensure it gets a working interface.
	"""

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
		return dict();

	def Receive(self, message):
		pass;

	def main(self):
		pass;
