#!/usr/bin/env python3
#
# MiRCARTCanvasExportStore.py -- XXX
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import io, os, tempfile

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

class MiRCARTCanvasExportStore():
    """XXX"""
    parentCanvas = None

    # {{{ _exportFileToImgur(self, apiKey, imgName, imgTitle, pathName): upload single PNG file to Imgur
    def _exportFileToImgur(self, apiKey, imgName, imgTitle, pathName):
        with open(pathName, "rb") as requestImage:
            requestImageData = requestImage.read()
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

    #
    # __init__(self, parentCanvas): initialisation method
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
