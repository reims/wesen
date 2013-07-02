from OpenGL.GL import *;
#from OpenGL.GLUT import *;
from .object import GuiObject;

class Map(GuiObject):
	"""used to draw a map of all objects"""

	def __init__(self, gui, infoWorld, sourceList, colorList):
		GuiObject.__init__(self, gui);
		self.infoWorld = infoWorld;
		colorDescriptor = {};
		for (wesenSource,color) in zip(sourceList, colorList):
			colorDescriptor[wesenSource] = color;
		self.colorDescriptor = colorDescriptor;

	def DrawMap(self):
                frame, col, plast, x, y = self._getFrameData();
                glTranslatef(frame, 2*frame, 0.0); # moving away from the frame
                length = float(self.infoWorld["length"]);
                blockSize = (1.0 - 2*frame) / length;
                scaleFactor = blockSize;
                glScale(scaleFactor, scaleFactor, 1.0);
                for desc in self.descriptor:
                        color = self.colorDescriptor[desc["source"]] if desc["type"] == "wesen" else [0.0, 1.0, 0.0];
                        glColor3f(*color);
                        glRectf(desc["position"][0], desc["position"][1], desc["position"][0]+1.0, desc["position"][1]-1.0);

	def Draw(self):
		"""draws the map"""
		GuiObject.Draw(self);
		if(self.visible):
			self.DrawMap();
