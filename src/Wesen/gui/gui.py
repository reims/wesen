from ..definition import NAMES, VERSIONS;
from .map import Map;
from .text import Text;
from .graph import Graph;
from .graph import SensorSystem;
from .graph import SENSORFCT_FROMSTATS_ENERGY;
from OpenGL.GL import *;
from OpenGL.GLU import GLubyte;
from OpenGL.GLUT import *;
import sys;
import traceback;

cl_default =   [("red",[1.0, 0.0, 0.0]), ("blue",[0.0, 0.0, 1.0]),
		("violet",[1.0, 0.0, 1.0]), ("brown",[1.0, 1.0, 0.0]),
		("cyan",[0.0, 1.0, 1.0]), ("light red",[0.5, 0.0, 0.0]),
		("light blue",[0.0, 0.0, 0.5]), ("light violet",[0.5, 0.0, 0.5]),
		("light brown",[0.5, 0.5, 0.0]), ("light cyan",[0.0, 0.5, 0.5])];
cl_freak =     [("lilablue",[0.4, 0.2, 0.6]), ("redlila",[0.6, 0.2, 0.4]),
		("red",[0.8, 0.2, 0.2]), ("blue",[0.2, 0.2, 0.8])];

colorList = cl_default;

#glutArgvDebugging = "--indirect --sync --gldebug";

class GUI:

	def __init__(self, infoGUI, GameLoop, world, extraArgs):
		"""infoGUI should be a dict, GameLoop a method, world a World object and extraArgs is a string which is passed to OpenGL"""
		self.GameLoop = GameLoop;
		self.config = infoGUI["config"];
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
		self.descriptor = [{},[]];
		self.bgcolor = [0.0, 0.0, 0.05];
		self.fgcolor = [0.0, 0.1, 0.2];
		self.graph = Graph(self, self.world);
		SensorSystem(self, self.graph, self.world);
		self._SetColorDescriptor();
		self.map = Map(self, self.infoWorld, self.colorDescriptor);
		self.text = Text(self, self.descriptor, self.world, self.infoWorld);
		self.text.SetAspect(2,1); # aspect ratio x:y is 2:1
		self.objects = [self.map, self.text];
		if(not self.infoGui["map"]): self.map.ChangeVisibility();
		if(not self.infoGui["text"]): self.text.ChangeVisibility();
		if(not self.infoGui["graph"]): self.graph.ChangeVisibility();
		self.initGL(extraArgs);
		self.initMenu();
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
		#NOTE: the following lines would make sense for fancier graphics:
		#glEnable(GL_ALPHA_TEST);
		#glAlphaFunc(GL_GREATER, 0);
		#glEnable(GL_DEPTH_TEST);
		#glEnable(GL_BLEND);
		#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
		glClearColor(self.bgcolor[0], self.bgcolor[1], self.bgcolor[2], 0.0);

	def Exit(self):
		glFinish();
		sys.exit();

	def Pause(self):
		self.pause = not self.pause;

	def SetSpeed(self, amount):
		"""SetSpeed(amount) -> amount is added to the speed, checks if too low  or high"""
		self.wait = 1;
		self.speed += amount;
		if(self.speed <= 0):
			self.speed = 0.0;
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
		glutAddMenuEntry(b"change map visibility",0);
		glutAddMenuEntry(b"change graph visibility",25);
		glutAddMenuEntry(b"change text visibility",50);
		glutAddMenuEntry(b"display key bindings",55);
		glutAddMenuEntry(b"pause   (space)",100);
		glutAttachMenu(GLUT_RIGHT_BUTTON);

	def HandleAction(self, action):
		if(action == 0):
			self.map.ChangeVisibility();
		elif(action == 25):
			self.graph.ChangeVisibility();
		elif(action == 50):
			self.text.ChangeVisibility();
		elif(action == 55):
			self.text.Print("key bindings:\nx|q|esc: exit\n p|space: pause\n+-:speed\nik:frame drop rate\nm:movie mode\nd:debug info\narrows: modify food, left/right: del/add, up/down: inc/dec."); #TODO put that string somewhere else
		elif(action == 100):
			self.Pause();
		else:
			raise "unknown action from popup-menu (%s)" % (action);
		return 0;

	def HandleKeys(self, key, x, y):
		"""handle both usual (character) and special (ordinal) keys"""
		#print("key detection: key="+str(key)+" at (x,y)="+str(x)+","+str(y));
		#TODO document this functionality somewhere (e.g. in the menu)
		if(key == b"x" or key == b"q"): self.Exit();
		elif(key == b"p" or key == b" "): self.Pause();
		elif(key == b"-"): self.SpeedDown();
		elif(key == b"+"): self.SpeedUp();
		elif(key == b"i"): self.DropDown();
		elif(key == b"k"): self.DropUp();
		elif(key == b"m"): self.ToggleMovie();
		elif(key == b"d"): print(self.infoWorld);
		elif(key == 13): self.Step(); # <enter> #TODO seems to be broken
		elif(key == 27): self.Exit(); # <esc>
		elif(key == 100): self.ModifyFood("delete");   # <leftarrow>
		elif(key == 101): self.ModifyFood("increase"); # <uparrow>
		elif(key == 102): self.ModifyFood("add");      # <rightarrow>
		elif(key == 103): self.ModifyFood("decrease"); # <downarrow>

	def ToggleMovie(self):
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
			self.mouseFirst = [x,y];
			posX, posY = self._win2wesenCoord(x, y);
			if(posX != self.posX or posY != self.posY):
				self.posX, self.posY = (posX, posY);
		if(state == 1):
			self.mouseLast = [x,y];
			image = self.takeScreenshot();
			image.save('screenshot.png');

	def takeScreenshot(self):
		"""takes a screenshot of the map region"""
		(width,height) = self.windowSize;
		buffer = ( GLubyte * (3*width*height) )(0);
		glReadPixels(0,0,width,height,
			     GL_RGB,GL_UNSIGNED_BYTE, buffer);
		from PIL import Image;
		image = Image.fromstring(mode="RGB",
					size=(width, height),
					data=buffer);
		image = image.transpose(Image.FLIP_TOP_BOTTOM);
		image = image.crop((0,0,width//2,height//2));
		image = image.resize((800,800),Image.ANTIALIAS);
		return image;

	def Reshape(self, x, y):
		"""warning: symmetrical x/y reshape not implemented yet"""
		glViewport(0, 0, x, y);
		self.windowSize = [x, y];
		for object in self.objects:
			object.Reshape(x,y);

	def DrawMap(self):
		glTranslatef(-1.0, 0.0, 0.0); # draw at -1.0/0.0 - 0.0/1.0
		if(self.map.visible):
			self.map.SetDescriptor(self.descriptor);
		if(self.descriptor[0]["finished"]):
			self.map.active = False;
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

	def ResetView(self):
		glLoadIdentity();

	def RenderScene(self):
		"""draws the actual descriptor"""
		glClear(GL_COLOR_BUFFER_BIT);
		glMatrixMode(GL_MODELVIEW);
		self.ResetView();
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
		if((not self.pause) or self.step):
			if(self.step):
				self.descriptor = self.GameLoop();
				self.turns += 1;
				self.CalcFps();
				if(not self.descriptor[0]["finished"]):
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
						if(not self.descriptor[0]["finished"]):
							self.graph.Step();
						dropped += 1;
				else:
					self.wait += 1;
		if(self.init):
			self.Pause();
			self.init = False;
		try:
			self.RenderScene();
		except Exception as e:
			print("exception:", e);
			print(traceback.format_exc());
			sys.exit(1);
			return 0;
		return 1

	def _SetColorDescriptor(self):
		colorDescriptor = {};
		sourceList = self.infoWesen["sources"];
		sourceList.sort();
		enoughColors = colorList * int(1+len(sourceList)/len(colorList));
		for (wesenSource,colorInfo) in zip(sourceList, enoughColors):
			colorDescriptor[wesenSource] = colorInfo[1];
			self.graph.AddSensor({"f":SENSORFCT_FROMSTATS_ENERGY,
					      "color":colorInfo[1],
					      "colorname":colorInfo[0],
					      "statskey":wesenSource,
					      "name":wesenSource+" energy"});
		self.colorDescriptor = colorDescriptor;
