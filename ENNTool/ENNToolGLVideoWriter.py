#!/usr/bin/env python3
#
# ENNTool -- mIRC art animation tool (for EFnet #MiRCART) (WIP)
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT license.
#
# References:
# Tue, 03 Jul 2018 20:35:52 +0200 [1] <https://stackoverflow.com/questions/23930671/how-to-create-n-dim-numpy-array-from-a-pointer>
# Wed, 04 Jul 2018 10:02:22 +0200 [2] <http://www.songho.ca/opengl/gl_pbo.html>
#

from OpenGL.GL import *
import ctypes, cv2, numpy

class ENNToolGLVideoWriter(object):
    """XXX"""

    # {{{ _copyFrames(self): XXX
    def _copyFrames(self):
        for numPbo in range(self.pboCount):
            glBindBuffer(GL_PIXEL_PACK_BUFFER, self.pboList[numPbo])
            frameBufferPtr = glMapBuffer(GL_PIXEL_PACK_BUFFER, GL_READ_ONLY)
            frameBufferPtr = ctypes.cast(frameBufferPtr, ctypes.POINTER(ctypes.c_ubyte))
            frameBuffer = numpy.ctypeslib.as_array(frameBufferPtr, shape=(self.videoSize[1], self.videoSize[0], 3))
            frameBuffer = numpy.flipud(frameBuffer)
            self.videoWriter.write(frameBuffer)
            glUnmapBuffer(GL_PIXEL_PACK_BUFFER)
    # }}}
    # {{{ _initCv2(self, videoFps, videoPath, videoSize): XXX
    def _initCv2(self, videoFps, videoPath, videoSize):
        fourcc = cv2.VideoWriter_fourcc(*"avc1")
        videoWriter = cv2.VideoWriter(videoPath, fourcc, videoFps, tuple(videoSize), True)
        return videoWriter
    # }}}
    # {{{ _initPbos(self, pboCount, videoSize): XXX
    def _initPbos(self, pboCount, videoSize):
        pboBufs, pboCur, pboList = [None] * pboCount, 0, [None] * pboCount
        for numPbo in range(pboCount):
            pboList[numPbo] = glGenBuffers(1)
            glBindBuffer(GL_PIXEL_PACK_BUFFER, pboList[numPbo])
            glBufferData(GL_PIXEL_PACK_BUFFER,
                         videoSize[0] * videoSize[1] * 3, None, GL_STREAM_READ)
        glBindBuffer(GL_PIXEL_PACK_BUFFER, 0)
        return pboBufs, pboCount, pboCur, pboList
    # }}}
    # {{{ saveFrame(self): XXX
    def saveFrame(self):
        glBindBuffer(GL_PIXEL_PACK_BUFFER, self.pboList[self.pboCur])
        glReadPixels(0, 0, self.videoSize[0], self.videoSize[1], GL_BGR, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))
        self.pboCur += 1
        if self.pboCur >= self.pboCount:
            self._copyFrames(); self.pboCur = 0;
        glBindBuffer(GL_PIXEL_PACK_BUFFER, 0)
    # }}}
    # {{{ saveVideo(self): XXX
    def saveVideo(self):
        return
    # }}}
    # {{{ __init__(self, videoPath, videoSize, videoFps=25): XXX
    def __init__(self, videoPath, videoSize, videoFps=25):
        videoWriter = self._initCv2(videoFps, videoPath, videoSize)
        self.pboBufs, self.pboCount,    \
        self.pboCur, self.pboList = self._initPbos(videoFps, videoSize)
        self.videoFps, self.videoPath,  \
        self.videoSize, self.videoWriter = videoFps, videoPath, videoSize, videoWriter
    # }}}

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
