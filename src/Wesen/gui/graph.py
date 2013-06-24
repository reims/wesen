"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

from numpy import array as narray;
from OpenGL.GL import *;
from OpenGL.GLU import *;
from OpenGL.GLUT import *;
from OpenGL.arrays import vbo;
from random import randint;
from .object import GuiObject;
from .text import TextPrinter;
from functools import reduce;

PLOTMODE = GL_LINE_STRIP; # GL_LINES GL_POINTS GL_LINE_STRIP
import traceback;

class Graph(GuiObject):

	def __init__(self, gui, world, resolution=1000):
		GuiObject.__init__(self, gui);
		self.world = world;
		self.shadow = True;
		self.maxValue = 1000; # used to compute y axis scaling
		self.SetResolution(resolution);
		self.printer = TextPrinter();

	def Reshape(self, x, y):
		GuiObject.Reshape(self, x, y);
		self.SetResolution(self.width / 2.0);

	def SetResolution(self, resolution):
		#print("Graph resolution:", resolution);
		self.resolution = float(resolution);
		self.histlength = int(self.resolution);

	def SetSensors(self, sensors):
		self.sensors = sensors;
		self.history = [SensorData(self.histlength) for n in range(len(self.sensors))];

	def AddSensor(self, sensor):
		""" sensor = dict(f=self.getFoodEnergy,color=[0.0,1.0,0.0],colorname="light green",name="food energy")
		where f has to be a function which takes a variable self and expects there to be self.world."""
		self.sensors.append(sensor);
		self.history = [SensorData(self.histlength) for n in range(len(self.sensors))];

	def Step(self):
		for n in range(len(self.history)):
			self.history[n].AddValue(self.sensors[n]["f"](self.world));
		self.maxValue=max([sensor.maxValue for sensor in self.history]+[self.maxValue]);

	def DrawPlot(self):
		glPushMatrix();
		glScalef(1.0/self.resolution, 0.8/self.maxValue, 1.0);
		for i,data in enumerate(self.history):
			c = self.sensors[i]["color"];
			glColor4f(c[0], c[1], c[2], 1.0);
			data.Draw();
		glPopMatrix();

	def DrawHint(self):
		glPushMatrix();
		glTranslatef(0.0, 1.55, 0.0);
		p = self.printer;
		border = 24;
		for n in range(border):
			p.PrintLn();
		for s in self.sensors:
			p.PrintLn(p.fullString(s["colorname"],border)+" - "+s["name"]);
		p.ResetRaster();
		glPopMatrix();

	def Draw(self):
		GuiObject.Draw(self);
		if(self.visible):
			self.DrawHint();
			self.DrawPlot();

class SensorData(object):
	def __init__(self, size):
		self.size = size;
		self.buf = narray(reduce(lambda x,y: x +y, [[i,0.0] for i in range(size)]), 'f');
		self.vbo = vbo.VBO(self.buf, 
				   usage = GL_STREAM_DRAW,
				   target = GL_ARRAY_BUFFER,
				   size = 4*2*size);
		self.previous_index = -1;
		self.buffer_full = False;
		self.maxValue = 0;

	def AddValue(self, value):
		if self.previous_index == self.size - 1 and not(self.buffer_full):
			self.buffer_full = True;
		self.previous_index = (self.previous_index +1) % self.size;
		self.buf[self.previous_index*2+1] = value;
		self.vbo[self.previous_index*2+1:self.previous_index*2+2] = narray([value],'f');
		self.maxValue = max(self.maxValue, value);

	def Draw(self):
		self.vbo.bind();
		self.vbo.copy_data();
		try:
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
		except Exception:
			print(traceback.format_exc());
		finally:
			glDisableClientState(GL_VERTEX_ARRAY);
			self.vbo.unbind();

class SensorSystem(object):

	def __init__(self, gui, graph, world):
		self.gui = gui;
		self.world = world;
		graph.SetSensors(self.getSensors());

	def getSensors(self):
		sensors = [\
			   dict(f=lambda world : world.getEnergy(),color=[0.5,0.5,0.5],colorname="grey",name="global energy"), \
			   ];
		return sensors;
