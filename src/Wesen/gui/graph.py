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

	def __init__(self, gui, world, sourceList, colorList, resolution=1000):
		GuiObject.__init__(self, gui);
		self.world = world;
		self.sourceList = sourceList;
		self.colorList = colorList;
		self.shadow = True;
		self.maxValue = 1000; # used to compute y axis scaling
		self.SetResolution(resolution);
		self.sensors = [];
		self.printer = TextPrinter();
		self._AddDefaultSensors();
		self._AddObjectEnergySensors();

	def _AddDefaultSensors(self):
		"""currently: (global energy, food energy)"""
		self.AddSensor({"f":SENSORFCT_FROMSTATS_ENERGY,
				 "statskey":"global",
				 "color":[0.5,0.5,0.5],
				 "name":"global energy"});
		self.AddSensor({"f":SENSORFCT_FROMSTATS_ENERGY,
				 "statskey":"food",
				 "color":[0.0,1.0,0.0],
				 "name":"food energy"});

	def _AddObjectEnergySensors(self):
		for (wesenSource, color) in zip(self.sourceList, self.colorList):
			self.AddSensor({"f":SENSORFCT_FROMSTATS_ENERGY,
					"color":color,
					"statskey":wesenSource,
					"name":wesenSource+" energy"});

	def Reshape(self, x, y):
		GuiObject.Reshape(self, x, y);
		self.printer.Reshape(x, y);
		self.SetResolution(self.width / 2.0);

	def SetResolution(self, resolution):
		self.resolution = float(resolution);
		self.histlength = int(self.resolution);

	def SetSensors(self, sensors):
		self.sensors = sensors;
		self.history = [SensorData(self.histlength) for _ in self.sensors];

	def AddSensor(self, newSensor):
		"""newSensor = {f=lambda world : lambda statskey : int,
				statskey=None,
				color=[0.0,1.0,0.0],
				name="food energy"}"""
		self.sensors.append(newSensor);
		self.history = [SensorData(self.histlength) for _ in self.sensors];

	def Step(self):
		for sensorInfo, data in zip(self.sensors, self.history):
			data.AddValue(sensorInfo["f"]\
					      (self.world)\
					      (sensorInfo["statskey"]));
		self.maxValue = max([data.maxValue for data in self.history]
				    + [self.maxValue]);

	def DrawPlot(self):
		glPushMatrix();
		glScalef(1.0/self.resolution, 0.8/self.maxValue, 1.0);
		for sensorInfo, data in zip(self.sensors, self.history):
			glColor3f(*(sensorInfo["color"]));
			data.Draw();
		glPopMatrix();

	def DrawHint(self):
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

class SensorData(object):
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
		if(self.previous_index == self.size - 1
		   and not(self.buffer_full)):
			self.buffer_full = True;
		self.previous_index = (self.previous_index +1) % self.size;
		self.buf[self.previous_index*2+1] = value;
		self.vbo[self.previous_index*2+1:self.previous_index*2+2] = narray([value],'f');
		self.maxValue = max(self.maxValue, value);

	def Draw(self):
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
			glDrawArrays(GL_LINE_STRIP,
				     0,
				     (self.previous_index +1));
			glPopMatrix();
		else:
			glDrawArrays(GL_LINE_STRIP,
				     0,
				     (self.previous_index +1));
		glDisableClientState(GL_VERTEX_ARRAY);
		self.vbo.unbind();
