from ..strings import VERSIONSTRING
from .map import Map
from .text import Text
from .graph import Graph
from OpenGL.GL import glClearColor, glLineWidth, \
    glEnable, glViewport, glTranslatef, \
    glScale, glLoadIdentity, glClear, glMatrixMode, \
    glPushMatrix, glPopMatrix, glFinish, GLError, \
    GL_LINE_SMOOTH, GL_COLOR_BUFFER_BIT, GL_MODELVIEW
from OpenGL.GLUT import glutMainLoop, glutInitDisplayMode, \
    glutInitWindowSize, glutInitWindowPosition, glutInit, \
    glutCreateWindow, glutDisplayFunc, glutIdleFunc, \
    glutPostRedisplay, glutReshapeFunc, glutKeyboardFunc, \
    glutSpecialFunc, glutMouseFunc, glutSwapBuffers, glutGet, \
    GLUT_ELAPSED_TIME, GLUT_DOUBLE, GLUT_RGB
import sys
import traceback

# TODO Error checking should be a config option.
import OpenGL
OpenGL.ERROR_CHECKING = False
# performance-relevant

#glutArgvDebugging = "--indirect --sync --gldebug";

cl_default = [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0],
              [1.0, 0.0, 1.0], [1.0, 1.0, 0.0],
              [0.0, 1.0, 1.0], [0.5, 0.0, 0.0],
              [0.0, 0.0, 0.5], [0.5, 0.0, 0.5],
              [0.5, 0.5, 0.0], [0.0, 0.5, 0.5]]


class BasicGUI(object):

    def __init__(self, infoGUI, GameLoop, world, extraArgs, colorList=cl_default):
        """infoGUI should be a dict,
        GameLoop a method,
        world a World object and
        extraArgs is a string which is passed to OpenGL"""
        # TODO there are a bit too many member variables.
        self.GameLoop = GameLoop
        self.wesend = infoGUI["wesend"]
        self.infoWorld = infoGUI["world"]
        self.infoWesen = infoGUI["wesen"]
        self.infoFood = infoGUI["food"]
        self.infoGui = infoGUI["gui"]
        self.world = world
        self.windowactive = True
        self.size = self.infoGui["size"]
        self.windowSize = [self.size, self.size]
        self.pause = False
        self.init = True
        self.frame = 0
        self.lasttime = 0
        self.lastturns = 0
        self.turns = 0
        # TODO restore after resume?
        self.fps = 0
        self.tps = 0
        # TODO maybe kill turns per second stats
        self.speed = 1.0
        self.wait = 1
        self.posX, self.posY = (0, 0)
        initxy = self.infoGui["pos"]
        self.initx = int(initxy[:initxy.index(",")])
        self.inity = int(initxy[initxy.index(",") + 1:])
        self.step = False
        # TODO maybe repair step feature
        self.descriptor = [{}, []]
        self.bgcolor = [0.0, 0.0, 0.05]
        self.fgcolor = [0.0, 0.1, 0.2]
        self.colorList = colorList *\
            int(1 + len(self.infoWesen["sources"]) / len(colorList))
        self.graph = Graph(self, self.world,
                           self.infoWesen["sources"],
                           self.colorList)
        self.map = Map(self, self.infoWorld,
                       self.infoWesen["sources"],
                       self.colorList)
        self.world.setCallbacks(self.map.GetCallbacks())
        self.text = Text(self, self.world)
        self.text.SetAspect(2, 1)
        # aspect ratio x:y is 2:1
        self.objects = [self.map, self.text]
        self._initGL(extraArgs)
        self.menu = None
        self.initMenu()
        self.keybindings = dict()
        self.keyExplanation = dict()
        self.initKeyBindings()
        self.mouseFirst = [0, 0]
        self.mouseLast = [0, 0]
        glutMainLoop()

    def _initGL(self, extraArgs):
        """initializes OpenGL and creates the Window"""
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(self.size, self.size)
        glutInitWindowPosition(self.initx, self.inity)
        glutInit(extraArgs.split(" "))
        glutCreateWindow(VERSIONSTRING.encode("ascii"))
        glutDisplayFunc(self.Draw)
        glutIdleFunc(glutPostRedisplay)
        glutReshapeFunc(self.Reshape)
        glutKeyboardFunc(self.HandleKeys)
        glutSpecialFunc(self.HandleKeys)
        glutMouseFunc(self.HandleMouse)
        glClearColor(*(self.bgcolor + [0.0]))
        glEnable(GL_LINE_SMOOTH)
        glLineWidth(1.3)

    def Exit(self):
        """Stop the simulation and quit"""
        glFinish()
        self.world.DumpGameState()
        sys.exit()

    def Pause(self):
        """Pause/Unpause the simulation"""
        self.pause = not self.pause

    def SetSpeed(self, amount):
        """SetSpeed(amount) -> amount is added to the speed, checks if too low  or high"""
        self.wait = 1
        self.speed += amount
        if(self.speed <= 0):
            self.speed = 0.01
        if(self.speed > 1):
            self.speed = 1.0

    def SpeedDown(self):
        """decrease Speed by 0.05"""
        self.SetSpeed(-0.05)

    def SpeedUp(self):
        """increase Speed by 0.05"""
        self.SetSpeed(0.05)

    def Step(self):
        """run 1 turn of game"""
        self.step = True

    def initMenu(self):
        pass
        # subclasses can do:
        #self.menu = glutCreateMenu(self.HandleAction);
        # glutAttachMenu(GLUT_RIGHT_BUTTON);

    def HandleAction(self, action):
        raise NotImplementedError(
            "unknown action from popup-menu (%s)" % (action))

    def _getKeyRepresentation(self, key):
        # TODO rewrite this function for readability.
        specialKeyRepresentation = \
            lambda key: ("<ESC>" if key == 27 else
                         "<RETURN>" if key == 13 else
                         "<LEFT>" if key == 100 else
                         "<UP>" if key == 101 else
                         "<RIGHT>" if key == 102 else
                         "<DOWN>" if key == 103 else
                         str(key))
        return (key.decode('ascii')
                if type(key) is bytes
                else specialKeyRepresentation(key))

    def _generateKeyExplanations(self):
        self.keyExplanation = {self._getKeyRepresentation(key):
                               str(self.keybindings[key].__doc__)
                               for key in self.keybindings}

    def initKeyBindings(self):
        self.keybindings = {b"q": self.Exit, 27: self.Exit, b"x": self.Exit,
                            b" ": self.Pause,
                            b"-": self.SpeedDown,
                            b"+": self.SpeedUp,
                            13: self.Step,  # TODO seems to be broken
                            }
        self._generateKeyExplanations()

    def HandleKeys(self, key, x, y):
        """handle both usual (character) and special (ordinal) keys"""
        #print("key detection: key="+str(key)+" at (x,y)="+str(x)+","+str(y));
        if(key in self.keybindings):
            self.keybindings[key]()

    def _win2glCoord(self, x, y):
        posX = (2.0 * x / self.windowSize[0])
        posY = (2.0 * y / self.windowSize[1])
        return (posX, posY)

    def _win2wesenCoord(self, x, y):
        x, y = self._win2glCoord(x, y)
        posX = int(x * self.infoWorld["length"])
        posY = int((1.0 - y) * self.infoWorld["length"]) + 1
        # why +1 ?
        return (posX, posY)

    def HandleMouse(self, button, state, x, y):
        """handles all mouse events as clicks, dragdrops, etc."""
        if(state == 0):
            self.mouseFirst = [x, y]
            posX, posY = self._win2wesenCoord(x, y)
            if(posX != self.posX or posY != self.posY):
                self.posX, self.posY = (posX, posY)
        if(state == 1):
            self.mouseLast = [x, y]

    def Reshape(self, x, y):
        """warning: symmetrical x/y reshape not implemented yet"""
        glViewport(0, 0, x, y)
        self.windowSize = [x, y]
        for o in self.objects:
            o.Reshape(x, y)

    def RenderScene(self):
        """draws the actual descriptor"""
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        glTranslatef(-1.0, 0.0, 0.0)
        # draw at -1.0/0.0 - 0.0/1.0
        self.map.Draw(self.descriptor)
        glPopMatrix()
        glPushMatrix()
        # draw at 0.0/0.0 - 1.0/1.0 (standard)
        self.graph.Draw()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(-1.0, -1.0, 0.0)
        # draw at -1.0/-1.0 - 0.0/1.0
        glScale(2.0, 1.0, 1.0)
        self.text.Draw()
        glPopMatrix()
        glutSwapBuffers()

    def CalcFps(self):
        """calculates GUI.fps and GUI.tps (call every frame)"""
        self.frame += 1
        actualtime = glutGet(GLUT_ELAPSED_TIME)
        timenow = actualtime - self.lasttime
        turnsnow = self.turns - self.lastturns
        if(timenow > 1000):
            self.fps = self.frame * 1000.0 / timenow
            self.lasttime = actualtime
            self.lastturns = self.turns
            self.tps = turnsnow * 1000.0 / timenow
            self.frame = 0

    def Draw(self):
        """actualizes the descriptor by calling his GameLoop and renders it"""
        # TODO figure out how self.step is supposed to work (broken!)
        # TODO find out if the framedropping mechanism is already killed
        # everywhere
        if((not self.pause) or self.step):
            if(self.step):
                self.descriptor = self.GameLoop()
                self.turns += 1
                self.CalcFps()
                self.graph.Step()
                self.step = False
            else:
                if(self.wait == int(1.0 / self.speed)):
                    self.wait = 1
                    self.descriptor = self.GameLoop()
                    self.turns += 1
                    self.CalcFps()
                    self.graph.Step()
                else:
                    self.wait += 1
        if(self.init):
            self.Pause()
            self.init = False
        # TODO do the try/catch only in debugging-mode
        try:
            self.RenderScene()
        except GLError as e:
            print("exception:", e)
            print(traceback.format_exc())
            sys.exit(1)
            return 0
        return 1
