#!/usr/bin/env python3
#
# mawj.py -- MiRCART Animation via Waves Generator
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT license.
#

from OpenGL.GL import *
from PIL import Image
import cv2, math, numpy, os, sys, wx, wx.glcanvas

MiRCARTColours = [
# {{{ MiRCARTColours: mIRC colour number to RGBA map given none of ^[BFV_] (bold, italic, reverse, underline],
    [1.00, 1.00, 1.00], # White
    [0.00, 0.00, 0.00], # Black
    [0.00, 0.00, 0.73], # Blue
    [0.00, 0.73, 0.00], # Green
    [1.00, 0.33, 0.33], # Light Red
    [0.73, 0.00, 0.00], # Red
    [0.73, 0.00, 0.73], # Purple
    [0.73, 0.73, 0.00], # Yellow
    [1.00, 1.00, 0.33], # Light Yellow
    [0.33, 1.00, 0.33], # Light Green
    [0.00, 0.73, 0.73], # Cyan
    [0.33, 1.00, 1.00], # Light Cyan
    [0.33, 0.33, 1.00], # Light Blue
    [1.00, 0.33, 1.00], # Pink
    [0.33, 0.33, 0.33], # Grey
    [0.73, 0.73, 0.73], # Light Grey
]
# }}}

class MawjMiRCARTImporter(object):
    """XXX"""

    # {{{ _CellState(): Cell state
    class _CellState():
        CS_NONE             = 0x00
        CS_BOLD             = 0x01
        CS_ITALIC           = 0x02
        CS_UNDERLINE        = 0x04
    # }}}
    # {{{ _ParseState(): Parsing loop state
    class _ParseState():
        PS_CHAR             = 1
        PS_COLOUR_DIGIT0    = 2
        PS_COLOUR_DIGIT1    = 3
    # }}}
    # {{{ _flipCellStateBit(self, cellState, bit): XXX
    def _flipCellStateBit(self, cellState, bit):
        if cellState & bit:
            return cellState & ~bit
        else:
            return cellState | bit
    # }}}
    # {{{ _parseCharAsColourSpec(self, colourSpec, curColours): XXX
    def _parseCharAsColourSpec(self, colourSpec, curColours):
        if len(colourSpec) > 0:
            colourSpec = colourSpec.split(",")
            if  len(colourSpec) == 2                             \
            and len(colourSpec[1]) > 0:
                return [int(colourSpec[0] or curColours[0]),    \
                    int(colourSpec[1])]
            elif len(colourSpec) == 1                           \
            or   len(colourSpec[1]) == 0:
                return [int(colourSpec[0]), curColours[1]]
        else:
            return [15, 1]
    # }}}
    # {{{ fromTextFile(self, pathName): XXX
    def fromTextFile(self, pathName):
        self.inFile = open(pathName, "r")
        self.inSize = self.outMap = None;
        inCurColourSpec = ""; inCurRow = -1;
        inLine = self.inFile.readline()
        inSize = [0, 0]; outMap = []; inMaxCols = 0;
        while inLine:
            inCellState = self._CellState.CS_NONE
            inParseState = self._ParseState.PS_CHAR
            inCurCol = 0; inMaxCol = len(inLine);
            inCurColourDigits = 0; inCurColours = [15, 1]; inCurColourSpec = "";
            inCurRow += 1; outMap.append([]); inRowCols = 0; inSize[1] += 1;
            while inCurCol < inMaxCol:
                inChar = inLine[inCurCol]
                if inChar in set("\r\n"):                                   \
                    inCurCol += 1
                elif inParseState == self._ParseState.PS_CHAR:
                    inCurCol += 1
                    if inChar == "":
                        inCellState = self._flipCellStateBit(               \
                            inCellState, self._CellState.CS_BOLD)
                    elif inChar == "":
                        inParseState = self._ParseState.PS_COLOUR_DIGIT0
                    elif inChar == "":
                        inCellState = self._flipCellStateBit(               \
                            inCellState, self._CellState.CS_ITALIC)
                    elif inChar == "":
                        inCellState |= self._CellState.CS_NONE
                        inCurColours = [15, 1]
                    elif inChar == "":
                        inCurColours = [inCurColours[1], inCurColours[0]]
                    elif inChar == "":
                        inCellState = self._flipCellStateBit(               \
                            inCellState, self._CellState.CS_UNDERLINE)
                    else:
                        inRowCols += 1
                        outMap[inCurRow].append([*inCurColours, inCellState, inChar])
                elif inParseState == self._ParseState.PS_COLOUR_DIGIT0      \
                or   inParseState == self._ParseState.PS_COLOUR_DIGIT1:
                    if  inChar == ","                                       \
                    and inParseState == self._ParseState.PS_COLOUR_DIGIT0:
                        if  (inCurCol + 1) < inMaxCol                       \
                        and not inLine[inCurCol + 1] in set("0123456789"):
                            inCurColours = self._parseCharAsColourSpec(      \
                                inCurColourSpec, inCurColours)
                            inCurColourDigits = 0; inCurColourSpec = "";
                            inParseState = self._ParseState.PS_CHAR
                        else:
                            inCurCol += 1
                            inCurColourDigits = 0; inCurColourSpec += inChar;
                            inParseState = self._ParseState.PS_COLOUR_DIGIT1
                    elif inChar in set("0123456789")                        \
                    and  inCurColourDigits == 0:
                        inCurCol += 1
                        inCurColourDigits += 1; inCurColourSpec += inChar;
                    elif inChar in set("0123456789")                        \
                    and  inCurColourDigits == 1                             \
                    and  inCurColourSpec[-1] == "0":
                        inCurCol += 1
                        inCurColourDigits += 1; inCurColourSpec += inChar;
                    elif inChar in set("012345")                            \
                    and  inCurColourDigits == 1                             \
                    and  inCurColourSpec[-1] == "1":
                        inCurCol += 1
                        inCurColourDigits += 1; inCurColourSpec += inChar;
                    else:
                        inCurColours = self._parseCharAsColourSpec(         \
                            inCurColourSpec, inCurColours)
                        inCurColourDigits = 0; inCurColourSpec = "";
                        inParseState = self._ParseState.PS_CHAR
            inMaxCols = max(inMaxCols, inRowCols)
            inLine = self.inFile.readline()
        inSize[0] = inMaxCols; self.inSize = inSize; self.outMap = outMap;
        self.inFile.close()
    # }}}
    # {{{ __init__(self, inFile): initialisation method
    def __init__(self, inFile):
        self.inFile = inFile; self.inSize = self.outMap = None;
        self.fromTextFile(inFile)
    # }}}

class MawjFrame(wx.Frame):
    """XXX"""

    # {{{ __init__(self, parent, size, videoPath=None): initialisation method
    def __init__(self, parent, size, videoPath=None):
        super().__init__(parent, size=size)
        self.panelSkin = wx.Panel(self, wx.ID_ANY)
        self.panelGLCanvas = MawjGLCanvasPanel(self.panelSkin, size=[s-128 for s in size], videoPath=videoPath)
        self.Bind(wx.EVT_MOUSEWHEEL, self.panelGLCanvas.onMouseWheel)
        self.SetFocus(); self.Show(True);
    # }}}

class MawjGLCanvasPanel(wx.glcanvas.GLCanvas, wx.Panel):
    """XXX"""

    # {{{ drawAll(self, deltaX=0, deltaY=0, deltaZ=0, paintFlag=False): XXX
    def drawAll(self, deltaX=0, deltaY=0, deltaZ=0, paintFlag=False):
        self.SetCurrent(self.glContext)
        if not self.hasGLInit:
            self.onGLInit(); self.hasGLInit = True;
        if deltaX != 0 or deltaY != 0 or deltaZ != 0 or paintFlag:
            self.isDirty = True
        if self.isDirty:
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glBegin(GL_QUADS)
            curPos = [0,0,0]; cubeSize = (0.1,0.2);
            for numRow in range(len(self.MiRCART.outMap)):
                for numCol in range(len(self.MiRCART.outMap[numRow])):
                    cubeColour = MiRCARTColours[self.MiRCART.outMap[numRow][numCol][1]]
                    self.drawIrcCube(colour=cubeColour, pos=curPos, size=cubeSize)
                    curPos[0] += cubeSize[0]
                curPos[0] = 0; curPos[1] -= cubeSize[1];
            glEnd()
            if deltaX != 0 or deltaY != 0:
                w, h = self.GetClientSize(); w = max(w, 1.0); h = max(h, 1.0);
                glRotatef(deltaY * (180.0/h), 1.0, 0.0, 0.0)
                glRotatef(deltaX * (180.0/w), 0.0, 1.0, 0.0)
            if deltaZ != 0:
                glTranslatef(0, 0, deltaZ)
            self.isDirty = False; self.SwapBuffers(); self.snap();
    # }}}
    # {{{ drawIrcCube(self, colour=(1.0, 0.0, 0.0), pos=(0,0,0), size=(0.1,0.2)): XXX
    def drawIrcCube(self, colour=(1.0, 0.0, 0.0), pos=(0,0,0), size=(0.1,0.2)):
        # Top Right, Top Left, Bottom Left, Bottom Right
        glColor3f(*colour)
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(pos[0],          pos[1],         pos[2])
        glVertex3f(pos[0]-size[0],  pos[1],         pos[2])
        glVertex3f(pos[0]-size[0],  pos[1]-size[1], pos[2])
        glVertex3f(pos[0],          pos[1]-size[1], pos[2])
    # }}}
    # {{{ onGLInit(self): XXX
    def onGLInit(self):
        # <https://www.opengl.org/discussion_boards/showthread.php/125843-default-camera?p=954801&viewfull=1#post954801>
        glViewport(0, 0, *self.curSize)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity(); glFrustum(-1, 1, -1, 1, 1, 100);
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0, 0, 0, 1); glClearDepth(1);
        glTranslatef(-5.0, 3.0, -5)

        # <https://www.khronos.org/opengl/wiki/How_lighting_works#Good_Settings.>
        glLight(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
        glLight(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glLight(GL_LIGHT0, GL_POSITION, (1, 1, 0+2, 0))
        glLight(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 1))
        glEnable(GL_LIGHTING); glEnable(GL_LIGHT0);
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        if self.videoPath != None:
            width, height = self.GetClientSize()
            fourcc = cv2.VideoWriter_fourcc("X", "V", "I", "D")
            self.videoWriter = cv2.VideoWriter(self.videoPath, fourcc, 25, (width, height), True)
    # }}}
    # {{{ onMouseDown(self, event): XXX
    def onMouseDown(self, event):
        self.CaptureMouse(); self.mouseXlast, self.mouseYlast = event.GetPosition();
    # }}}
    # {{{ onMouseMotion(self, event): XXX
    def onMouseMotion(self, event):
        if event.Dragging():
            if event.LeftIsDown():
                mouseX, mouseY = event.GetPosition()
                self.drawAll(deltaX=mouseX-self.mouseXlast, deltaY=mouseY-self.mouseYlast)
                self.mouseXlast, self.mouseYlast = mouseX, mouseY
            elif event.RightIsDown():
                mouseX, mouseY = event.GetPosition()
                self.swirlAll(2, 30.0)
                self.drawAll(paintFlag=True)
                self.mouseXlast, self.mouseYlast = mouseX, mouseY
    # }}}
    # {{{ onMouseWheel(self, event): XXX
    def onMouseWheel(self, event):
        wheelRotation = event.GetWheelRotation()
        if wheelRotation < 0:
            self.drawAll(deltaZ=-1)
        else:
            self.drawAll(deltaZ=1)
    # }}}
    # {{{ onMouseUp(self, event): XXX
    def onMouseUp(self, event):
        self.ReleaseMouse(); self.mouseXlast = self.mouseYlast = 0;
    # }}}
    # {{{ onPaint(self, event): XXX
    def onPaint(self, event):
        eventDc = wx.PaintDC(self)
        eventUpdates = wx.RegionIterator(self.GetUpdateRegion())
        paintFlag = True if eventUpdates.HaveRects() else False
        self.drawAll(paintFlag=paintFlag)
    # }}}
    # {{{ snap(self): XXX
    def snap(self):
        width, height = self.GetClientSize()
        if sys.byteorder == "little":
            screenshot = glReadPixels(0, 0, width, height, GL_BGR, GL_UNSIGNED_BYTE)
        else:
            screenshot = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        screenshot = numpy.flipud(numpy.frombuffer(screenshot, numpy.uint8).reshape((height, width, 3)))
        self.videoWriter.write(screenshot)
    # }}}
    # {{{ swirlAll(self, radiusDiv=4, step=30.0): XXX
    def swirlAll(self, radiusDiv=4, step=30.0):
        # <http://geekofficedog.blogspot.de/2013/04/hello-swirl-swirl-effect-tutorial-in.html>
        width = len(self.MiRCART.outMap[0]); height = len(self.MiRCART.outMap);
        centerX = math.floor(width / 2); centerY = math.floor(height / 2);
        size = width if width < height else height
        radius = math.floor(size / radiusDiv)
        newMap = self.MiRCART.outMap.copy()
        for y in range(-radius, radius):
            for x in range(-radius, radius):
                # Transform the pixel cartesian coordinates (x, y) to polar coordinates (r, alpha)
                # Remember that the angle alpha is in radians, transform it to degrees
                r = math.sqrt(pow(x, 2) + pow(y, 2)); alpha = math.atan2(y, x);
                degrees = (alpha * 180.0) / math.pi

                # Shift the angle by a constant delta
                # Note the '-' sign was changed by '+' the inverted function
                degrees -= step

                # Transform back from polar coordinates to cartesian
                alpha = (degrees * math.pi) / 180.0
                newY = math.floor(r * math.sin(alpha)); newX = math.floor(r * math.cos(alpha));

                try:
                    # Calculate the pixel array position
                    # Get the new pixel location
                    srcPosY = y + centerY; srcPosX = x + centerX;
                    destPosY = newY + centerY; destPosX = newX + centerX;
                    newMap[destPosY][destPosX] = self.MiRCART.outMap[srcPosY][srcPosX]
                except IndexError:
                    continue
        self.MiRCART.outMap = newMap
    # }}}
    # {{{ __init__(self, parent, size, defaultPos=(24,24), videoPath=None): initialisation method
    def __init__(self, parent, size, defaultPos=(24,24), videoPath=None):
        super().__init__(parent, pos=defaultPos, size=size)
        self.curPos = list(defaultPos); self.curSize = list(size);

        self.glContext = wx.glcanvas.GLContext(self);
        self.hasGLInit = False; self.isDirty = True;
        self.mouseXlast = self.mouseYlast = 0;

        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseUp)
        self.Bind(wx.EVT_MOTION, self.onMouseMotion)
        self.Bind(wx.EVT_PAINT, self.onPaint)

        self.MiRCART = MawjMiRCARTImporter("puke.txt"); self.videoPath = videoPath;
    # }}}

#
# Entry point
def main(*argv):
    wxApp = wx.App(False)
    appFrame = MawjFrame(None, size=(1152,864), videoPath=os.path.join("F:\\", "mawj.avi"))
    wxApp.MainLoop()
if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
