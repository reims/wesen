from OpenGL.GL import *;
#from OpenGL.GLUT import *;

class GuiObject(object):

	def __init__(self, gui):
		self.gui = gui;
		self.frame = {"frame":3, "color":[0.75, 0.75, 0.75],
			      "plastic":0.5, "aspect":1};
		self.shadow = False;
		self.visible = True;
		self.active = True;

	def _getFrameData(self):
		frame = self.frame["frame"] * 0.001;
		col = self.frame["color"];
		plast = self.frame["plastic"] / 2.0;
		aspect = self.frame["aspect"];
		if(aspect < 1):
			x = frame / aspect;
			y = frame;
		else:
			y = frame / aspect;
			x = frame;
		return (frame, col, plast, x, y);

	def ChangeVisibility(self):
		self.visible = not self.visible;
		if(not self.shadow):
			self.active = self.visible;

	def SetAspect(self, x, y):
		self.frame["aspect"] = float(x) / float(y);

	def SetDescriptor(self, descriptor):
		self.descriptor = descriptor;

	def DrawFrame(self):
		frame, col, plast, x, y = self._getFrameData();
		glColor4f(col[0]-plast, col[1]-plast, col[2]-plast, 1.0);
		glRectf(0.0,1.0,1.0,1.0-x); # top
		glRectf(0.0,0.0,y,1.0); # left
		glColor4f(col[0]+plast, col[1]+plast, col[2]+plast, 1.0);
		glRectf(0.0,0.0,1.0,x); # bottom
		glRectf(1.0,0.0,1.0-y,1.0); # right

	def DrawBlank(self):
		frame, col, plast, x, y = self._getFrameData();
		glColor4f(self.gui.fgcolor[0], self.gui.fgcolor[1], self.gui.fgcolor[2], 1.0);
		glRectf(0.0+x,0.0+y,1.0-x,1.0-y);

	def Draw(self):
		self.DrawFrame();
		if(not self.visible):
			self.DrawBlank();

	def Reshape(self, x, y):
		self.width = x;
		self.height = y;

	def Step(self):
		pass;
