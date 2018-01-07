#!/usr/bin/env python3
#
# MiRCARTToPastebin.py -- XXX
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

from MiRCARTToTextFile import MiRCARTToTextFile
import io
import base64
import requests, urllib.request

class MiRCARTToPastebin():
    apiDevKey = outFile = outToTextFile = None

    # export(self): XXX
    def export(self):
        self.outToTextFile.export(self.outFile, pasteName="", pastePrivate=0)
        requestData = {                                                     \
            "api_dev_key":          self.apiDevKey,                         \
            "api_option":           "paste",                                \
            "api_paste_code":       base64.b64encode(self.outFile.read()),  \
            "api_paste_name":       pasteName,                              \
            "api_paste_private":    pastePrivate}
        responseHttp = requests.post("https://pastebin.com/post.php",       \
                data=requestData)
        if responseHttp.status_code == 200:
            return responseHttp.text
        else:
            return None

    # __init__(self, canvasMap, canvasSize): XXX
    def __init__(self, apiDevKey, canvasMap, canvasSize):
        self.apiDevKey = apiDevKey
        self.outFile = io.StringIO()
        self.outToTextFile = MiRCARTToTextFile(canvasMap, canvasSize)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
