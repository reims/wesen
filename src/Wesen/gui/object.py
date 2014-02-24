"""Each object in the GUI that gets real estate is a GuiObject"""

from OpenGL.GL import glColor3f, glRectf


class GuiObject(object):

    """A GuiObject maintains a visual frame around it."""

    def __init__(self, gui):
        self.gui = gui
        self.frame = {"frame": 0.003,  # ???
                      "color": [0.75, 0.75, 0.75],  # base color
                      "plastic": 0.5,  # thickness of the frame
                      "aspect": 1, "x": 0, "y": 0}

    def _getFrameData(self):
        """returns a dict with info about the visual frame"""
        # TODO the whole frame mechanism should be beautified.
        frame = self.frame["frame"]
        aspect = self.frame["aspect"]
        if(aspect < 1):
            x = frame / aspect
            y = frame
        else:
            y = frame / aspect
            x = frame
        self.frame["x"] = x
        self.frame["y"] = y
        return self.frame

    def SetAspect(self, x, y):
        """takes width and height and sets the visual frame aspect.
        This is necessary to let the frame be of same thickness horizontally
        and vertically, even after rescaling."""
        self.frame["aspect"] = x / y

    def _drawframe(self):
        """Draw a frame around the GuiObject"""
        framedata = self._getFrameData()
        color, plastic, x, y = framedata["color"], framedata["plastic"], \
            framedata["x"], framedata["y"]
        glColor3f(*(c - plastic for c in color))
        glRectf(0.0, 1.0, 1.0, 1.0 - x)
        # top
        glRectf(0.0, 0.0, y, 1.0)
        # left
        glColor3f(*(c + plastic for c in color))
        glRectf(0.0, 0.0, 1.0, x)
        # bottom
        glRectf(1.0, 0.0, 1.0 - y, 1.0)
        # right

    def Draw(self):
        """Each GuiObject has a Draw() method."""
        self._drawframe()

    def Reshape(self, x, y):
        """Each GuiObject can handle reshaping events."""
        pass
