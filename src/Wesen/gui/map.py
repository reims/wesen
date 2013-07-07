"""Contains the Map, a visualization of all object's positions."""

from OpenGL.GL import glTranslatef, glScale, \
    glColor3f, glRectf;
from .object import GuiObject;

class Map(GuiObject):
	"""A Map() object plots the descriptor data onto a 2d-grid."""

	def __init__(self, gui, infoWorld, sourceList, colorList):
		GuiObject.__init__(self, gui);
		self.worldLength = infoWorld["length"];
		self.colorDescriptor = {wesenSource:color
					for (wesenSource, color)
					in zip(sourceList, colorList)};

	def Draw(self, descriptor):
		"""Draws a map with all objects in the world,
		according to the descriptor."""
		GuiObject.Draw(self);
		#TODO move the frame mechanism to GuiObject!
		frame, col, plast, x, y = self._getFrameData();
		glTranslatef(frame, 2*frame, 0.0); # moving away from the frame
		blockSize = (1 - 2*frame) / self.worldLength;
		scaleFactor = blockSize;
		glScale(scaleFactor, scaleFactor, 1.0);
		for desc in descriptor:
			#TODO treating wesen and food so different is bad,
			#     and creates awkward code like this everywhere:
			color = (self.colorDescriptor[desc["source"]]
				 if desc["type"] == "wesen"
				 else [0.0, 1.0, 0.0]);
			glColor3f(*color);
			glRectf(desc["position"][0],     desc["position"][1],
				desc["position"][0]+1.0, desc["position"][1]-1.0);
