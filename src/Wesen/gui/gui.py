from ..definition import NAMES, VERSIONS;
from ..defaults import DEFAULT_GAME_STATE_FILE;
from .map import Map;
from .text import Text;
from .graph import Graph;
from OpenGL.GL import glClearColor, glLineWidth, \
    glEnable, glViewport, glReadPixels, glTranslatef, \
    glScale, glLoadIdentity, glClear, glMatrixMode, \
    glPushMatrix, glPopMatrix, glFinish, GLError, \
    GL_RGB, GL_UNSIGNED_BYTE, GL_LINE_SMOOTH, \
    GL_COLOR_BUFFER_BIT, GL_MODELVIEW;
from OpenGL.GLU import GLubyte;
from OpenGL.GLUT import glutMainLoop, glutInitDisplayMode, \
    glutInitWindowSize, glutInitWindowPosition, glutInit, \
    glutCreateWindow, glutDisplayFunc, glutIdleFunc, \
    glutPostRedisplay, glutReshapeFunc, glutKeyboardFunc, \
    glutSpecialFunc, glutMouseFunc, glutCreateMenu, \
    glutAddMenuEntry, glutAttachMenu, glutSwapBuffers, glutGet, \
    GLUT_ELAPSED_TIME, GLUT_DOUBLE, GLUT_RGB, GLUT_RIGHT_BUTTON;
from PIL import Image;
import sys;
import traceback;

#TODO Error checking should be a config option.
import OpenGL;
OpenGL.ERROR_CHECKING = False; # performance-relevant

cl_default =   [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0],
		[1.0, 0.0, 1.0], [1.0, 1.0, 0.0],
		[0.0, 1.0, 1.0], [0.5, 0.0, 0.0],
		[0.0, 0.0, 0.5], [0.5, 0.0, 0.5],
		[0.5, 0.5, 0.0], [0.0, 0.5, 0.5]];
cl_freak =     [[0.4, 0.2, 0.6], [0.6, 0.2, 0.4],
		[0.8, 0.2, 0.2], [0.2, 0.2, 0.8],
		[0.7, 0.3, 0.1], [0.1, 0.3, 0.7]];

colorList = cl_freak;

#glutArgvDebugging = "--indirect --sync --gldebug";

class GUI:

	def __init__(self, infoGUI, GameLoop, world, extraArgs):
		"""infoGUI should be a dict,
		GameLoop a method,
		world a World object and
		extraArgs is a string which is passed to OpenGL"""
		self.GameLoop = GameLoop;
		self.wesend = infoGUI["wesend"];
		self.infoWorld = infoGUI["world"];
		self.infoWesen = infoGUI["wesen"];
		self.infoFood = infoGUI["food"];
		self.infoGui = infoGUI["gui"];
		self.world = world;
		self.windowactive = True;
		self.size = self.infoGui["size"];
		self.windowSize = [self.size, self.size];
		self.pause = False;
		self.init = True;
		self.frame = 0;
		self.lasttime = 0;
		self.lastturns = 0;
		self.turns = 0;
		self.fps = 0;
		self.tps = 0;
		self.speed = 1.0;
		self.wait = 1;
		self.dropFrames = 0;
		self.movieMode = False;
		self.posX, self.posY = (0, 0);
		initxy = self.infoGui["pos"];
		self.initx = int(initxy[:initxy.index(",")]);
		self.inity = int(initxy[initxy.index(",")+1:]);
		self.fieldInformation = [];
		self.step = False;
		self.descriptor = [{}, []];
		self.bgcolor = [0.0, 0.0, 0.05];
		self.fgcolor = [0.0, 0.1, 0.2];
		self.colorList = colorList *\
		    int(1+len(self.infoWesen["sources"])/len(colorList));
		self.graph = Graph(self, self.world,
				   self.infoWesen["sources"],
				   self.colorList);
		self.map = Map(self, self.infoWorld,
			       self.infoWesen["sources"],
			       self.colorList);
		self.text = Text(self, self.world);
		self.text.SetAspect(2, 1); # aspect ratio x:y is 2:1
		self.objects = [self.map, self.text];
		#TODO remove the capability to change visibility in GuiObject!
		if(not self.infoGui["map"]): self.map.ChangeVisibility();
		if(not self.infoGui["text"]): self.text.ChangeVisibility();
		if(not self.infoGui["graph"]): self.graph.ChangeVisibility();
		self.initGL(extraArgs);
		self.initMenu();
		self.initKeyBindings();
		glutMainLoop();

	def initGL(self, extraArgs):
		"""initializes OpenGL and creates the Window"""
		glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
		glutInitWindowSize(self.size, self.size);
		glutInitWindowPosition(self.initx, self.inity);
		glutInit(extraArgs.split(" "));
		glutCreateWindow((NAMES["PROJECT"]+" "+VERSIONS["PROJECT"]).encode("ascii"));
		glutDisplayFunc(self.Draw);
		glutIdleFunc(glutPostRedisplay);
		glutReshapeFunc(self.Reshape);
		glutKeyboardFunc(self.HandleKeys);
		glutSpecialFunc(self.HandleKeys);
		glutMouseFunc(self.HandleMouse);
		glClearColor(*(self.bgcolor+[0.0]));
		glEnable(GL_LINE_SMOOTH);
		glLineWidth(1.3);

	def Exit(self):
		"""Stop the simulation and quit"""
		glFinish();
		self.DumpGameState();
		sys.exit();

	def Pause(self):
		"""Pause/Unpause the simulation"""
		self.pause = not self.pause;

	def DumpGameState(self, filename = DEFAULT_GAME_STATE_FILE):
		with open(filename, 'w') as f:
			json = self.world.persistToJSON();
			f.write(json);

	def SetSpeed(self, amount):
		"""SetSpeed(amount) -> amount is added to the speed, checks if too low  or high"""
		self.wait = 1;
		self.speed += amount;
		if(self.speed <= 0):
			self.speed = 0.01;
		if(self.speed > 1):
			self.speed = 1.0;

	def DropDown(self):
		"""decrease framedrops by 1"""
		self.dropFrames -= 1;
		if(self.dropFrames < 0):
			self.dropFrames = 0;

	def DropUp(self):
		"""increase framedrops by 1"""
		self.dropFrames += 1;

	def SpeedDown(self):
		"""decrease Speed by 0.05"""
		self.SetSpeed(-0.05);

	def SpeedUp(self):
		"""increase Speed by 0.05"""
		self.SetSpeed(0.05);

	def Step(self):
		"""run 1 turn of game"""
		self.step = True;

	def ModifyFood(self, action):
		"""action can be "delete" "add" "increase" "decrease" """
		if(action == "delete"):
			for o in self.world.objects.values():
				if(o.objectType == "food"):
					if(self.world.DeleteObject(o.id)):
						break;
		if(action == "add"):
			infoFood = self.infoFood;
			if("position" in infoFood):
				del infoFood["position"];
			self.world.AddObject(infoFood);
		if(action == "increase"):
			for o in self.world.objects.values():
				if(o.objectType == "food"):
					o.energy += 10;
		if(action == "decrease"):
			for o in self.world.objects.values():
				if(o.objectType == "food"):
					o.energy -= 10;

	def initMenu(self):
		self.menu = glutCreateMenu(self.HandleAction);
		glutAddMenuEntry(b"change map visibility", 0);
		glutAddMenuEntry(b"change graph visibility", 25);
		glutAddMenuEntry(b"change text visibility", 50);
		glutAddMenuEntry(b"display key bindings", 55);
		glutAddMenuEntry(b"pause   (space)", 100);
		glutAttachMenu(GLUT_RIGHT_BUTTON);

	def HandleAction(self, action):
		if(action == 0):
			self.map.ChangeVisibility();
		elif(action == 25):
			self.graph.ChangeVisibility();
		elif(action == 50):
			self.text.ChangeVisibility();
		elif(action == 55):
			line = "".join(["'%s' %s\n" % (key, self.keyExplanation[key])
					for key in sorted(self.keyExplanation.keys())]);
			self.text.Print(line);
		elif(action == 100):
			self.Pause();
		else:
			raise "unknown action from popup-menu (%s)" % (action);
		return 0;

	def initKeyBindings(self):
		specialKeyRepresentation = \
		    lambda key : ("<ESC>"    if key == 27 else
				  "<RETURN>" if key == 13 else
				  "<LEFT>"   if key == 100 else
				  "<UP>"     if key == 101 else
				  "<RIGHT>"  if key == 102 else
				  "<DOWN>"   if key == 103 else
				  str(key));
		keyRepresentation = \
		    lambda key : (key.decode('ascii')
				  if type(key) is bytes
				  else specialKeyRepresentation(key));
		keybindings = {b"x": self.Exit, b"q":self.Exit, 27:self.Exit,
			       b"p": self.Pause, b" ":self.Pause,
			       b"-": self.SpeedDown,
			       b"+": self.SpeedUp,
			       b"i": self.DropDown,
			       b"k": self.DropUp,
			       b"m": self.ToggleMovie,
			       #b"d": lambda : print(self.infoWorld),
			       13  : self.Step, #TODO seems to be broken
			       100 : lambda : self.ModifyFood("delete"),
			       101 : lambda : self.ModifyFood("increase"),
			       102 : lambda : self.ModifyFood("add"),
			       103 : lambda : self.ModifyFood("decrease"),
			       };
		self.keyExplanation = {keyRepresentation(key):str(keybindings[key].__doc__)
				       for key in keybindings};
		self.keybindings = keybindings;

	def HandleKeys(self, key, x, y):
		"""handle both usual (character) and special (ordinal) keys"""
		#print("key detection: key="+str(key)+" at (x,y)="+str(x)+","+str(y));
		if(key in self.keybindings):
			self.keybindings[key]();

	def ToggleMovie(self):
		"""Toggle movie mode on/off. In movie mode, each frame is saved to disk."""
		self.movieMode = not self.movieMode;

	def _win2glCoord(self, x, y):
		posX = (2.0 * x / self.windowSize[0]);
		posY = (2.0 * y / self.windowSize[1]);
		return (posX, posY);

	def _win2wesenCoord(self, x, y):
		x, y = self._win2glCoord(x, y);
		posX = int(x * self.infoWorld["length"]);
		posY = int((1.0-y) * self.infoWorld["length"])+1; # why +1 ?
		return (posX, posY);

	def HandleMouse(self, button, state, x, y):
		"""handles all mouse events as clicks, dragdrops, etc."""
		if(state == 0):
			self.mouseFirst = [x, y];
			posX, posY = self._win2wesenCoord(x, y);
			if(posX != self.posX or posY != self.posY):
				self.posX, self.posY = (posX, posY);
		if(state == 1):
			self.mouseLast = [x, y];
			image = self.takeScreenshot();
			image.save('screenshot.png');

	def takeScreenshot(self):
		"""takes a screenshot of the map region"""
		(width, height) = self.windowSize;
		buffer = ( GLubyte * (3*width*height) )(0);
		glReadPixels(0, 0, width, height,
			     GL_RGB, GL_UNSIGNED_BYTE, buffer);
		image = Image.fromstring(mode="RGB",
					size=(width, height),
					data=buffer);
		# use image coordinates, not OpenGL coordinates:
		image = image.transpose(Image.FLIP_TOP_BOTTOM);
		# take only the Map part of the screenshot:
		image = image.crop((0, 0, width//2, height//2));
		# resize to a uniform format (important for movie mode):
		image = image.resize((800, 800), Image.ANTIALIAS);
		return image;

	def Reshape(self, x, y):
		"""warning: symmetrical x/y reshape not implemented yet"""
		glViewport(0, 0, x, y);
		self.windowSize = [x, y];
		for o in self.objects:
			o.Reshape(x, y);

	def DrawMap(self):
		glTranslatef(-1.0, 0.0, 0.0); # draw at -1.0/0.0 - 0.0/1.0
		if(self.map.visible):
			self.map.SetDescriptor(self.descriptor);
		self.map.Draw();

	def DrawGraph(self):
		# draw at 0.0/0.0 - 1.0/1.0 (standard)
		self.graph.Draw();

	def DrawText(self):
		glTranslatef(-1.0, -1.0, 0.0); # draw at -1.0/-1.0 - 0.0/1.0
		glScale(2.0, 1.0, 1.0);
		self.text.SetDescriptor(self.descriptor);
		self.text.Step();
		self.text.Draw();

	def RenderScene(self):
		"""draws the actual descriptor"""
		glClear(GL_COLOR_BUFFER_BIT);
		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity();
		glPushMatrix();
		self.DrawMap();
		glPopMatrix();
		glPushMatrix();
		self.DrawGraph();
		glPopMatrix();
		glPushMatrix();
		self.DrawText();
		glPopMatrix();
		glutSwapBuffers();
		if(self.movieMode):
			self.takeScreenshot().save(("m%08d.png" % (self.turns)));

	def CalcFps(self):
		"""calculates GUI.fps and GUI.tps (call every frame)"""
		self.frame += 1;
		self.actualtime = glutGet(GLUT_ELAPSED_TIME);
		timenow = self.actualtime - self.lasttime;
		turnsnow = self.turns - self.lastturns;
		if(timenow > 1000):
			self.fps = self.frame*1000.0/timenow;
			self.lasttime = self.actualtime;
			self.lastturns = self.turns;
			self.tps = turnsnow*1000.0/timenow;
			self.frame = 0;

	def Draw(self):
		"""actualizes the descriptor by calling his GameLoop and renders it"""
		#TODO figure out how self.step is supposed to work
		#TODO kill the framedropping mechanism
		#     (OpenGL code is very fast now, we don't need that)
		if((not self.pause) or self.step):
			if(self.step):
				self.descriptor = self.GameLoop();
				self.turns += 1;
				self.CalcFps();
				self.graph.Step();
				self.step = False;
			else:
				if(self.wait == int(1.0/self.speed)):
					self.wait = 1;
					dropped = 0;
					while(dropped <= self.dropFrames):
						self.descriptor = self.GameLoop();
						self.turns += 1;
						self.CalcFps();
						self.graph.Step();
						dropped += 1;
				else:
					self.wait += 1;
		if(self.init):
			self.Pause();
			self.init = False;
		#TODO do the try/catch only in debugging-mode
		try:
			self.RenderScene();
		except GLError as e:
			print("exception:", e);
			print(traceback.format_exc());
			sys.exit(1);
			return 0;
		return 1
