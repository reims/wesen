"""Each object in the GUI that gets real estate is a GuiObject"""

from OpenGL.GL import glColor3f, glRectf;

class GuiObject(object):
	"""A GuiObject maintains a frame."""

	def __init__(self, gui):
		self.gui = gui;
		self.frame = {"frame":0.003, # ???
			      "color":[0.75, 0.75, 0.75], # base color
			      "plastic":0.5, # thickness of the frame
			      "aspect":1}; # ???

	def _getFrameData(self):
		#TODO the whole frame mechanism should be beautified.
		frame = self.frame["frame"];
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

	def SetAspect(self, x, y):
		#TODO understand the "aspect" mechanism...
		self.frame["aspect"] = x / y;

	def _drawframe(self):
		"""Draw a frame around the GuiObject"""
		frame, col, plast, x, y = self._getFrameData();
		glColor3f(*(c-plast for c in col));
		glRectf(0.0, 1.0, 1.0, 1.0-x); # top
		glRectf(0.0, 0.0, y, 1.0); # left
		glColor3f(*(c+plast for c in col));
		glRectf(0.0, 0.0, 1.0, x); # bottom
		glRectf(1.0, 0.0, 1.0-y, 1.0); # right

	def Draw(self):
		"""Each GuiObject has a Draw() method."""
		self._drawframe();

	def Reshape(self, x, y):
		"""Each GuiObject can handle reshaping events."""
		pass;
