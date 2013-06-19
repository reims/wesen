from OpenGL.GL import *;
from OpenGL.GLU import *;
from OpenGL.GLUT import *;
import math;
from numpy import array as numericArray;
from .object import GuiObject;

class Map(GuiObject):
	"""used to draw a map of all objects"""

	def __init__(self, gui, infoWorld, colorDescriptor):
		GuiObject.__init__(self, gui);
		self.infoWorld = infoWorld;
		self.colorDescriptor = colorDescriptor;

	def DrawMap(self):
                frame, col, plast, x, y = self._getFrameData();
                glTranslatef(frame, 2*frame, 0.0); # moving away from the frame
                length = float(self.infoWorld["length"]);
                blockSize = (1.0 - 2*frame) / length;
                scaleFactor = blockSize;
                glScale(scaleFactor, scaleFactor, 1.0);
                for desc in self.descriptor[1]:
                        color = self.colorDescriptor[desc["source"]] if desc["type"] == "wesen" else [0.0, 1.0, 0.0];
                        glColor4f(color[0], color[1], color[2], 1.0);
                        glRectf(desc["position"][0], desc["position"][1], desc["position"][0]+1.0, desc["position"][1]-1.0);

	def Draw(self):
		"""draws the map"""
		GuiObject.Draw(self);
		if(self.visible):
			self.DrawMap();
