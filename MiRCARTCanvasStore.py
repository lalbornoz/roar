#!/usr/bin/env python3
#
# MiRCARTCanvasStore.py -- XXX
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

import base64
import io
import wx

try:
    from MiRCARTToPngFile import MiRCARTToPngFile
    haveMiRCARTToPngFile = True
except ImportError:
    haveMiRCARTToPngFile = False

try:
    import requests, urllib.request
    haveUrllib = True
except ImportError:
    haveUrllib = False

class MiRCARTCanvasStore():
    """XXX"""
    inFile = inSize = outMap = None
    parentCanvas = None

    #
    # _CellState(): Cell state
    class _CellState():
        CS_NONE             = 0x00
        CS_BOLD             = 0x01
        CS_ITALIC           = 0x02
        CS_UNDERLINE        = 0x04

    #
    # _ParseState(): Parsing loop state
    class _ParseState():
        PS_CHAR             = 1
        PS_COLOUR_DIGIT0    = 2
        PS_COLOUR_DIGIT1    = 3

    # {{{ _parseCharAsColourSpec(self, colourSpec, curColours): XXX
    def _parseCharAsColourSpec(self, colourSpec, curColours):
        if len(colourSpec) > 0:
            colourSpec = colourSpec.split(",")
            if len(colourSpec) == 2:
                return (int(colourSpec[0] or curColours[0]),    \
                    int(colourSpec[1]))
            elif len(colourSpec) == 1:
                return (int(colourSpec[0]), curColours[0])
        else:
            return (15, 1)
    # }}}
    # {{{ _flipCellStateBit(self, cellState, bit): XXX
    def _flipCellStateBit(self, cellState, bit):
        if cellState & bit:
            return cellState & ~bit
        else:
            return cellState | bit
    # }}}

    # {{{ exportPastebin(self, apiDevKey): XXX
    def exportPastebin(self, apiDevKey):
        if haveUrllib:
            outFile = io.StringIO(); self.exportTextFile(outFile);
            requestData = {                                                 \
                "api_dev_key":          self.apiDevKey,                     \
                "api_option":           "paste",                            \
                "api_paste_code":       base64.b64encode(outFile.read()),   \
                "api_paste_name":       pasteName,                          \
                "api_paste_private":    pastePrivate}
            responseHttp = requests.post("https://pastebin.com/post.php",   \
                    data=requestData)
            if responseHttp.status_code == 200:
                return responseHttp.text
            else:
                return None
        else:
            return None
    # }}}
    # {{{ exportPngFile(self): XXX
    def exportPngFile(self, pathName):
        if haveMiRCARTToPngFile:
            outFile = io.StringIO(); self.exportTextFile(outFile);
            MiRCARTToPng(outFile).export(pathName)
            return True
        else:
            return False
    # }}}
    # {{{ exportTextFile(self, outFile): XXX
    def exportTextFile(self, outFile):
        canvasMap = self.parentCanvas.canvasMap
        canvasSize = self.parentCanvas.canvasSize
        for canvasRow in range(0, canvasSize[1]):
            canvasLastColours = []
            for canvasCol in range(0, canvasSize[0]):
                canvasColColours = canvasMap[canvasRow][canvasCol][0:2]
                canvasColText = self.canvasMap[canvasRow][canvasCol][2]
            if canvasColColours != canvasLastColours:
                canvasLastColours = canvasColColours
                outFile.write("\x03" +          \
                    str(canvasColColours[0]) +  \
                    "," + str(canvasColColours[1]))
                outFile.write(canvasColText)
            outFile.write("\n")
    # }}}
    # {{{ importIntoPanel(self): XXX
    def importIntoPanel(self):
        canvasSize = self.inSize; self.parentCanvas.resize(canvasSize);
        self.parentCanvas.canvasJournal.reset()
        eventDc = wx.ClientDC(self.parentCanvas); tmpDc = wx.MemoryDC();
        tmpDc.SelectObject(self.parentCanvas.canvasBitmap)
        for numRow in range(0, len(self.outMap)):
            for numCol in range(0, len(self.outMap[numRow])):
                self.parentCanvas.onJournalUpdate(False,  \
                    (numCol, numRow), [numCol, numRow,    \
                    self.outMap[numRow][numCol][0][0],    \
                    self.outMap[numRow][numCol][0][1],    \
                    self.outMap[numRow][numCol][2]],      \
                    eventDc, tmpDc, (0, 0))
        wx.SafeYield()
    # }}}
    # {{{ importTextFile(self, pathName): XXX
    def importTextFile(self, pathName):
        self.inFile = open(pathName, "r")
        self.inSize = self.outMap = None;
        inCurColourSpec = ""; inCurRow = -1;
        inLine = self.inFile.readline()
        inSize = [0, 0]; outMap = []; inMaxCols = 0;
        while inLine:
            inCellState = self._CellState.CS_NONE
            inParseState = self._ParseState.PS_CHAR
            inCurCol = 0; inMaxCol = len(inLine);
            inCurColourDigits = 0; inCurColours = (15, 1); inCurColourSpec = "";
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
                        inCurColours = (15, 1)
                    elif inChar == "":
                        inCurColours = (inCurColours[1], inCurColours[0])
                    elif inChar == "":
                        inCellState = self._flipCellStateBit(               \
                            inCellState, self._CellState.CS_UNDERLINE)
                    else:
                        inRowCols += 1
                        outMap[inCurRow].append((inCurColours, inCellState, inChar))
                elif inParseState == self._ParseState.PS_COLOUR_DIGIT0      \
                or   inParseState == self._ParseState.PS_COLOUR_DIGIT1:
                    if  inChar == ","                                       \
                    and inParseState == self._ParseState.PS_COLOUR_DIGIT0:
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
    # {{{ importNew(self, newCanvasSize=None): XXX
    def importNew(self, newCanvasSize=None):
        if newCanvasSize != None:
            self.parentCanvas.resize(newCanvasSize)
        self.parentCanvas.canvasJournal.reset()
        self.parentCanvas.canvasMap = [[[1, 1, " "]                             \
                for x in range(self.parentCanvas.canvasSize[0])]                \
            for y in range(self.parentCanvas.canvasSize[1])]
        canvasWinSize = (                                                       \
            self.parentCanvas.cellSize[0] * self.parentCanvas.canvasSize[0],    \
            self.parentCanvas.cellSize[1] * self.parentCanvas.canvasSize[1])
        if self.parentCanvas.canvasBitmap != None:
            self.parentCanvas.canvasBitmap.Destroy()
        self.parentCanvas.canvasBitmap = wx.Bitmap(canvasWinSize)
        eventDc = wx.ClientDC(self.parentCanvas); tmpDc = wx.MemoryDC();
        tmpDc.SelectObject(self.parentCanvas.canvasBitmap)
        for numRow in range(0, len(self.parentCanvas.canvasMap)):
            for numCol in range(0, len(self.parentCanvas.canvasMap[numRow])):
                self.parentCanvas.onJournalUpdate(False,                        \
                    (numCol, numRow), [numCol, numRow, 1, 1, " "],              \
                    eventDc, tmpDc, (0, 0))
        wx.SafeYield()
    # }}}

    #
    # __init__(self, inFile=None, parentCanvas=None): initialisation method
    def __init__(self, inFile=None, parentCanvas=None):
        self.inFile = inFile; self.inSize = self.outMap = None;
        self.parentCanvas = parentCanvas
        if inFile != None:
            self.importTextFile(inFile)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
