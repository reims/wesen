"""Each object in the GUI that gets real estate is a GuiObject"""

from OpenGL.GL import glColor3f, glRectf;

class GuiObject(object):
	"""A GuiObject has a frame and changeable visibility."""

	def __init__(self, gui):
		self.gui = gui;
		self.frame = {"frame":3, "color":[0.75, 0.75, 0.75],
			      "plastic":0.5, "aspect":1};
		self.descriptor = None;
		self.visible = True;

	def _getFrameData(self):
		#TODO the whole frame mechanism should be beautified.
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
		"""Toggle visibility"""
		#TODO Think about removing this,
		#     as it is not necessary for performance any longer!
		self.visible = not self.visible;

	def SetAspect(self, x, y):
		#TODO understand the "aspect" mechanism...
		self.frame["aspect"] = x / y;

	def SetDescriptor(self, descriptor):
		"""Each GuiObject has a SetDescriptor(descriptor)
		method, that should be called each time the data changes."""
		self.descriptor = descriptor;

	def DrawFrame(self):
		"""Draw a frame around the GuiObject"""
		frame, col, plast, x, y = self._getFrameData();
		glColor3f(*(c-plast for c in col));
		glRectf(0.0, 1.0, 1.0, 1.0-x); # top
		glRectf(0.0, 0.0, y, 1.0); # left
		glColor3f(*(c+plast for c in col));
		glRectf(0.0, 0.0, 1.0, x); # bottom
		glRectf(1.0, 0.0, 1.0-y, 1.0); # right

	def DrawBlank(self):
		"""Draw a placeholder for invisible mode"""
		frame, col, plast, x, y = self._getFrameData();
		glColor3f(*(self.gui.fgcolor));
		glRectf(0.0+x, 0.0+y, 1.0-x, 1.0-y);

	def Draw(self):
		"""If visible, draw."""
		self.DrawFrame();
		if(not self.visible):
			self.DrawBlank();

	def Step(self):
		"""Each GuiObject should have a Step() method,
		that is called each turn."""
		pass;

	def Reshape(self, x, y):
		"""Each GuiObject can handle reshaping events."""
		pass;
