#!/usr/bin/env python3
#
# ENNTool -- mIRC art animation tool (for EFnet #MiRCART) (WIP)
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT license.
#
# References:
# Wed, 27 Jun 2018 16:02:10 +0200 [1] <https://www.opengl.org/discussion_boards/showthread.php/125843-default-camera?p=954801&viewfull=1#post954801>
# Wed, 27 Jun 2018 16:02:11 +0200 [2] <https://www.opengl.org/discussion_boards/showthread.php/167808-2D-texture-problem-lines-between-textures>
# Wed, 27 Jun 2018 16:02:12 +0200 [3] <https://www.khronos.org/opengl/wiki/How_lighting_works#Good_Settings.>
# Wed, 27 Jun 2018 16:02:13 +0200 [4] <https://www.khronos.org/opengl/wiki/Common_Mistakes>
# Wed, 27 Jun 2018 16:02:14 +0200 [5] <https://www.khronos.org/opengl/wiki/Pixel_Transfer#Pixel_layout>
# Thu, 28 Jun 2018 18:32:50 +0200 [6] <https://stackoverflow.com/questions/18935203/shader-position-vec4-or-vec3>
# Tue, 03 Jul 2018 14:34:57 +0200 [7] <https://gamedev.stackexchange.com/questions/107793/binding-and-unbinding-what-would-you-do>
#

from ENNToolMiRCARTColours import ENNToolMiRCARTColoursFloat
from OpenGL.GL import *
from OpenGL.GL import shaders
import ctypes, wx, wx.glcanvas

class ENNToolGLCanvas(wx.glcanvas.GLCanvas):
    # {{{ initOpenGL(self, cameraPos=(-5.0, 3.0, -5)): XXX
    def initOpenGL(self, cameraPos=(-5.0, 3.0, -5)):
        self.glContext = wx.glcanvas.GLContext(self)
        self.SetCurrent(self.glContext)

        # [1]
        glViewport(0, 0, *self.curSize)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity(); glFrustum(-1, 1, -1, 1, 1, 100);
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glTranslatef(*cameraPos)
    # }}}
    # {{{ initShaders(self): XXX
    def initShaders(self):
        # Fragment shader
        fs = shaders.compileShader("""
            #version 330 core

            in vec2 frgTexCoord;
            in vec3 frgFgColour;
            in vec3 frgBgColour;
            uniform sampler2D texture;

            layout(location = 0) out vec4 fragColour;

            void main() {
                vec4 texel = texture2D(texture, frgTexCoord);
                if (texel.r == 0.0 && texel.g == 0.0 && texel.b == 0.0 && texel.a == 0.0) {
                    fragColour = vec4(frgBgColour.r, frgBgColour.g, frgBgColour.b, 1.0);
                } else {
                    fragColour = vec4(frgFgColour.r, frgFgColour.g, frgFgColour.b, 1.0);
                }
            }
            """, GL_FRAGMENT_SHADER)

        # Vertex shader
        vs = shaders.compileShader("""
            #version 330 core

            layout(location = 0) in vec4 vertex;
            layout(location = 1) in vec2 texcoord;
            layout(location = 2) in vec3 vexFgColour;
            layout(location = 3) in vec3 vexBgColour;

            out vec2 frgTexCoord;
            out vec3 frgFgColour;
            out vec3 frgBgColour;

            uniform mat4 modelview;
            uniform mat4 projection;

            void main() {
                gl_Position = projection * modelview * vertex;
                frgTexCoord = texcoord;
                frgFgColour = vexFgColour;
                frgBgColour = vexBgColour;
            }
            """, GL_VERTEX_SHADER)
        self.shader = shaders.compileProgram(vs, fs)
    # }}}
    # {{{ renderFrame(self, artTextureId, artVbo, artVboLen): XXX
    def renderFrame(self, artTextureId, artVbo, artVboLen):
        # Bind VBO and named texture & install shader program object
        glBindBuffer(GL_ARRAY_BUFFER, artVbo)
        glBindTexture(GL_TEXTURE_2D, artTextureId)
        glUseProgram(self.shader)

        # Specify modelview and projection matrix & texture unit uniforms for shader programs
        modelview, projection = (GLfloat * 16)(), (GLfloat * 16)()
        glGetFloatv(GL_MODELVIEW_MATRIX, modelview)
        glGetFloatv(GL_PROJECTION_MATRIX, projection)
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "modelview"), 1, GL_FALSE, modelview)
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"), 1, GL_FALSE, projection)
        glUniform1i(glGetUniformLocation(self.shader, "texture"), 0)

        # VBO vertices location
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 44, ctypes.c_void_p(0))
        glVertexPointer(3, GL_FLOAT, 44, ctypes.c_void_p(0))

        # VBO texture coordinates
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 44, ctypes.c_void_p(12))
        glTexCoordPointer(2, GL_FLOAT, 44, ctypes.c_void_p(12))

        # VBO foreground colours
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, False, 44, ctypes.c_void_p(20))
        glTexCoordPointer(3, GL_FLOAT, 44, ctypes.c_void_p(20))

        # VBO background colours
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, False, 44, ctypes.c_void_p(32))
        glTexCoordPointer(3, GL_FLOAT, 44, ctypes.c_void_p(32))

        # Clear colour and depth buffer, draw quads from VBO & clear state
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDrawArrays(GL_QUADS, 0, artVboLen)
        glDisableVertexAttribArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)
    # }}}
    # {{{ renderMiRCART(self, artInfo, artMap, centre=True, canvasCols=100, cubeSize=(0.1, 0.2)): XXX
    def renderMiRCART(self, artInfo, artMap, centre=True, canvasCols=100, cubeSize=(0.1, 0.2)):
        curPos, vertices, numVertices = [0, 0, 0], [], 0
        for numRow in range(len(artMap)):
            if centre and (len(artMap[numRow]) < canvasCols):
                curPos[0] += (((canvasCols - len(artMap[numRow])) * cubeSize[0]) / 2)
            for numCol in range(len(artMap[numRow])):
                cubeFg = artMap[numRow][numCol][0]
                cubeBg = artMap[numRow][numCol][1]
                cubeAttrs = artMap[numRow][numCol][2]
                cubeChar = artMap[numRow][numCol][3]
                artCell = artInfo[cubeAttrs][cubeChar]

                # Top Right, Top Left
                vertices += curPos
                vertices += artCell[0:2]
                vertices += [*ENNToolMiRCARTColoursFloat[cubeFg]]
                vertices += [*ENNToolMiRCARTColoursFloat[cubeBg]]
                vertices += [curPos[0] - cubeSize[0], curPos[1], curPos[2]]
                vertices += artCell[2:4]
                vertices += ENNToolMiRCARTColoursFloat[cubeFg]
                vertices += ENNToolMiRCARTColoursFloat[cubeBg]

                # Bottom Left, Bottom Right
                vertices += [curPos[0] - cubeSize[0], curPos[1] - cubeSize[1], curPos[2]]
                vertices += artCell[4:6]
                vertices += [*ENNToolMiRCARTColoursFloat[cubeFg]]
                vertices += [*ENNToolMiRCARTColoursFloat[cubeBg]]
                vertices += [curPos[0], curPos[1] - cubeSize[1], curPos[2]]
                vertices += artCell[6:8]
                vertices += ENNToolMiRCARTColoursFloat[cubeFg]
                vertices += ENNToolMiRCARTColoursFloat[cubeBg]

                curPos[0], numVertices = curPos[0] + cubeSize[0], numVertices + 4
            curPos[0], curPos[1] = 0, curPos[1] - cubeSize[1]

        artVbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, artVbo)
        glBufferData(GL_ARRAY_BUFFER,
                     (ctypes.c_float*len(vertices))(*vertices),
                     GL_STATIC_DRAW)
        return artVbo, len(vertices), -curPos[1], numVertices
    # }}}
    # {{{ __init__(self, parentCanvas, size): initialisation method
    def __init__(self, parentCanvas, size):
        super().__init__(parentCanvas, size=size)
        self.curSize = list(size)
        self.parentCanvas = parentCanvas
    # }}}

class ENNToolGLPanel(wx.Panel):
    """XXX"""

    # {{{ onPaint(self, event): XXX
    def onPaint(self, event):
        eventDc = wx.PaintDC(self)
        eventUpdates = wx.RegionIterator(self.GetUpdateRegion())
        paintFlag = True if eventUpdates.HaveRects() else False
        if self.frameFun != None:
            self.frameFun()
    # }}}
    # {{{ onTimer(self, event): XXX
    def onTimer(self, event):
        if self.frameFun != None:
            if not self.frameFun():
                event.GetTimer().Stop()
                event.GetTimer().Destroy()
    # }}}
    # {{{ __init__(self, parent, size, defaultPos=(24,24), parentFrame=None): initialisation method
    def __init__(self, parent, size, defaultPos=(24,24), parentFrame=None):
        super().__init__(parent, pos=defaultPos, size=size)
        self.curPos = list(defaultPos); self.curSize = list(size);
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.frameFun = None
        self.timerTimer = wx.Timer(self, 1)
        self.timerTimer.Start(40)
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timerTimer)
    # }}}

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
