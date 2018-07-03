#!/usr/bin/env python3
#
# ENNTool -- mIRC art animation tool (for EFnet #MiRCART) (WIP)
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT license.
#

from OpenGL.GL import *
import numpy, subprocess

class ENNToolGLVideoWriter(object):
    """XXX"""

    # {{{ saveFrame(self): XXX
    def saveFrame(self):
        frameBuffer = glReadPixels(0, 0, self.videoSize[0], self.videoSize[1], GL_RGB, GL_UNSIGNED_BYTE)
        frameBuffer = numpy.frombuffer(frameBuffer, numpy.uint8)
        frameBuffer = frameBuffer.reshape((self.videoSize[1], self.videoSize[0], 3))
        frameBuffer = numpy.flipud(frameBuffer)
        self.videoFrames += [frameBuffer]
    # }}}
    # {{{ saveVideo(self): XXX
    def saveVideo(self):
        with subprocess.Popen([
                "FFmpeg.exe",
                "-pix_fmt", "rgb24",
                "-r",       str(self.videoFps),
                "-s",       "x".join([str(r) for r in self.videoSize]),
                "-vcodec",  "rawvideo",
                "-f",       "rawvideo",
                "-i",       "-",
                "-an",
                "-y",
                self.videoPath], stdin=subprocess.PIPE) as procObject:
            for videoFrame in self.videoFrames:
                procObject.stdin.write(videoFrame.tobytes())
    # }}}
    # {{{ __init__(self, videoPath, videoSize, videoFps=25): XXX
    def __init__(self, videoPath, videoSize, videoFps=25):
        self.videoFps, self.videoPath, self.videoSize = videoFps, videoPath, videoSize
        self.videoFrames = []
    # }}}

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
