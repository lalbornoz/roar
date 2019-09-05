#!/usr/bin/env python3
#
# CanvasExportStore.py -- XXX
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Colours import ColourMapBold, ColourMapNormal, MiRCARTToAnsiColours
import io, os, tempfile

try:
    from PIL import Image, ImageDraw, ImageFont
    havePIL = True
except ImportError:
    havePIL = False

try:
    import base64, json, requests, urllib.request
    haveUrllib = True
except ImportError:
    haveUrllib = False

class CanvasExportStore():
    """XXX"""
    # {{{ _CellState(): Cell state
    class _CellState():
        CS_NONE             = 0x00
        CS_BOLD             = 0x01
        CS_ITALIC           = 0x02
        CS_UNDERLINE        = 0x04
    # }}}
    ImgurUploadUrl = "https://api.imgur.com/3/upload.json"
    PastebinPostUrl = "https://pastebin.com/api/api_post.php"

    # {{{ _drawUnderline(self, curPos, fontSize, imgDraw, fillColour): XXX
    def _drawUnderLine(self, curPos, fontSize, imgDraw, fillColour):
        imgDraw.line(                                                       \
            xy=(curPos[0], curPos[1] + (fontSize[1] - 2),                   \
                curPos[0] + fontSize[0], curPos[1] + (fontSize[1] - 2)),    \
                fill=fillColour)
    # }}}
    # {{{ _exportFileToImgur(self, apiKey, imgName, imgTitle, pathName): upload single PNG file to Imgur
    def _exportFileToImgur(self, apiKey, imgName, imgTitle, pathName):
        with open(pathName, "rb") as requestImage:
            requestImageData = requestImage.read()
        requestData = {                                     \
            "image":    base64.b64encode(requestImageData), \
            "key":      apiKey,                             \
            "name":     imgName,                            \
            "title":    imgTitle,                           \
            "type":     "base64"}
        requestHeaders = {"Authorization": "Client-ID " + apiKey}
        responseHttp = requests.post(ImgurUploadUrl, data=requestData, headers=requestHeaders)
        responseDict = json.loads(responseHttp.text)
        if responseHttp.status_code == 200:
                return [200, responseDict.get("data").get("link")]
        else:
                return [responseHttp.status_code, ""]
    # }}}

    # {{{ exportAnsiFile(self, canvasMap, canvasSize, outFile): XXX
    def exportAnsiFile(self, canvasMap, canvasSize, outFile):
        outBuffer = ""
        for inCurRow in range(len(canvasMap)):
            lastAttribs = self._CellState.CS_NONE
            lastColours = None
            for inCurCol in range(len(canvasMap[inCurRow])):
                inCurCell = canvasMap[inCurRow][inCurCol]
                if lastAttribs != inCurCell[2]:
                    if inCurCell[2] & self._CellState.CS_BOLD:
                        outBuffer += "\u001b[1m"
                    if inCurCell[2] & self._CellState.CS_UNDERLINE:
                        outBuffer += "\u001b[4m"
                    lastAttribs = inCurCell[2]
                if lastColours == None or lastColours != inCurCell[:2]:
                    ansiBg = MiRCARTToAnsiColours[int(inCurCell[1])] + 10
                    ansiFg = MiRCARTToAnsiColours[int(inCurCell[0])]
                    outBuffer += "\u001b[{:02d}m\u001b[{:02d}m{}".format(ansiBg, ansiFg, inCurCell[3])
                    lastColours = inCurCell[:2]
                else:
                    outBuffer += inCurCell[3]
            outBuffer += "\u001b[0m\n"
        outFile.write(outBuffer)
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
    # {{{ exportBitmapToPngFile(self, canvasBitmap, outPathName, outType): XXX
    def exportBitmapToPngFile(self, canvasBitmap, outPathName, outType):
        return canvasBitmap.ConvertToImage().SaveFile(outPathName, outType)
    # }}}
    # {{{ exportPastebin(self, apiDevKey, canvasMap, canvasSize, pasteName="", pastePrivate=0): XXX
    def exportPastebin(self, apiDevKey, canvasMap, canvasSize, pasteName="", pastePrivate=0):
        if haveUrllib:
            outFile = io.StringIO()
            self.exportTextFile(canvasMap, canvasSize, outFile)
            requestData = {                                             \
                "api_dev_key":          apiDevKey,                      \
                "api_option":           "paste",                        \
                "api_paste_code":       outFile.getvalue().encode(),    \
                "api_paste_name":       pasteName,                      \
                "api_paste_private":    pastePrivate}
            responseHttp = requests.post(PastebinPostUrl, data=requestData)
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
    # {{{ exportPngFile(self, canvasMap, outPathName, fontFilePath, fontSize): XXX
    def exportPngFile(self, canvasMap, outPathName, fontFilePath, fontSize):
        if havePIL:
            outFontFilePath, outFontSize = fontFilePath, fontSize
            outImgFont = ImageFont.truetype(outFontFilePath, outFontSize)
            outImgFontSize = [*outImgFont.getsize(" ")]
            outImgFontSize[1] += 3
            inSize = (len(canvasMap[0]), len(canvasMap))
            outSize = [a*b for a,b in zip(inSize, outImgFontSize)]
            outCurPos = [0, 0]
            outImg = Image.new("RGBA", outSize, (*ColourMapNormal[1], 255))
            outImgDraw = ImageDraw.Draw(outImg)
            outImgDraw.fontmode = "1"
            for inCurRow in range(len(canvasMap)):
                for inCurCol in range(len(canvasMap[inCurRow])):
                    inCurCell = canvasMap[inCurRow][inCurCol]
                    outColours = [0, 0]
                    if inCurCell[2] & self._CellState.CS_BOLD:
                        if inCurCell[3] != " ":
                            if inCurCell[3] == "█":
                                outColours[1] = ColourMapNormal[inCurCell[0]]
                            else:
                                outColours[0] = ColourMapBold[inCurCell[0]]
                                outColours[1] = ColourMapNormal[inCurCell[1]]
                        else:
                            outColours[1] = ColourMapNormal[inCurCell[1]]
                    else:
                        if inCurCell[3] != " ":
                            if inCurCell[3] == "█":
                                outColours[1] = ColourMapNormal[inCurCell[0]]
                            else:
                                outColours[0] = ColourMapNormal[inCurCell[0]]
                                outColours[1] = ColourMapNormal[inCurCell[1]]
                        else:
                            outColours[1] = ColourMapNormal[inCurCell[1]]
                    outImgDraw.rectangle((*outCurPos, outCurPos[0] + outImgFontSize[0], outCurPos[1] + outImgFontSize[1]), fill=(*outColours[1], 255))
                    if  not inCurCell[3] in " █"    \
                    and outColours[0] != outColours[1]:
                        # XXX implement italic
                        outImgDraw.text(outCurPos, inCurCell[3], (*outColours[0], 255), outImgFont)
                    if inCurCell[2] & self._CellState.CS_UNDERLINE:
                        outColours[0] = ColourMapNormal[inCurCell[0]]
                        self._drawUnderLine(outCurPos, outImgFontSize, outImgDraw, (*outColours[0], 255))
                    outCurPos[0] += outImgFontSize[0];
                outCurPos[0] = 0
                outCurPos[1] += outImgFontSize[1]
            outImg.save(outPathName);
            return True
        else:
            return False
    # }}}
    # {{{ exportTextBuffer(self, canvasMap, canvasSize): XXX
    def exportTextBuffer(self, canvasMap, canvasSize):
        outBuffer = ""
        for canvasRow in range(canvasSize[1]):
            canvasLastColours = [15, 1]
            for canvasCol in range(canvasSize[0]):
                canvasColColours = canvasMap[canvasRow][canvasCol][0:2]
                canvasColText = canvasMap[canvasRow][canvasCol][3]
                if   canvasColColours[0] != canvasLastColours[0]    \
                and  canvasColColours[1] != canvasLastColours[1]:
                    if  canvasColColours[0] == canvasLastColours[1] \
                    and canvasColColours[1] == canvasLastColours[0]:
                        outBuffer += "\u0016"
                    else:
                        outBuffer += "\u0003{},{}".format(canvasColColours[0], canvasColColours[1])
                    canvasLastColours = canvasColColours
                elif canvasColColours[1] != canvasLastColours[1]:
                    outBuffer += "\u0003{},{}".format(canvasLastColours[0], canvasColColours[1])
                    canvasLastColours[1] = canvasColColours[1]
                elif canvasColColours[0] != canvasLastColours[0]:
                    outBuffer += "\u0003{}".format(canvasColColours[0])
                    canvasLastColours[0] = canvasColColours[0]
                outBuffer += canvasColText
            outBuffer += "\n"
        return outBuffer
    # }}}
    # {{{ exportTextFile(self, canvasMap, canvasSize, outFile): XXX
    def exportTextFile(self, canvasMap, canvasSize, outFile):
        outBuffer = self.exportTextBuffer(canvasMap, canvasSize)
        outFile.write(outBuffer)
    # }}}

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
