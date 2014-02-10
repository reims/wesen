"""Contains the Map, a visualization of all object's positions."""

import OpenGL;
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import GL_VERTEX_ARRAY, GL_COLOR_ARRAY, GL_TRIANGLES, \
    GL_DYNAMIC_DRAW, GL_ARRAY_BUFFER, GL_FLOAT, \
    glPushMatrix, glPopMatrix, glGetError, \
    glScale, glColor3f, glTranslatef, \
    glEnableClientState, glDisableClientState, \
    glVertexPointer, glColorPointer, glDrawArrays;
from .object import GuiObject;
from OpenGL.arrays import vbo;
from numpy import array as narray;
from numpy import empty as nempty;
from numpy import zeros as nzeros;
from functools import reduce;
from math import ceil,log;

class Map(GuiObject):
	"""A Map() object plots the descriptor data onto a 2d-grid."""

	def __init__(self, gui, infoWorld, sourceList, colorList):
		GuiObject.__init__(self, gui);
		self.worldLength = infoWorld["length"];
		self.colorDescriptor = {wesenSource:color
					for (wesenSource, color)
					in zip(sourceList, colorList)};
		self._indices = {};
		self._data = None;
		self._vbo = None;
		self._empty_indices = [];
		self._max_index = -1;
		self._data_size = -1;
		self._dirty_objects = {};

	def DrawMap(self, descriptor):
		"""Draws a map with all objects in the world,
		according to the descriptor."""
		#TODO move the frame mechanism to GuiObject!
		frame, col, plast, x, y = self._getFrameData();
		glTranslatef(frame, 2*frame, 0.0); # moving away from the frame
		blockSize = (1 - 2*frame) / self.worldLength;
		scaleFactor = blockSize;
		# data = narray(reduce(lambda a,b: a + b, 
		# 		     map(self._descToArray, 
		# 			 descriptor)), 
		# 	      "f");
		if len(descriptor) > 0:
			valuesPerObject = len(self._descToArray(descriptor[0]));
			if self._vbo is None:
				self._BuildData(descriptor);
			for _id,obj in self._dirty_objects.items():
				self._UpdateObject(_id, obj);
			self._dirty_objects = {};
			glTranslatef(frame, 2*frame, 0.0); # moving away from the frame
			glScale(scaleFactor, scaleFactor, 1.0);
			self._vbo.bind();
			self._vbo.copy_data();
			try:
				glEnableClientState(GL_VERTEX_ARRAY);
				glEnableClientState(GL_COLOR_ARRAY);
				#2 coordinates with 4 color values with 4 bytes each in between
				glVertexPointer(2, GL_FLOAT, 24, self._vbo);
				#4 color values with 2 coordinates with 4 bytes each in between
				glColorPointer(4, GL_FLOAT, 24, self._vbo+8);
				glDrawArrays(GL_TRIANGLES, 0, 3*2*(self._max_index + 1));
			finally:
				self._vbo.unbind();
				glDisableClientState(GL_VERTEX_ARRAY);
				glDisableClientState(GL_COLOR_ARRAY);

	def GetCallbacks(self):
		return {"UpdatePos":self._MarkDirty,
			"DeleteObject":self._DelObject,
			"AddObject":self._AddObject};

				
	def _BuildData(self, descriptor):
		"""Builds data array from scratch and creates VBO object"""
		if len(descriptor) == 0:
			return;
		num_objects = len(descriptor);
		values_per_object = len(self._descToArray(descriptor[0]));
		self._data_size = 2**ceil(log(num_objects, 2));
		self._data = nzeros(self._data_size*values_per_object, "f");
		self._indices = {};
		for i,obj in enumerate(descriptor):
			_id = obj["id"];
			values = self._descToArray(obj);
			for j,v in enumerate(values):
				self._data[i*values_per_object + j] = v;
			self._indices[_id] = i;
		self._empty_indices = [];
		self._max_index = num_objects - 1;
		self._vbo = vbo.VBO(self._data,
				    usage=GL_DYNAMIC_DRAW,
				    target=GL_ARRAY_BUFFER,
				    size=self._data_size*values_per_object*4);
		self._dirty_objects = {};

	def _AddObject(self, _id, obj):
		if self._vbo is None:
			return;
		index = -1;
		if len(self._empty_indices) > 0:
			index = self._empty_indices.pop();
		elif self._max_index < self._data_size-1:
			self._max_index += 1;
			index = self._max_index;
		if index > 0:
			values = self._descToArray(obj);
			num_values = len(values);
			self._vbo[index*num_values:(index+1)*num_values] = narray(values,"f");
			self._indices[_id] = index;
		else:
			self._vbo = None; # trigger _BuildData for next draw

	def _DelObject(self, _id):
		if self._vbo is None:
			return;
		index = self._indices[_id];
		num_values = type(self)._num_values;
		del self._indices[_id];
		if not (index == self._max_index):
			self._empty_indices.append(index);
		else:
			self._max_index -= 1;
		self._vbo[index*num_values:(index+1)*num_values] = nzeros(num_values, "f");

	def _UpdateObject(self, _id, obj):
		if self._vbo is None:
			return;
		index = self._indices.get(_id, -1);
		if index < 0: #have to check since object could have been deleted since marked as dirty
			return;
		num_values = type(self)._num_values;
		self._vbo[index*num_values:(index+1)*num_values] = narray(self._descToArray(obj), "f");

	def _MarkDirty(self, _id, obj):
		if self._vbo is None:
			return;
		self._dirty_objects[_id] = obj;

	_num_values = 6*(2+4);  #6 points with 2 coordinates and 4 color values


	def _descToArray(self,desc):
		"""returns list that contains the vertex and color data for one object"""
		color = (self.colorDescriptor[desc["source"]]               #color
			 if desc["type"] == "wesen"
			 else [0.0, 1.0, 0.0]);
		return ([desc["position"][0],     desc["position"][1]    , color[0], color[1], color[2], 1.0,     #first triangle
			 desc["position"][0],     desc["position"][1]-1.0, color[0], color[1], color[2], 1.0,
			 desc["position"][0]+1.0, desc["position"][1]    , color[0], color[1], color[2], 1.0,
			 desc["position"][0]+1.0, desc["position"][1]    , color[0], color[1], color[2], 1.0,    #second triangle
			 desc["position"][0],     desc["position"][1]-1.0, color[0], color[1], color[2], 1.0,
			 desc["position"][0]+1.0, desc["position"][1]-1.0, color[0], color[1], color[2], 1.0]);


	def Draw(self, descriptor):
		"""draws the map"""
		GuiObject.Draw(self);
		if(self.visible):
			self.DrawMap(descriptor);
