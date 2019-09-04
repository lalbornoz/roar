#!/usr/bin/env python3
#
# MiRCARTToPngFile.py -- convert ASCII w/ mIRC control codes to monospaced PNG (for EFnet #MiRCART)
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

import os, sys
[sys.path.append(os.path.join(os.getcwd(), "..", "..", path)) for path in ["libcanvas", "librtl", "libtools"]]

from CanvasImportStore import CanvasImportStore
from getopt import getopt, GetoptError
from PIL import Image, ImageDraw, ImageFont

class MiRCARTToPngFile:
    """XXX"""
    inFile = inFromTextFile = None
    outFontFilePath = outFontSize = None

    # {{{ _ColourMapBold: mIRC colour number to RGBA map given ^B (bold)
    _ColourMapBold = [
        [255, 255, 255],    # Bright White
        [85,  85,  85],     # Black
        [85,  85,  255],    # Light Blue
        [85,  255, 85],     # Green
        [255, 85,  85],     # Red
        [255, 85,  85],     # Light Red
        [255, 85,  255],    # Pink
        [255, 255, 85],     # Yellow
        [255, 255, 85],     # Light Yellow
        [85,  255, 85],     # Light Green
        [85,  255, 255],    # Cyan
        [85,  255, 255],    # Light Cyan
        [85,  85,  255],    # Blue
        [255, 85,  255],    # Light Pink
        [85,  85,  85],     # Grey
        [255, 255, 255],    # Light Grey
    ]
    # }}}
    # {{{ _ColourMapNormal: mIRC colour number to RGBA map given none of ^[BFV_] (bold, italic, reverse, underline)
    _ColourMapNormal = [
        [255, 255, 255],    # Bright White
        [0,   0,   0],      # Black
        [0,   0,   187],    # Light Blue
        [0,   187, 0],      # Green
        [255, 85,  85],     # Red
        [187, 0,   0],      # Light Red
        [187, 0,   187],    # Pink
        [187, 187, 0],      # Yellow
        [255, 255, 85],     # Light Yellow
        [85,  255, 85],     # Light Green
        [0,   187, 187],    # Cyan
        [85,  255, 255],    # Light Cyan
        [85,  85,  255],    # Blue
        [255, 85,  255],    # Light Pink
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
        outImgDraw.fontmode = "1"
        for inCurRow in range(len(self.inCanvasMap)):
            for inCurCol in range(len(self.inCanvasMap[inCurRow])):
                inCurCell = self.inCanvasMap[inCurRow][inCurCol]
                outColours = [0, 0]
                if inCurCell[2] & CanvasImportStore._CellState.CS_BOLD:
                    if inCurCell[3] != " ":
                        if inCurCell[3] == "█":
                            outColours[1] = self._ColourMapNormal[inCurCell[0]]
                        else:
                            outColours[0] = self._ColourMapBold[inCurCell[0]]
                            outColours[1] = self._ColourMapNormal[inCurCell[1]]
                    else:
                        outColours[1] = self._ColourMapNormal[inCurCell[1]]
                else:
                    if inCurCell[3] != " ":
                        if inCurCell[3] == "█":
                            outColours[1] = self._ColourMapNormal[inCurCell[0]]
                        else:
                            outColours[0] = self._ColourMapNormal[inCurCell[0]]
                            outColours[1] = self._ColourMapNormal[inCurCell[1]]
                    else:
                        outColours[1] = self._ColourMapNormal[inCurCell[1]]
                outImgDraw.rectangle((*outCurPos,           \
                    outCurPos[0] + self.outImgFontSize[0],  \
                    outCurPos[1] + self.outImgFontSize[1]), \
                    fill=(*outColours[1], 255))
                if  not inCurCell[3] in " █"                \
                and outColours[0] != outColours[1]:
                    # XXX implement italic
                    outImgDraw.text(outCurPos,              \
                        inCurCell[3], (*outColours[0], 255), self.outImgFont)
                if inCurCell[2] & CanvasImportStore._CellState.CS_UNDERLINE:
                    outColours[0] = self._ColourMapNormal[inCurCell[0]]
                    self._drawUnderLine(outCurPos,          \
                        self.outImgFontSize,                \
                        outImgDraw, (*outColours[0], 255))
                outCurPos[0] += self.outImgFontSize[0];
            outCurPos[0] = 0
            outCurPos[1] += self.outImgFontSize[1]
        outImg.save(outFilePath);
    # }}}

    #
    # __init__(self, inCanvasMap, fontFilePath, fontSize): initialisation method
    def __init__(self, inCanvasMap, fontFilePath, fontSize):
        self.inCanvasMap = inCanvasMap
        self.outFontFilePath, self.outFontSize = fontFilePath, fontSize
        self.outImgFont = ImageFont.truetype(self.outFontFilePath, self.outFontSize)
        self.outImgFontSize = [*self.outImgFont.getsize(" ")]
        self.outImgFontSize[1] += 3

#
# Entry point
def main(*argv):
    argv0 = argv[0]; optlist, argv = getopt(argv[1:], "f:hs:"); optdict = dict(optlist);
    if len(argv) < 1:
        print("""usage: {} [-f fname] [-h] [-s size] fname...
       -h.........: show this screen
       -f fname...: font file pathname (defaults to: ../fonts/DejaVuSansMono.ttf)
       -s size....: font size (defaults to: 11)""".format(argv0), file=sys.stderr)
    else:
        if not "-f" in optdict:
            optdict["-f"] = os.path.join("..", "fonts", "DejaVuSansMono.ttf")
        optdict["-s"] = 11 if not "-s" in optdict else int(optdict["-s"])
        for inFile in argv:
            canvasStore, outFile = CanvasImportStore(inFile=inFile), os.path.splitext(inFile)[0] + ".png"
            MiRCARTToPngFile(canvasStore.outMap, fontFilePath=optdict["-f"], fontSize=optdict["-s"]).export(outFile)
if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
