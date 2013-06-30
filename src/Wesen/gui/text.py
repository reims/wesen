from OpenGL.GL import *;
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13;
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
		self.givenText = None;

	def Step(self):
		self.printer.ResetRaster();

	def Print(self, line):
		self.givenText = line;

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
				p.PrintLn("Food(%6d): %4d years old" % (element["energy"], element["age"]));
			elif(element["type"] == "wesen"):
				p.PrintLines("%s(%6d): %4d years old - %s" % (element["source"], element["energy"], element["age"], element["sourcedescriptor"]));

	def DrawGameStats(self, p):
		statString = "%-20s | %9s | %9s | %14s |";
		p.PrintLn(statString % 
			  ("","energy","count","energy/object"));
		energy = self.world.energy;
		count = len(self.world.objects);
		if(count == 0):
			perObject = 0;
		else:
			perObject = energy // count;
		p.PrintLn(statString % 
			  ("all", energy, count, perObject));
		for source in list(self.world.stats.keys()):
			energy = self.world.stats[source]["energy"];
			count = self.world.stats[source]["count"];
			if(count == 0):
				perWesen = 0;
			else:
				perWesen = energy // count;
			p.PrintLn(statString % 
				  (source, energy, count, perWesen));
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
		p.PrintLn("%10s\n" % (status));
		p.PrintLn("\t%3.1f fps,  %8d turns" % (self.gui.fps, self.world.turns));
		#p.PrintLn("\t%3d fps | drawing every %s frames" % (self.gui.fps, self.gui.dropFrames+1));
		#p.PrintLn("\t\t\t\t| manual slowdown: %3d percent" % (int(100.0/self.gui.speed)));
		#p.PrintLn("\t%.1f tps | %5d turns | %10d sec | overall tps: %s" % (self.gui.tps, self.world.turns, int(glutGet(GLUT_ELAPSED_TIME)/1000), int(self.world.turns/(glutGet(GLUT_ELAPSED_TIME)/1000)));

	def DrawGivenText(self, p):
		if(self.givenText is not None):
			p.PrintLn(self.givenText);

	def DrawText(self):
		glPushMatrix();
		glTranslatef(0.02, 0.85, 0.0);
		p = self.printer;
		p.PrintLn();
		self.DrawEngineStats(p);
		p.PrintLn();
		self.DrawGameStats(p);
		p.PrintLn();
		self.DrawFieldStats(p);
		p.PrintLn();
		self.DrawGivenText(p);
		glPopMatrix();

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

	def PrintLn(self, text=""):
		self.Print(" "+text+"\n");

	def PrintLines(self, text=""):
		while(len(text) >= self.x):
			self.Print(text[:self.x]+"\n");
			text = text[self.x:];
		self.PrintLn(text);

	def PrintBreak(self):
		self.rasterPos -= self.y;
		self.SetColumn();

	def Print(self, text):
		for character in text:
			if(character == "\n"):
				self.PrintBreak();
			elif(character == "\t"):
				self.Print(" "*self.tabSize);
			else:
				glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(character));
