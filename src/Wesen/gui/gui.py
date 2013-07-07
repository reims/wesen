"""This GUI is an example how visualization may help
in developing AI code and watch tournaments.

For implementation details, see basicgui.py"""

from .basicgui import BasicGUI;
from OpenGL.GL import GL_RGB, GL_UNSIGNED_BYTE, glReadPixels;
from OpenGL.GLU import GLubyte;
from OpenGL.GLUT import GLUT_RIGHT_BUTTON, \
    glutCreateMenu, glutAddMenuEntry, glutAttachMenu;
from PIL import Image;

cl_freak = [[0.4, 0.2, 0.6], [0.6, 0.2, 0.4],
	    [0.8, 0.2, 0.2], [0.2, 0.2, 0.8],
	    [0.7, 0.3, 0.1], [0.1, 0.3, 0.7]];

class GUI(BasicGUI):

	def __init__(self, infoGUI, GameLoop, world, extraArgs):
		"""SEE BasicGUI"""
		self.movieMode = False;
		# the following starts glutMainLoop:
		BasicGUI.__init__(self, infoGUI, GameLoop, world, extraArgs, colorList=cl_freak);

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
		glutAddMenuEntry(b"display key bindings", 55);
		glutAddMenuEntry(b"pause   (space)", 100);
		glutAttachMenu(GLUT_RIGHT_BUTTON);

	def HandleAction(self, action):
		if(action == 55):
			line = "".join(["'%s' %s\n" % (key, self.keyExplanation[key])
					for key in sorted(self.keyExplanation.keys())]);
			self.text.Print(line);
		elif(action == 100):
			self.Pause();
		else:
			raise "unknown action from popup-menu (%s)" % (action);
		return 0;

	def initKeyBindings(self):
		BasicGUI.initKeyBindings(self);
		newKeybindings = {b"m": self.ToggleMovie,
				  100 : lambda : self.ModifyFood("delete"),
				  101 : lambda : self.ModifyFood("increase"),
				  102 : lambda : self.ModifyFood("add"),
				  103 : lambda : self.ModifyFood("decrease"),
				  };
		newKeyExplanations = {"m":str(self.ToggleMovie.__doc__),
				      self._getKeyRepresentation(100):"Delete some food",
				      self._getKeyRepresentation(101):"Increase overall food energy",
				      self._getKeyRepresentation(102):"Add some food",
				      self._getKeyRepresentation(103):"Decrease overall food energy",
				      };
		self.keybindings.update(newKeybindings);
		self.keyExplanation.update(newKeyExplanations);

	def HandleMouse(self, button, state, x, y):
		"""handles all mouse events as clicks, dragdrops, etc."""
		BasicGUI.HandleMouse(self, button, state, x, y);
		if(state == 1):
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

	def ToggleMovie(self):
		"""Toggle movie mode on/off. In movie mode, each frame is saved to disk."""
		self.movieMode = not self.movieMode;

	def RenderScene(self):
		"""draws the actual descriptor"""
		BasicGUI.RenderScene(self);
		if(self.movieMode):
			self.takeScreenshot().save(("m%08d.png" % (self.turns)));
