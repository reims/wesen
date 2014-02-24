"""This module contains all methods related to displaying text in the gui"""

from OpenGL.GL import glPushMatrix, glPopMatrix, \
    glTranslatef, glRasterPos
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13
from .object import GuiObject


class Text(GuiObject):

    """A Text object displays world.stats"""

    def __init__(self, gui, world):
        GuiObject.__init__(self, gui)
        self.world = world
        self.printer = TextPrinter()
        self.givenText = None
        # TODO replace this mechanism by something else

    def Print(self, line):  # TODO replace this mechanism by something else
        self.givenText = line

    def Reshape(self, x, y):
        GuiObject.Reshape(self, x, y)
        self.printer.Reshape(x, y)

    def DrawGameStats(self):
        """Print world.stats"""
        p = self.printer
        statString = "%-20s | %9s | %9s | %14s |\n"
        p.Print(statString %
                ("", "energy", "count", "energy/object"))
        for source in sorted(self.world.stats.keys()):
            energy = self.world.stats[source]["energy"]
            count = self.world.stats[source]["count"]
            if(count == 0):
                perWesen = 0
            else:
                perWesen = energy // count
            p.Print(statString %
                    (source, energy, count, perWesen))

    def DrawEngineStats(self):
        """Print some information about the game engine,
        such as fps (frames per second), number of turns, etc."""
        p = self.printer
        p.Print("paused" if self.gui.pause else "running")
        p.Print("\n\n\n%3.1f fps,  %8d turns\n\n" %
                (self.gui.fps, self.world.turns))
        # p.Print("manual slowdown: %3d percent" %
        #	  (int(100.0/self.gui.speed)));

    def DrawGivenText(self):  # TODO replace this mechanism by something else
        if(self.givenText is not None):
            self.printer.Print("\n")
            self.printer.Print(self.givenText)

    def Draw(self):
        GuiObject.Draw(self)
        self.printer.ResetRaster()
        self.DrawEngineStats()
        self.DrawGameStats()
        self.DrawGivenText()


class TextPrinter(object):

    """A printer that uses OpenGL to draw strings.
    Use ResetRaster() and then Print(text)."""

    def __init__(self):
        self.x = 0  # TODO x currently unused, results in suboptimal resizing
        self.y = 0.03  # TODO where does the magic number come from?
        self.rasterPos = 0
        self.ResetRaster()

    def ResetRaster(self):
        """Call each frame before any Print()"""
        self.rasterPos = self.y
        self.Print("\n")

    def Reshape(self, x, y):
        self.x = x
        self.y = 30 / y

    def Print(self, text):
        """Print(String text) prints text to the screen"""
        glPushMatrix()
        glTranslatef(0.02, 0.96, 0.0)
        for character in text:
            if(character == "\n"):
                self.rasterPos -= self.y
                glRasterPos(0, self.rasterPos)
            else:
                glutBitmapCharacter(GLUT_BITMAP_8_BY_13,
                                    ord(character))
        glPopMatrix()
