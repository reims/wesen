"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

from OpenGL.GL import *;
from OpenGL.GLU import *;
from OpenGL.GLUT import *;
from random import randint;
from Wesen.gui.object import GuiObject;
from Wesen.gui.text import TextPrinter;

PLOTMODE = GL_LINE_STRIP; # GL_LINES GL_POINTS GL_LINE_STRIP

class Graph(GuiObject):

	def __init__(self, gui, resolution=1000):
		GuiObject.__init__(self, gui);
		self.shadow = True;
		self.SetResolution(resolution);
		self.printer = TextPrinter();

	def Reshape(self, x, y):
		GuiObject.Reshape(self, x, y);
		self.SetResolution(self.width / 2.0);

	def SetResolution(self, resolution):
		self.resolution = float(resolution);
		self.histlength = int(self.resolution);

	def SetSensors(self, sensors):
		self.sensors = sensors;
		self.history = [[] for n in range(len(self.sensors))];

	def Step(self):
		for n in range(len(self.history)):
			self.history[n] += [self.sensors[n]["f"]()];

	def DrawPlot(self):
		for s in range(len(self.history)):
			c = self.sensors[s]["color"];
			glColor4f(c[0], c[1], c[2], 1.0);
			glBegin(PLOTMODE);
			for n in range(int(self.resolution)):
				try:
					y = self.history[s][-self.histlength:][n] / 100.0;
				except:
					pass;
				else:
					glVertex2f(n/self.resolution,y);
			glEnd();

	def DrawHint(self):
		p = self.printer;
		border = 24;
		for n in range(border):
			p.PrintLn();
		for s in self.sensors:
			p.PrintLn(p.fullString(s["colorname"],border)+" - "+s["name"]);
		p.ResetRaster();

	def Draw(self):
		GuiObject.Draw(self);
		if(self.visible):
			self.DrawHint();
			self.DrawPlot();

class SensorSystem(object):

	def __init__(self, gui, graph, world):
		self.gui = gui;
		self.world = world;
		graph.SetSensors(self.getSensors());

	def getSensors(self):
		sensors = [dict(f=self.getGlobalEnergy,color=[1.0,1.0,1.0],colorname="white",name="global energy"), \
			dict(f=self.getGlobalObjects,color=[0.5,0.5,0.5],colorname="grey",name="object count"), \
			dict(f=self.getFoodEnergy,color=[0.0,1.0,0.0],colorname="light green",name="food energy"), \
			dict(f=self.getFoodObjects,color=[0.0,0.5,0.0],colorname="dark green",name="food count"), \
			dict(f=self.getFps,color=[1.0,0.0,1.0],colorname="magenta",name="frames per second")];
		return sensors;

	def breakDown(self, value, base=100):
		return value / float(base);

	def getGlobalEnergy(self):
		return self.breakDown(self.world.getEnergy());

	def getGlobalObjects(self):
		return self.breakDown(len(self.world.objects), 1);

	def getFoodEnergy(self):
		return self.breakDown(self.world.stats["food"]["energy"]);

	def getFoodObjects(self):
		return self.breakDown(self.world.stats["food"]["count"], 1);

	def getFps(self):
		return self.breakDown(self.gui.fps, 1);
