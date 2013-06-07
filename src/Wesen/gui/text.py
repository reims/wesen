from OpenGL.GL import *;
from OpenGL.GLU import *;
from OpenGL.GLUT import *;
import math;
from random import randint; # funny stuff, can be deleted!!
from ..objects.wesen import Wesen;
from .object import GuiObject;

color3white = [1,1,1];
color3grey = [0.9,0.9,0.9];
color3hacker = [0.2,0.9,0.2];
color3freak = [0.9,0.95,0.9];
colorset = color3freak;

class Text(GuiObject):

	def __init__(self, gui, descriptor, world, infoWorld):
		GuiObject.__init__(self, gui);
		self.SetDescriptor(descriptor);
		self.world = world;
		self.infoWorld = infoWorld;
		self.printer = TextPrinter();

	def Step(self):
		self.printer.ResetRaster();

	def Reshape(self, x, y):
		GuiObject.Reshape(self, x, y);
		self.printer.Reshape(x,y);

	def DrawFieldStats(self, p):
		fieldInformation = self.gui.fieldInformation;
		if(not fieldInformation):
			return;
		p.PrintLn("Field %s information:" % (fieldInformation[0]["position"]));
		for element in fieldInformation:
			if(element["type"] == "food"):
				p.PrintLn("Food(%s): %s years old" % (p.fullString(element["energy"],6), p.fullString(element["age"],4)));
			elif(element["type"] == "wesen"):
				p.PrintLines("%s(%s): %s years old - %s" % (element["source"], element["energy"], element["age"], element["sourcedescriptor"]));

	def DrawGameStats(self, p):
		p.PrintLn("        global | %s e | %s o |" % (p.fullString(self.world.energy,5), p.fullString(len(self.world.objects),3)));
		for source in list(self.world.stats.keys()):
			energy = self.world.stats[source]["energy"];
			count = self.world.stats[source]["count"];
			try:
				perWesen = int(energy / count);
			except ZeroDivisionError:
				perWesen = 0;
			p.PrintLn("%s | %s e | %s o | %s e/o |" % (p.fullString(source,14), p.fullString(energy,5),\
							      p.fullString(count,3), p.fullString(perWesen,4)));
		if(self.world.winner):
			p.PrintLn("\nWinner: %s" % (self.world.winner));
		else:
			p.PrintLn();

	def DrawEngineStats(self, p):
		if(self.gui.pause):
			status = "paused";
		else:
			status = "running";
		if(self.descriptor[0]["finished"]):
			status += " and finished";
		p.PrintLn("%s\n\n\t%s fps | %s speed\n\t%s turns | %s sec" % (p.fullString(status,9), p.fullString("%.1f" % self.gui.fps,7), p.fullString(self.gui.speed,4), p.fullString(self.world.turns,5), p.fullString((int(glutGet(GLUT_ELAPSED_TIME)/1000)),6)));

	def DrawText(self):
		p = self.printer;
		p.PrintLn();
		self.DrawEngineStats(p);
		p.PrintLn();
		self.DrawGameStats(p);
		p.PrintLn();
		self.DrawFieldStats(p);

	def Draw(self):
		GuiObject.Draw(self);
		if(self.visible):
			self.DrawText();

class TextPrinter(object):

	def __init__(self):
		self.ResetRaster();
		self.tabSize = 4; # in blanks
		self.color = colorset;
		self.SetColor();
		self.SetColumn();
		self.x = 1.0;
		self.y = 0.03;

	def Reshape(self, x, y):
		self.x = int(x / 8.0);
		self.y = 0.03;

	def ResetRaster(self):
		self.rasterPos = 0.1;

	def SetColumn(self):
		glRasterPos(0,self.rasterPos);

	def SetColor(self):
		glColor3f(self.color[0], self.color[1], self.color[2]);

	def fullString(self, string="", length=4, fillChar=" "):
		"""
		fullString([string=""[, length=4[, fillChar="0"]]]) => "0000"
		fullString(25,6) => "000025"
		fullString("test",8," ") => "    test"
		"""
		while(len(str(string)) < length):
			string = fillChar + str(string);
		return string;

	def PrintLn(self, text=""):
		self.Print(" "+text+"\n");

	def PrintLines(self, text=""):
		while(len(text) >= self.x):
			self.Print(text[:self.x]+"\n");
			text = text[self.x:];
		self.PrintLn(text);

	def PrintBreak(self):
		self.rasterPos += self.y;
		self.SetColumn();

	def Print(self, text):
		for character in text:
			if(character == "\n"):
				self.PrintBreak();
			elif(character == "\t"):
				self.Print(" "*self.tabSize);
			else:
				glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(character));
