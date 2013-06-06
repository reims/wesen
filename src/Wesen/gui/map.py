from OpenGL.GL import *;
from OpenGL.GLU import *;
from OpenGL.GLUT import *;
import math;
from numpy import array as numericArray;
from Wesen.gui.object import GuiObject;

class Map(GuiObject):
	"""used to draw a map of all objects"""

	def __init__(self, gui, infoWorld, colorDescriptor):
		GuiObject.__init__(self, gui);
		self.infoWorld = infoWorld;
		self.colorDescriptor = colorDescriptor;
		self.NewArray();

	def Step(self):
		if(self.active):
			self.NewArray();
			self.FillArray();

	def NewArray(self):
		self.array = numericArray([[Field([], self.colorDescriptor) for i in range(self.infoWorld["length"])]
                                           for i in range(self.infoWorld["length"])]);

	def FillArray(self):
		for descriptor in self.descriptor[1]:
			try:
				self.array[descriptor["position"][0], descriptor["position"][1]].descriptorList.append(descriptor);
			except:
				raise "GuiError: descriptor does not fit array: %s" % descriptor;

	def DrawMap(self):
		length = float(self.infoWorld["length"]);
		blockSize = 1.0 / length;
		scaleFactor = blockSize;
		glScale(scaleFactor, scaleFactor, 1.0);
		for x in range(len(self.array)):
			for y in range(len(self.array[0])):
				self.array[x,y].Draw();
				glTranslatef(0.0, 1.0, 0.0);
			glTranslatef(1.0, -length, 0.0);

	def Draw(self):
		"""draws the map"""
		GuiObject.Draw(self);
		if(self.visible):
			self.DrawMap();

class Field(object):

	def __init__(self, descriptorList, colorDescriptor):
		object.__init__(self);
		self.descriptorList = descriptorList;
		self.colorDescriptor = colorDescriptor;

	def _SetColor(self):
		color = [0.0, 0.0, 0.0];
		for descriptor in self.descriptorList:
			objectType = descriptor["type"];
			if(objectType == "wesen"):
				sourceCode = descriptor["source"][:3];
				color = [(color[i] + self.colorDescriptor[descriptor["source"]][i]) for i in range(3)];
			elif(objectType == "food"):
				color[1] += 1.0;
		count = len(self.descriptorList);
		color = [colorindex / count for colorindex in color]
		self.color = color;

	def _DrawDefinition(self):
		glColor4f(self.color[0], self.color[1], self.color[2], 1.0);
		glRectf(0.0, 0.0, 1.0, -1.0);

	def Draw(self):
		if(self.descriptorList):
			self._SetColor();
			self._DrawDefinition();
