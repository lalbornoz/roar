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
#

from OpenGL.GL import *
from PIL import Image
import cv2, numpy
import ctypes, sys
import wx, wx.glcanvas

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

        # [3]
        glLight(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
        glLight(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glLight(GL_LIGHT0, GL_POSITION, (1, 1, 0+2, 0))
        glLight(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 1))
        glEnable(GL_LIGHTING); glEnable(GL_LIGHT0);
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    # }}}
    # {{{ initTexture(self, pathName): XXX
    def initTexture(self, pathName):
        artTextureId = glGenTextures(1)
        artTextureImage = Image.open(pathName)
        artTextureImageData = numpy.array(list(artTextureImage.getdata()), numpy.uint8)

        glBindTexture(GL_TEXTURE_2D, artTextureId)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

        # [2]
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        # [4][5]
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                     artTextureImage.size[0], artTextureImage.size[1],
                     0, GL_RGBA, GL_UNSIGNED_BYTE, artTextureImageData)
        glBindTexture(GL_TEXTURE_2D, artTextureId)
        return artTextureId
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
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnable(GL_TEXTURE_2D)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glBindTexture(GL_TEXTURE_2D, artTextureId)
        glBindBuffer(GL_ARRAY_BUFFER, artVbo)
        glVertexPointer(3, GL_FLOAT, 32, ctypes.c_void_p(0))
        glNormalPointer(GL_FLOAT, 32, ctypes.c_void_p(12))
        glTexCoordPointer(2, GL_FLOAT, 32, ctypes.c_void_p(24))
        glDrawArrays(GL_QUADS, 0, artVboLen)

        glDisable(GL_TEXTURE_2D)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
    # }}}
    # {{{ renderMiRCART(self, artMap, centre=True, canvasCols=100, cubeSize=(0.1, 0.2), texelHeight=0.0625, texelWidth=0.0625): XXX
    def renderMiRCART(self, artMap, centre=True, canvasCols=100, cubeSize=(0.1, 0.2), texelHeight=0.0625, texelWidth=0.0625):
        curPos = [0, 0, 0]; vertices = []; numVertices = 0;
        for numRow in range(len(artMap)):
            if centre and (len(artMap[numRow]) < canvasCols):
                curPos[0] += (((canvasCols - len(artMap[numRow])) * cubeSize[0]) / 2)
            for numCol in range(len(artMap[numRow])):
                cubeColour = artMap[numRow][numCol][1] * texelWidth

                # Top Right
                vertices += curPos
                vertices += [0.0, 0.0, 1.0]
                vertices += [cubeColour+texelWidth, texelHeight]
                numVertices += 1

                # Top Left
                vertices += [curPos[0]-cubeSize[0], curPos[1], curPos[2]]
                vertices += [0.0, 0.0, 1.0]
                vertices += [cubeColour, texelHeight]
                numVertices += 1

                # Bottom Left
                vertices += [curPos[0]-cubeSize[0], curPos[1]-cubeSize[1], curPos[2]]
                vertices += [0.0, 0.0, 1.0]
                vertices += [cubeColour, 0.0]
                numVertices += 1

                # Bottom Right
                vertices += [curPos[0], curPos[1]-cubeSize[1], curPos[2]]
                vertices += [0.0, 0.0, 1.0]
                vertices += [cubeColour+texelWidth, 0.0]
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
