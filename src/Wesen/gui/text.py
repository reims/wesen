"""This module contains all methods related to displaying text in the gui"""

from OpenGL.GL import glPushMatrix, glPopMatrix, \
    glTranslatef, glRasterPos;
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13;
from .object import GuiObject;

class Text(GuiObject):
	"""A Text object displays world.stats"""

	def __init__(self, gui, world):
		GuiObject.__init__(self, gui);
		self.world = world;
		self.printer = TextPrinter();
		self.givenText = None; #TODO replace this mechanism by something else

	def Print(self, line): #TODO replace this mechanism by something else
		self.givenText = line;

	def Reshape(self, x, y):
		GuiObject.Reshape(self, x, y);
		self.printer.Reshape(x, y);

	def DrawFieldStats(self): #TODO unused? maybe remove.
		p = self.printer;
		fieldInformation = self.gui.fieldInformation;
		if(not fieldInformation):
			return;
		p.Print("Field %s information:\n" % (fieldInformation[0]["position"]));
		for element in fieldInformation:
			if(element["type"] == "food"):
				p.Print("Food(%6d): %4d years old\n" %
					(element["energy"],
					 element["age"]));
			elif(element["type"] == "wesen"):
				p.Print("%s(%6d): %4d years old - %s\n" %
					(element["source"],
					 element["energy"],
					 element["age"],
					 element["sourcedescriptor"]));

	def DrawGameStats(self):
		"""Print world.stats"""
		p = self.printer;
		statString = "%-20s | %9s | %9s | %14s |\n";
		p.Print(statString % 
			  ("","energy","count","energy/object"));
		for source in sorted(self.world.stats.keys()):
			energy = self.world.stats[source]["energy"];
			count = self.world.stats[source]["count"];
			if(count == 0):
				perWesen = 0;
			else:
				perWesen = energy // count;
			p.Print(statString % 
				(source, energy, count, perWesen));

	def DrawEngineStats(self):
		"""Print some information about the game engine,
		such as fps (frames per second), number of turns, etc."""
		p = self.printer;
		status = "paused" if self.gui.pause else "running";
		p.Print(status);
		p.Print("\n\n\n%3.1f fps,  %8d turns\n\n" %
			(self.gui.fps, self.world.turns));
		#TODO clean up the following mess:
		#TODO find out whether/how framedrop,speed and tps work.
		#     (as it seems that tps and fps is only working at full speed)
		#p.PrintLn("%3d fps | drawing every %s frames" %
		#	  (self.gui.fps, self.gui.dropFrames+1));
		#p.PrintLn("| manual slowdown: %3d percent" %
		#	  (int(100.0/self.gui.speed)));
		#p.PrintLn("%.1f tps | %5d turns | %10d sec | overall tps: %s" %
		#	  (self.gui.tps, self.world.turns,
		#	   int(glutGet(GLUT_ELAPSED_TIME)/1000),
		#	   int(self.world.turns/(glutGet(GLUT_ELAPSED_TIME)/1000)));

	def DrawGivenText(self): #TODO replace this mechanism by something else
		if(self.givenText is not None):
			self.printer.Print("\n");
			self.printer.Print(self.givenText);

	def Draw(self):
		GuiObject.Draw(self);
		if(self.visible):
			self.printer.ResetRaster();
			self.DrawEngineStats();
			self.DrawGameStats();
			self.DrawFieldStats();
			self.DrawGivenText();

class TextPrinter(object):
	"""A printer that uses OpenGL to draw strings.
	Use ResetRaster() and then Print(text)."""

	def __init__(self):
		self.y = 0.03;
		self.ResetRaster();

	def ResetRaster(self):
		"""Call each frame before any Print()"""
		self.rasterPos = self.y;
		self.Print("\n");

	def Reshape(self, x, y):
		self.y = 30 / y;

	def PrintLn(self, text=""):
		"""PrintLn() is equivalent to Print(" \n")"""
		self.Print(" "+text+"\n");

	def Print(self, text):
		"""Print(String text) prints text to the screen"""
		glPushMatrix();
		glTranslatef(0.02, 0.96, 0.0);
		for character in text:
			if(character == "\n"):
				self.rasterPos -= self.y;
				glRasterPos(0, self.rasterPos);
			else:
				glutBitmapCharacter(GLUT_BITMAP_8_BY_13,
						    ord(character));
		glPopMatrix();
