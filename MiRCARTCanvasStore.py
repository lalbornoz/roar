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

import io, os, tempfile

try:
    import wx
    haveWx = True
except ImportError:
    haveWx = False

try:
    from MiRCARTToPngFile import MiRCARTToPngFile
    haveMiRCARTToPngFile = True
except ImportError:
    haveMiRCARTToPngFile = False

try:
    import base64, json, requests, urllib.request
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

    # {{{ _exportFileToImgur(self, apiKey, imgName, imgTitle, pathName): upload single PNG file to Imgur
    def _exportFileToImgur(self, apiKey, imgName, imgTitle, pathName):
        requestImageData = open(pathName, "rb").read()
        requestData = {                                     \
            "image": base64.b64encode(requestImageData),    \
            "key":   apiKey,                                \
            "name":  imgName,                               \
            "title": imgTitle,                              \
            "type":  "base64"}
        requestHeaders = {"Authorization": "Client-ID " + apiKey}
        responseHttp = requests.post(                       \
            "https://api.imgur.com/3/upload.json",          \
            data=requestData, headers=requestHeaders)
        responseDict = json.loads(responseHttp.text)
        if responseHttp.status_code == 200:
                return [200, responseDict.get("data").get("link")]
        else:
                return [responseHttp.status_code, ""]
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
            if len(colourSpec) == 2:
                return (int(colourSpec[0] or curColours[0]),    \
                    int(colourSpec[1]))
            elif len(colourSpec) == 1:
                return (int(colourSpec[0]), curColours[0])
        else:
            return (15, 1)
    # }}}

    # {{{ exportBitmapToPngFile(self, canvasBitmap, outPathName, outType): XXX
    def exportBitmapToPngFile(self, canvasBitmap, outPathName, outType):
        return canvasBitmap.ConvertToImage().SaveFile(outPathName, outType)
    # }}}
    # {{{ exportBitmapToImgur(self, apiKey, canvasBitmap, imgName, imgTitle, imgType): XXX
    def exportBitmapToImgur(self, apiKey, canvasBitmap, imgName, imgTitle, imgType):
        tmpPathName = tempfile.mkstemp()
        os.close(tmpPathName[0])
        canvasBitmap.ConvertToImage().SaveFile(tmpPathName[1], imgType)
        imgurResult = self._exportFileToImgur(apiKey, imgName, imgTitle, tmpPathName[1])
        os.remove(tmpPathName[1])
        return imgurResult
    # }}}
    # {{{ exportPastebin(self, apiDevKey, canvasMap, canvasSize, pasteName="", pastePrivate=0): XXX
    def exportPastebin(self, apiDevKey, canvasMap, canvasSize, pasteName="", pastePrivate=0):
        if haveUrllib:
            outFile = io.StringIO()
            self.exportTextFile(canvasMap, canvasSize, outFile)
            requestData = {                                                         \
                "api_dev_key":          apiDevKey,                                  \
                "api_option":           "paste",                                    \
                "api_paste_code":       outFile.getvalue().encode(),                \
                "api_paste_name":       pasteName,                                  \
                "api_paste_private":    pastePrivate}
            responseHttp = requests.post("https://pastebin.com/api/api_post.php",   \
                    data=requestData)
            if responseHttp.status_code == 200:
                if responseHttp.text.startswith("http"):
                    return (True, responseHttp.text)
                else:
                    return (False, responseHttp.text)
            else:
                return (False, str(responseHttp.status_code))
        else:
            return (False, "missing requests and/or urllib3 module(s)")
    # }}}
    # {{{ exportPngFile(self, canvasMap, outPathName): XXX
    def exportPngFile(self, canvasMap, outPathName):
        if haveMiRCARTToPngFile:
            MiRCARTToPngFile(canvasMap).export(outPathName)
            return True
        else:
            return False
    # }}}
    # {{{ exportTextFile(self, canvasMap, canvasSize, outFile): XXX
    def exportTextFile(self, canvasMap, canvasSize, outFile):
        for canvasRow in range(canvasSize[1]):
            canvasLastColours = []
            for canvasCol in range(canvasSize[0]):
                canvasColColours = canvasMap[canvasRow][canvasCol][0]
                canvasColText = canvasMap[canvasRow][canvasCol][2]
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
        self.parentCanvas.onStoreUpdate(self.inSize, self.outMap)
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
        newMap = [[[(1, 1), 0, " "]                                 \
                for x in range(self.parentCanvas.canvasSize[0])]    \
                    for y in range(self.parentCanvas.canvasSize[1])]
        self.parentCanvas.onStoreUpdate(newCanvasSize, newMap)
    # }}}

    #
    # __init__(self, inFile=None, parentCanvas=None): initialisation method
    def __init__(self, inFile=None, parentCanvas=None):
        self.inFile = inFile; self.inSize = self.outMap = None;
        self.parentCanvas = parentCanvas
        if inFile != None:
            self.importTextFile(inFile)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
