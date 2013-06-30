from ...defaultwesensource import DefaultWesenSource;

class WesenSource(DefaultWesenSource):

	def __init__(self, infoAllSource):
		"""Do all initialization stuff."""
		DefaultWesenSource.__init__(self, infoAllSource);
		self.infoAllSource = infoAllSource;
		self.normal = True;

	def main(self):
		while(self.time() >= 20):
			if(self.normal and self.position() != [5,5]):
				self.MoveToPosition([5,5]);
			else:
				lookRange = self.closerLook();
				for o in lookRange:
					if(o["type"] == "food"):
						if(self.MoveToPosition(o["position"])):
							self.Eat(o["id"]);
				self.normal = False;
