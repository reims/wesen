from Wesen.defaultwesensource import DefaultWesenSource;

class WesenSource(DefaultWesenSource):
	"""this is a template to your own wesen sources."""

	def __init__(self, infoAllSource):
		"""Do all initialization stuff."""
		DefaultWesenSource.__init__(self, infoAllSource);

	def getDescriptor(self):
		descriptor = DefaultWesenSource.getDescriptor();
		return descriptor;

	def Receive(self, message):
		"""called when the wesen listens to a message.

		message should be a dictionary:
		{"extern":{},"intern":?}
		The "?" denotes that this is used for wesen-communication between friends,
		there is no unified protocol.

		not using the intern/extern-protocol is
		a violation to this games rules because it can cause other wesen to crash the whole game.
		"""
		pass;

	def main(self):
		"""A.I. code here, this method is run every time when
		the worlds main() command is used - every 'turn'.
		"""
		pass;














