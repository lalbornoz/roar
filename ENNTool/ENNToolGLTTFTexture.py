#!/usr/bin/env python3
#
# ENNTool -- mIRC art animation tool (for EFnet #MiRCART) (WIP)
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT license.
#
# References:
# Thu, 28 Jun 2018 17:03:16 +0200 [1] <https://stackoverflow.com/questions/384759/how-to-convert-a-pil-image-into-a-numpy-array>
# Thu, 28 Jun 2018 17:04:59 +0200 [2] <https://www.khronos.org/opengl/wiki/Common_Mistakes#y-axis>
# Wed, 27 Jun 2018 16:02:12 +0200 [3] <https://www.khronos.org/opengl/wiki/How_lighting_works#Good_Settings.>
# Wed, 27 Jun 2018 16:02:13 +0200 [4] <https://www.khronos.org/opengl/wiki/Common_Mistakes>
# Wed, 27 Jun 2018 16:02:14 +0200 [5] <https://www.khronos.org/opengl/wiki/Pixel_Transfer#Pixel_layout>
# Wed, 04 Jul 2018 10:57:09 +0200 [6] <https://stackoverflow.com/questions/466204/rounding-up-to-next-power-of-2>
#

from collections import defaultdict
from OpenGL.GL import *
from PIL import Image, ImageDraw, ImageFont
import numpy
import os, string, sys
from ENNToolMiRCARTColours import ENNToolMiRCARTColours
from ENNToolMiRCARTImporter import ENNToolMiRCARTImporter

class ENNToolGLTTFTexture(object):
    """XXX"""

    # {{{ _defaultDict(*args): XXX
    @staticmethod
    def _defaultDict(*args):
        return defaultdict(*args)
    # }}}
    # {{{ _nestedDict(): XXX
    @staticmethod
    def _nestedDict():
        return defaultdict(ENNToolGLTTFTexture._nestedDict)
    # }}}
    # {{{ _drawCharList(self, artInfo, charList, pilFontBold, pilFontNormal, pilImageDraw, pilImageSize): XXX
    def _drawCharList(self, artInfo, charList, pilFontBold, pilFontNormal, pilImageDraw, pilImageSize):
        curPos = [0, 0]
        for newChar in charList:
            if newChar[2] & ENNToolMiRCARTImporter._CellState.CS_BOLD:
                pilFont, pilFontSize = pilFontBold, [pilFontBold.getsize(newChar[3])[0], pilFontBold.getsize(newChar[3])[1]]
            else:
                pilFont, pilFontSize = pilFontNormal, [pilFontNormal.getsize(newChar[3])[0], pilFontNormal.getsize(newChar[3])[1]]
            if newChar[2] & ENNToolMiRCARTImporter._CellState.CS_UNDERLINE:
                underLine = True
            else:
                underLine = False
            if newChar[3] != " ":
                pilImageDraw.text(curPos, newChar[3], (255, 255, 255, 255), pilFont)
            elif newChar[0] == newChar[1]:
                pilImageDraw.rectangle((*curPos, curPos[0] + pilFontSize[0], curPos[1] + pilFontSize[1] - 1),
                                       fill=(255, 255, 255, 255))
            if underLine and False:
                pilImageDraw.line(
                    xy=(curPos[0], curPos[1] + (pilFontSize[1] - 2),
                        curPos[0] + pilFontSize[0], curPos[1] + pilFontSize[1]),
                    fill=(*ENNToolMiRCARTColours[newChar[0]], 255))

            artInfo[newChar[2]][newChar[3]] = []
            # Top Right
            artInfo[newChar[2]][newChar[3]] += [float(curPos[0] + pilFontSize[0]) / pilImageSize[0], 0.0]
            # Top Left
            artInfo[newChar[2]][newChar[3]] += [float(curPos[0]) / pilImageSize[0], 0.0]
            # Bottom Left
            artInfo[newChar[2]][newChar[3]] += [float(curPos[0]) / pilImageSize[0], float(pilFontSize[1]) / pilImageSize[1]]
            # Bottom Right
            artInfo[newChar[2]][newChar[3]] += [float(curPos[0] + pilFontSize[0]) / pilImageSize[0], float(pilFontSize[1]) / pilImageSize[1]]

            curPos[0] += pilFontSize[0]
        return artInfo
    # }}}
    # {{{ _initArtInfoCharList(self): XXX
    def _initArtInfoCharList(self, artMap):
        artInfo, charList = ENNToolGLTTFTexture._nestedDict(), []
        for numRow in range(len(artMap)):
            for numCol in range(len(artMap[numRow])):
                artFg = artMap[numRow][numCol][0]
                artBg = artMap[numRow][numCol][1]
                artAttrs = artMap[numRow][numCol][2]
                artChar = artMap[numRow][numCol][3]
                if artInfo[artAttrs][artChar] == {}:
                    artInfo[artAttrs][artChar] = None
                    charList += [[artFg, artBg, artAttrs, artChar]]
        return artInfo, charList
    # }}}
    # {{{ _initFonts(self, charMap): XXX
    def _initFonts(self, charMap):
        fontBoldPathName = os.path.join("assets", "DejaVuSansMono-Bold.ttf")
        fontNormalPathName = os.path.join("assets", "DejaVuSansMono.ttf")
        fontSize = int("26")
        pilFontBold = ImageFont.truetype(fontBoldPathName, fontSize)
        pilFontMaxSize = [16, 32] # TODO
        pilFontNormal = ImageFont.truetype(fontNormalPathName, fontSize)
        return pilFontBold, pilFontMaxSize, pilFontNormal
    # }}}
    # {{{ _initImage(self, charList, pilFontMaxSize): XXX
    def _initImage(self, charList, pilFontMaxSize):
        pilImageSize = [pilFontMaxSize[0] * len(charList), pilFontMaxSize[1]]
        for numDim in range(len(pilImageSize)):
            if (pilImageSize[numDim] & (pilImageSize[numDim] - 1)) != 0:
                pilImageSize[numDim] -= 1
                pilImageSize[numDim] |= pilImageSize[numDim] >> 1
                pilImageSize[numDim] |= pilImageSize[numDim] >> 2
                pilImageSize[numDim] |= pilImageSize[numDim] >> 4
                pilImageSize[numDim] |= pilImageSize[numDim] >> 8
                pilImageSize[numDim] |= pilImageSize[numDim] >> 16
                pilImageSize[numDim] += 1
        pilImage = Image.new("RGBA", pilImageSize, (0, 0, 0, 0))
        pilImageDraw = ImageDraw.Draw(pilImage)
        return pilImage, pilImageDraw, pilImageSize
    # }}}
    # {{{ _initTexture(self, pilImage): XXX
    def _initTexture(self, pilImage):
        # [1], [2]
        artTextureId = glGenTextures(1)
        artTextureImage = pilImage
        artTextureImageData = numpy.array(artTextureImage)

        glBindTexture(GL_TEXTURE_2D, artTextureId)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

        # [3]
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        # [4][5]
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                     artTextureImage.size[0], artTextureImage.size[1],
                     0, GL_RGBA, GL_UNSIGNED_BYTE, artTextureImageData)

        glBindTexture(GL_TEXTURE_2D, 0)
        return artTextureId
    # }}}
    # {{{ getParams(self): XXX
    def getParams(self):
        return self.artTextureId, self.artInfo
    # }}}
    # {{{ __init__(self): initialisation method
    def __init__(self, artMap, cubeSize, videoSize):
        artInfo, charList = self._initArtInfoCharList(artMap)
        pilFontBold, pilFontMaxSize, pilFontNormal = self._initFonts(charList)
        pilImage, pilImageDraw, pilImageSize = self._initImage(charList, pilFontMaxSize)
        artInfo = self._drawCharList(artInfo, charList, pilFontBold, pilFontNormal, pilImageDraw, pilImageSize)
        artTextureId = self._initTexture(pilImage)
        self.artTextureId = artTextureId
        self.artInfo = artInfo
    # }}}

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
