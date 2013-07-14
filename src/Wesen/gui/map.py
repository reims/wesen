"""Contains the Map, a visualization of all object's positions."""

from OpenGL.GL import GL_VERTEX_ARRAY, GL_COLOR_ARRAY, GL_TRIANGLES, \
    GL_STATIC_DRAW, GL_ARRAY_BUFFER, GL_FLOAT, \
    glPushMatrix, glPopMatrix, \
    glScale, glColor3f, glTranslatef, \
    glEnableClientState, glDisableClientState, \
    glVertexPointer, glColorPointer, glDrawArrays;
from .object import GuiObject;
from OpenGL.arrays import vbo;
from numpy import array as narray;
from functools import reduce;

class Map(GuiObject):
	"""A Map() object plots the descriptor data onto a 2d-grid."""

	def __init__(self, gui, infoWorld, sourceList, colorList):
		GuiObject.__init__(self, gui);
		self.worldLength = infoWorld["length"];
		self.colorDescriptor = {wesenSource:color
					for (wesenSource, color)
					in zip(sourceList, colorList)};

	def DrawMap(self):
		"""Draws a map with all objects in the world,
		according to the descriptor."""
		#TODO move the frame mechanism to GuiObject!
		frame, col, plast, x, y = self._getFrameData();
		glTranslatef(frame, 2*frame, 0.0); # moving away from the frame
		blockSize = (1 - 2*frame) / self.worldLength;
		scaleFactor = blockSize;
		glScale(scaleFactor, scaleFactor, 1.0);
		data = narray(reduce(lambda a,b: a + b, 
				     map(lambda d: self._descToArray(d), 
					 self.descriptor)), 
			      "f");
		_vbo = vbo.VBO(data,
			       usage=GL_STATIC_DRAW);
			       #size=4*6*5*len(self.descriptor)); #6 points with 5 values with 4 bytes
		_vbo.bind();
		try:
			glEnableClientState(GL_VERTEX_ARRAY);
			glEnableClientState(GL_COLOR_ARRAY);
			#2 dim points with 3 color values 4 bytes each in between
			glVertexPointer(2, GL_FLOAT, 20, _vbo);
			#3 color values with 2 coordinates 4 bytes each in between
			glColorPointer(3, GL_FLOAT, 20, _vbo+8); 
			glDrawArrays(GL_TRIANGLES,0,3*2*len(self.descriptor));
		finally:
			_vbo.unbind();
			glDisableClientState(GL_VERTEX_ARRAY);
			glDisableClientState(GL_COLOR_ARRAY);

	def _descToArray(self,desc):
		"""returns list that contains the vertex and color data for one object"""
		color = (self.colorDescriptor[desc["source"]]               #color
			 if desc["type"] == "wesen"
			 else [0.0, 1.0, 0.0]);
		return ([desc["position"][0],     desc["position"][1]    ]+color+     #first triangle
			[desc["position"][0],     desc["position"][1]-1.0]+color+
			[desc["position"][0]+1.0, desc["position"][1]    ]+color+
			[desc["position"][0]+1.0, desc["position"][1]    ]+color+     #second triangle
			[desc["position"][0],     desc["position"][1]-1.0]+color+
			[desc["position"][0]+1.0, desc["position"][1]-1.0]+color);


	def Draw(self):
		"""draws the map"""
		GuiObject.Draw(self);
		if(self.visible):
			self.DrawMap();
