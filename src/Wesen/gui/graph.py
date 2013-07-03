"""Contains 2 classes:
Graph and _SensorData.
Graph plots several curves,
_SensorData plots a single curve."""

from numpy import array as narray;
from OpenGL.GL import GL_VERTEX_ARRAY, GL_LINE_STRIP, \
    GL_STREAM_DRAW, GL_ARRAY_BUFFER, GL_FLOAT, \
    glPushMatrix, glPopMatrix, \
    glScalef, glColor3f, glTranslatef, \
    glEnableClientState, glDisableClientState, \
    glVertexPointer, glDrawArrays;
from OpenGL.arrays import vbo;
from .object import GuiObject;
from .text import TextPrinter;

SENSORFCT_FROMSTATS_ENERGY = lambda world : lambda x : world.stats[x]["energy"];

class Graph(GuiObject):
	"""A Graph object plots curves for sensors.
	See AddSensor().
	Currently, there are some default sensors."""

	def __init__(self, gui, world, sourceList, colorList):
		GuiObject.__init__(self, gui);
		self.world = world;
		self.shadow = True;
		self.maxValue = 20000; # used to compute y axis scaling
		self.sensors = [];
		self.history = [];
		# both sensors and history are set in AddSensor.
		self.printer = TextPrinter();
		self.resolution = 400;
		self._AddDefaultSensors();
		self._AddObjectEnergySensors(sourceList, colorList);

	def _AddDefaultSensors(self):
		"""adds sensors: (global energy, food energy)"""
		self.AddSensor({"f":SENSORFCT_FROMSTATS_ENERGY,
				 "statskey":"global",
				 "color":[0.5,0.5,0.5],
				 "name":"global energy"});
		self.AddSensor({"f":SENSORFCT_FROMSTATS_ENERGY,
				 "statskey":"food",
				 "color":[0.0,1.0,0.0],
				 "name":"food energy"});

	def _AddObjectEnergySensors(self, sourceList, colorList):
		"""adds a sensor for each source's energy."""
		for (wesenSource, color) in zip(sourceList, colorList):
			self.AddSensor({"f":SENSORFCT_FROMSTATS_ENERGY,
					"color":color,
					"statskey":wesenSource,
					"name":wesenSource+" energy"});

	def Reshape(self, x, y):
		GuiObject.Reshape(self, x, y);
		self.printer.Reshape(x, y);

	def AddSensor(self, newSensor):
		"""AddSensor(newSensor) should be called only
		during initialization, as it erases history.
		newSensor = {f=lambda world : lambda statskey : int,
				statskey=None,
				color=[0.0,1.0,0.0],
				name="some value"}"""
		self.sensors.append(newSensor);
		self.history = [_SensorData(self.resolution) for _ in self.sensors];

	def Step(self):
		"""adds current world.stats as data point to all sensors."""
		for sensorInfo, data in zip(self.sensors, self.history):
			data.AddValue(sensorInfo["f"]\
					      (self.world)\
					      (sensorInfo["statskey"]));
		self.maxValue = max(self.maxValue,
				    max(data.maxValue
					for data in self.history));

	def DrawPlot(self):
		"""Plots the curves for all sensors in self.sensors"""
		glPushMatrix();
		#TODO the following is "moving away from frame",
		# and should use the framedata (plastic, etc.)
		# from the GuiObject base class.
		# Probably this stuff should be done in GuiObject!
		glTranslatef(0.005, 0.01, 0.0);
		glScalef(0.99/self.resolution, 0.7/self.maxValue, 1.0);
		for sensorInfo, data in zip(self.sensors, self.history):
			glColor3f(*(sensorInfo["color"]));
			data.Draw();
		glPopMatrix();

	def DrawHint(self):
		"""Prints a caption for the plot"""
		p = self.printer;
		p.ResetRaster();
		for sensorInfo in self.sensors:
			glColor3f(*sensorInfo["color"]);
			# to make the color effective for text,
			# we have to call glRasterPos by printing a linebreak:
			p.Print("\n");
			p.Print("  %s" % (sensorInfo["name"]));

	def Draw(self):
		GuiObject.Draw(self);
		if(self.visible):
			self.DrawHint();
			self.DrawPlot();

class _SensorData(object):
	"""A _SensorData object holds the data
	for a single sensor, including previous data.
	It can draw itself via Draw()
	and you can update it via AddValue()"""

	def __init__(self, size):
		self.size = size;
		initialBuffer = [];
		for x, y in enumerate(range(size)):
			initialBuffer.append(x);
			initialBuffer.append(y);
		self.buf = narray(initialBuffer, 'f');
		self.vbo = vbo.VBO(self.buf, 
				   usage = GL_STREAM_DRAW,
				   target = GL_ARRAY_BUFFER,
				   size = 4*2*size);
		self.previous_index = -1;
		self.buffer_full = False;
		self.maxValue = 0;

	def AddValue(self, value):
		"""supply one more numerical value"""
		if(self.previous_index == self.size - 1
		   and not(self.buffer_full)):
			self.buffer_full = True;
		self.previous_index = (self.previous_index +1) % self.size;
		self.buf[self.previous_index*2+1] = value;
		self.vbo[self.previous_index*2+1
			 :self.previous_index*2+2] = narray([value],'f');
		self.maxValue = max(self.maxValue, value);

	def Draw(self):
		"""draw a curve of all previous data,
		up to a certain point (self.resolution)"""
		self.vbo.bind();
		self.vbo.copy_data();
		glEnableClientState(GL_VERTEX_ARRAY);
		glVertexPointer(2, GL_FLOAT, 0, self.vbo);
		if self.buffer_full:
			if self.previous_index != self.size -1:
				glPushMatrix();
				glTranslatef(-1* (self.previous_index+1), 0.0, 0.0);
				glDrawArrays(GL_LINE_STRIP, 
					     (self.previous_index+1),
					     (self.size - self.previous_index -1));
				glPopMatrix();
			glPushMatrix();
			glTranslatef(self.size - self.previous_index - 1, 0.0, 0.0);
			glDrawArrays(GL_LINE_STRIP, 0,
				     (self.previous_index +1));
			glPopMatrix();
		else:
			glDrawArrays(GL_LINE_STRIP, 0,
				     (self.previous_index +1));
		glDisableClientState(GL_VERTEX_ARRAY);
		self.vbo.unbind();
