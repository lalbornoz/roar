#!/usr/bin/env python3
#
# CanvasExportStore.py -- XXX
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import io, os, tempfile

try:
    from ToPngFile import ToPngFile
    haveToPngFile = True
except ImportError:
    haveToPngFile = False

try:
    import base64, json, requests, urllib.request
    haveUrllib = True
except ImportError:
    haveUrllib = False

class CanvasExportStore():
    """XXX"""
    ImgurUploadUrl = "https://api.imgur.com/3/upload.json"
    PastebinPostUrl = "https://pastebin.com/api/api_post.php"

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
    # {{{ exportPngFile(self, canvasMap, outPathName): XXX
    def exportPngFile(self, canvasMap, outPathName):
        if haveToPngFile:
            ToPngFile(canvasMap).export(outPathName)
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

    #
    # __init__(self, parentCanvas): initialisation method
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
