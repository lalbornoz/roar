#!/usr/bin/env python3
#
# MiRCARTToPngFile.py -- convert ASCII w/ mIRC control codes to monospaced PNG (for EFnet #MiRCART)
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import MiRCARTCanvasImportStore
from PIL import Image, ImageDraw, ImageFont
import sys

class MiRCARTToPngFile:
    """XXX"""
    inFile = inFromTextFile = None
    outFontFilePath = outFontSize = None

    # {{{ _ColourMapBold: mIRC colour number to RGBA map given ^B (bold)
    _ColourMapBold = [
        [255, 255, 255],    # White
        [85,  85,  85],     # Grey
        [85,  85,  255],    # Light Blue
        [85,  255, 85],     # Light Green
        [255, 85,  85],     # Light Red
        [255, 85,  85],     # Light Red
        [255, 85,  255],    # Pink
        [255, 255, 85],     # Light Yellow
        [255, 255, 85],     # Light Yellow
        [85,  255, 85],     # Light Green
        [85,  255, 255],    # Light Cyan
        [85,  255, 255],    # Light Cyan
        [85,  85,  255],    # Light Blue
        [255, 85,  255],    # Pink
        [85,  85,  85],     # Grey
        [255, 255, 255],    # White
    ]
    # }}}
    # {{{ _ColourMapNormal: mIRC colour number to RGBA map given none of ^[BFV_] (bold, italic, reverse, underline)
    _ColourMapNormal = [
        [255, 255, 255],    # White
        [0,   0,   0],      # Black
        [0,   0,   187],    # Blue
        [0,   187, 0],      # Green
        [255, 85,  85],     # Light Red
        [187, 0,   0],      # Red
        [187, 0,   187],    # Purple
        [187, 187, 0],      # Yellow
        [255, 255, 85],     # Light Yellow
        [85,  255, 85],     # Light Green
        [0,   187, 187],    # Cyan
        [85,  255, 255],    # Light Cyan
        [85,  85,  255],    # Light Blue
        [255, 85,  255],    # Pink
        [85,  85,  85],     # Grey
        [187, 187, 187],    # Light Grey
    ]
    # }}}
    # {{{ _drawUnderline(self, curPos, fontSize, imgDraw, fillColour): XXX
    def _drawUnderLine(self, curPos, fontSize, imgDraw, fillColour):
        imgDraw.line(                                                       \
            xy=(curPos[0], curPos[1] + (fontSize[1] - 2),                   \
                curPos[0] + fontSize[0], curPos[1] + (fontSize[1] - 2)),    \
                fill=fillColour)
    # }}}
    # {{{ export(self, outFilePath): XXX
    def export(self, outFilePath):
        inSize = (len(self.inCanvasMap[0]), len(self.inCanvasMap))
        outSize = [a*b for a,b in zip(inSize, self.outImgFontSize)]
        outCurPos = [0, 0]
        outImg = Image.new("RGBA", outSize, (*self._ColourMapNormal[1], 255))
        outImgDraw = ImageDraw.Draw(outImg)
        for inCurRow in range(len(self.inCanvasMap)):
            for inCurCol in range(len(self.inCanvasMap[inCurRow])):
                inCurCell = self.inCanvasMap[inCurRow][inCurCol]
                outColours = [0, 0]
                if inCurCell[1] & MiRCARTCanvasImportStore.MiRCARTCanvasImportStore._CellState.CS_BOLD:
                    if inCurCell[2] != " ":
                        if inCurCell[2] == "█":
                            outColours[1] = self._ColourMapNormal[inCurCell[0][0]]
                        else:
                            outColours[0] = self._ColourMapBold[inCurCell[0][0]]
                            outColours[1] = self._ColourMapNormal[inCurCell[0][1]]
                    else:
                        outColours[1] = self._ColourMapNormal[inCurCell[0][1]]
                else:
                    if inCurCell[2] != " ":
                        if inCurCell[2] == "█":
                            outColours[1] = self._ColourMapNormal[inCurCell[0][0]]
                        else:
                            outColours[0] = self._ColourMapNormal[inCurCell[0][0]]
                            outColours[1] = self._ColourMapNormal[inCurCell[0][1]]
                    else:
                        outColours[1] = self._ColourMapNormal[inCurCell[0][1]]
                outImgDraw.rectangle((*outCurPos,           \
                    outCurPos[0] + self.outImgFontSize[0],  \
                    outCurPos[1] + self.outImgFontSize[1]), \
                    fill=(*outColours[1], 255))
                if  not inCurCell[2] in " █"                \
                and outColours[0] != outColours[1]:
                    # XXX implement italic
                    outImgDraw.text(outCurPos,              \
                        inCurCell[2], (*outColours[0], 255), self.outImgFont)
                if inCurCell[1] & MiRCARTCanvasImportStore.MiRCARTCanvasImportStore._CellState.CS_UNDERLINE:
                    outColours[0] = self._ColourMapNormal[inCurCell[0][0]]
                    self._drawUnderLine(outCurPos,          \
                        self.outImgFontSize,                \
                        outImgDraw, (*outColours[0], 255))
                outCurPos[0] += self.outImgFontSize[0];
            outCurPos[0] = 0
            outCurPos[1] += self.outImgFontSize[1]
        outImg.save(outFilePath);
    # }}}

    #
    # __init__(self, inCanvasMap, fontFilePath="DejaVuSansMono.ttf", fontSize=11): initialisation method
    def __init__(self, inCanvasMap, fontFilePath="DejaVuSansMono.ttf", fontSize=11):
        self.inCanvasMap = inCanvasMap
        self.outFontFilePath = fontFilePath; self.outFontSize = int(fontSize);
        self.outImgFont = ImageFont.truetype(           \
            self.outFontFilePath, self.outFontSize)
        self.outImgFontSize = [*self.outImgFont.getsize(" ")]
        self.outImgFontSize[1] += 3

#
# Entry point
def main(*argv):
    canvasStore = MiRCARTCanvasImportStore.MiRCARTCanvasImportStore(inFile=argv[1])
    MiRCARTToPngFile(canvasStore.outMap, *argv[3:]).export(argv[2])
if __name__ == "__main__":
    if ((len(sys.argv) - 1) < 2)\
    or ((len(sys.argv) - 1) > 4):
        print("usage: {} "                                              \
            "<MiRCART input file pathname> "                            \
            "<PNG image output file pathname> "                         \
            "[<Font file pathname; defaults to DejaVuSansMono.ttf>] "   \
            "[<Font size; defaults to 11>]".format(sys.argv[0]), file=sys.stderr)
    else:
        main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
