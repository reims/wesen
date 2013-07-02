from OpenGL.GL import glColor3f, glRectf;

class GuiObject(object):

	def __init__(self, gui):
		self.gui = gui;
		self.frame = {"frame":3, "color":[0.75, 0.75, 0.75],
			      "plastic":0.5, "aspect":1};
		self.visible = True;

	def _getFrameData(self):
		frame = self.frame["frame"] * 0.001;
		color = self.frame["color"];
		plastic = self.frame["plastic"];
		aspect = self.frame["aspect"];
		if(aspect < 1):
			x = frame / aspect;
			y = frame;
		else:
			y = frame / aspect;
			x = frame;
		return (frame, color, plastic, x, y);

	def ChangeVisibility(self):
		self.visible = not self.visible;

	def SetAspect(self, x, y):
		self.frame["aspect"] = x / y;

	def SetDescriptor(self, descriptor):
		self.descriptor = descriptor;

	def DrawFrame(self):
		frame, col, plast, x, y = self._getFrameData();
		glColor3f(*(c-plast for c in col));
		glRectf(0.0, 1.0, 1.0, 1.0-x); # top
		glRectf(0.0, 0.0, y, 1.0); # left
		glColor3f(*(c+plast for c in col));
		glRectf(0.0, 0.0, 1.0, x); # bottom
		glRectf(1.0, 0.0, 1.0-y, 1.0); # right

	def DrawBlank(self):
		frame, col, plast, x, y = self._getFrameData();
		glColor3f(*(self.gui.fgcolor));
		glRectf(0.0+x, 0.0+y, 1.0-x, 1.0-y);

	def Draw(self):
		self.DrawFrame();
		if(not self.visible):
			self.DrawBlank();

	def Reshape(self, x, y):
		self.width = x;
		self.height = y;

	def Step(self):
		pass;
