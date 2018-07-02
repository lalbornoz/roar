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
#

from OpenGL.GL import *
from OpenGL.GL import shaders
import cv2, numpy
import ctypes, os, sys, time
import wx, wx.glcanvas

from ENNToolMiRCARTColours import ENNToolMiRCARTColoursFloat

class ENNToolGLCanvasPanel(wx.glcanvas.GLCanvas, wx.Panel):
    """XXX"""

    # {{{ initOpenGL(self): XXX
    def initOpenGL(self):
        self.glContext = wx.glcanvas.GLContext(self)
        self.SetCurrent(self.glContext)

        # [1]
        glViewport(0, 0, *self.curSize)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity(); glFrustum(-1, 1, -1, 1, 1, 100);
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0, 0, 0, 1); glClearDepth(1);
        glTranslatef(-5.0, 3.0, -5)
    # }}}
    # {{{ initShaders(self): XXX
    def initShaders(self):
        fs = shaders.compileShader("""
            #version 330 core

            in vec4 bgColour;
            in vec2 fgTexCoord;
            uniform sampler2D texture;

            void main() {
                vec4 texel = texture2D(texture, fgTexCoord);
                gl_FragColor = vec4(texel.r, texel.g, texel.b, 1.0);
            }
            """, GL_FRAGMENT_SHADER)
        vs = shaders.compileShader("""
            #version 330 core

            layout(location = 0) in vec4 vertex;
            layout(location = 1) in vec3 normal;
            layout(location = 2) in vec4 colour;
            layout(location = 3) in vec2 texcoord;

            out vec4 bgColour;
            out vec2 fgTexCoord;

            uniform mat4 model;
            uniform mat4 projection;

            void main() {
                gl_Position = projection * model * vertex;
                bgColour = colour;
                fgTexCoord = texcoord;
            }
            """, GL_VERTEX_SHADER)
        self.shader = shaders.compileProgram(vs, fs)
    # }}}
    # {{{ initVideoWriter(self): XXX
    def initVideoWriter(self, fourcc="XVID", fps=25):
        fourcc = cv2.VideoWriter_fourcc(*list(fourcc))
        self.videoWriter = cv2.VideoWriter(self.videoPath, fourcc, fps, (self.width, self.height), True)
    # }}}

    # {{{ renderFrame(self, artTextureId, artVbo, artVboLen): XXX
    def renderFrame(self, artTextureId, artVbo, artVboLen):
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnable(GL_TEXTURE_2D)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBindTexture(GL_TEXTURE_2D, artTextureId)
        glBindBuffer(GL_ARRAY_BUFFER, artVbo)

        glUseProgram(self.shader)
        model = (GLfloat * 16)()
        glGetFloatv(GL_MODELVIEW_MATRIX, model)
        projection = (GLfloat * 16)()
        glGetFloatv(GL_PROJECTION_MATRIX, projection)
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "model"), 1, GL_FALSE, model)
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"), 1, GL_FALSE, projection)
        glUniform1i(glGetUniformLocation(self.shader, "texture"), 0)

        # [6]
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 48, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, False, 48, ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 4, GL_FLOAT, False, 48, ctypes.c_void_p(24))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 2, GL_FLOAT, False, 48, ctypes.c_void_p(40))

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glVertexPointer(3, GL_FLOAT, 48, ctypes.c_void_p(0))
        glNormalPointer(GL_FLOAT, 48, ctypes.c_void_p(12))
        glColorPointer(4, GL_FLOAT, 48, ctypes.c_void_p(24))
        glTexCoordPointer(2, GL_FLOAT, 48, ctypes.c_void_p(40))
        glDrawArrays(GL_QUADS, 0, artVboLen)

        glDisableVertexAttribArray(0)
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
    # }}}
    # {{{ renderMiRCART(self, artInfo, artMap, centre=True, canvasCols=100, cubeSize=(0.1, 0.2)): XXX
    def renderMiRCART(self, artInfo, artMap, centre=True, canvasCols=100, cubeSize=(0.1, 0.2)):
        curPos = [0, 0, 0]; vertices = []; numVertices = 0;
        for numRow in range(len(artMap)):
            if centre and (len(artMap[numRow]) < canvasCols):
                curPos[0] += (((canvasCols - len(artMap[numRow])) * cubeSize[0]) / 2)
            for numCol in range(len(artMap[numRow])):
                cubeFg = artMap[numRow][numCol][0]
                cubeBg = artMap[numRow][numCol][1]
                cubeBgFloat = [*ENNToolMiRCARTColoursFloat[cubeBg], 1.0]
                cubeAttrs = artMap[numRow][numCol][2]
                cubeChar = artMap[numRow][numCol][3]
                artCell = artInfo[cubeFg][cubeBg][cubeAttrs][cubeChar]

                # Top Right
                vertices += curPos
                vertices += [0.0, 0.0, 1.0]
                vertices += cubeBgFloat
                vertices += artCell[0:2]
                numVertices += 1

                # Top Left
                vertices += [curPos[0]-cubeSize[0], curPos[1], curPos[2]]
                vertices += [0.0, 0.0, 1.0]
                vertices += cubeBgFloat
                vertices += artCell[2:4]
                numVertices += 1

                # Bottom Left
                vertices += [curPos[0]-cubeSize[0], curPos[1]-cubeSize[1], curPos[2]]
                vertices += [0.0, 0.0, 1.0]
                vertices += cubeBgFloat
                vertices += artCell[4:6]
                numVertices += 1

                # Bottom Right
                vertices += [curPos[0], curPos[1]-cubeSize[1], curPos[2]]
                vertices += [0.0, 0.0, 1.0]
                vertices += cubeBgFloat
                vertices += artCell[6:8]
                numVertices += 1

                curPos[0] += cubeSize[0]
            curPos[0], curPos[1] = 0, curPos[1] - cubeSize[1]

        artVbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, artVbo)
        glBufferData(GL_ARRAY_BUFFER,
                     (ctypes.c_float*len(vertices))(*vertices),
                     GL_STATIC_DRAW)
        return artVbo, len(vertices), -curPos[1], numVertices
    # }}}
    # {{{ saveFrame(self): XXX
    def saveFrame(self):
        if sys.byteorder == "little":
            screenshot = glReadPixels(0, 0, self.width, self.height, GL_BGR, GL_UNSIGNED_BYTE)
        else:
            screenshot = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        screenshot = numpy.flipud(numpy.frombuffer(screenshot, numpy.uint8).reshape((self.height, self.width, 3)))
        self.videoWriter.write(screenshot)
    # }}}

    # {{{ __init__(self, parent, size, defaultPos=(24,24), videoPath=None): initialisation method
    def __init__(self, parent, size, defaultPos=(24,24), videoPath=None):
        super().__init__(parent, pos=defaultPos, size=size)
        self.curPos = list(defaultPos); self.curSize = list(size);
        self.width, self.height = self.GetClientSize()
        self.videoPath = videoPath
    # }}}

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
