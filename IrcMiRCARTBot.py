#!/usr/bin/env python3
#
# IrcMiRCARTBot.py -- IRC<->MiRC2png bot (for EFnet #MiRCART)
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
import os, sys, time
import json
import IrcClient
import requests, urllib.request
from MiRCARTCanvasImportStore import MiRCARTCanvasImportStore
from MiRCARTToPngFile import MiRCARTToPngFile

class IrcMiRCARTBot(IrcClient.IrcClient):
    """IRC<->MiRC2png bot"""
    clientChannelLastMessage = clientChannelOps = clientChannel = None
    clientChannelRejoin = None

    # {{{ ContentTooLargeException(Exception): Raised by _urlretrieveReportHook() given download size > 1 MB
    class ContentTooLargeException(Exception):
        pass
    # }}}
    # {{{ _dispatch001(self, message): Dispatch single 001 (RPL_WELCOME)
    def _dispatch001(self, message):
        self._log("Registered on {}:{} as {}, {}, {}.".format(self.serverHname, self.serverPort, self.clientNick, self.clientIdent, self.clientGecos))
        self._log("Attempting to join {} on {}:{}...".format(self.clientChannel, self.serverHname, self.serverPort))
        self.queue("JOIN", self.clientChannel)
    # }}}
    # {{{ _dispatch353(self, message): Dispatch single 353 (RPL_NAMREPLY)
    def _dispatch353(self, message):
        if message[4].lower() == self.clientChannel.lower():
            for channelNickSpec in message[5].split(" "):
                if  len(channelNickSpec)                                    \
                and channelNickSpec[0] == "@"                               \
                and len(channelNickSpec[1:]):
                    self.clientChannelOps.append(channelNickSpec[1:].lower())
                    self._log("Authorising {} on {}".format(channelNickSpec[1:].lower(), message[4].lower()))
    # }}}
    # {{{ _dispatchJoin(self, message): Dispatch single JOIN message from server
    def _dispatchJoin(self, message):
        self._log("Joined {} on {}:{}.".format(message[2].lower(), self.serverHname, self.serverPort))
        self.clientNextTimeout = None; self.clientChannelRejoin = False;
    # }}}
    # {{{ _dispatchKick(self, message): Dispatch single KICK message from server
    def _dispatchKick(self, message):
        if  message[2].lower() == self.clientChannel.lower()                    \
        and message[3].lower() == self.clientNick.lower():
            self._log("Kicked from {} by {}, rejoining in 15 seconds".format(message[2].lower(), message[0]))
            self.clientNextTimeout = time.time() + 15; self.clientChannelRejoin = True;
    # }}}
    # {{{ _dispatchMode(self, message): Dispatch single MODE message from server
    def _dispatchMode(self, message):
        if message[2].lower() == self.clientChannel.lower():
            channelModeType = "+"; channelModeArg = 4;
            channelAuthAdd = ""; channelAuthDel = "";
            for channelModeChar in message[3]:
                if channelModeChar[0] == "-":
                    channelModeType = "-"
                elif channelModeChar[0] == "+":
                    channelModeType = "+"
                elif channelModeChar[0].isalpha():
                    if channelModeChar[0] == "o":
                        if channelModeType == "+":
                            channelAuthAdd = message[channelModeArg]; channelAuthDel = "";
                        elif channelModeType == "-":
                            channelAuthAdd = ""; channelAuthDel = message[channelModeArg];
                    channelModeArg += 1
            if  len(channelAuthAdd)                                             \
            and channelAuthAdd not in self.clientChannelOps:
                channelAuthAdd = channelAuthAdd.lower()
                self._log("Authorising {} on {}".format(channelAuthAdd, message[2].lower()))
                self.clientChannelOps.append(channelAuthAdd)
            elif len(channelAuthDel)                                            \
            and  channelAuthDel in self.clientChannelOps:
                channelAuthDel = channelAuthDel.lower()
                self._log("Deauthorising {} on {}".format(channelAuthDel, message[2].lower()))
                self.clientChannelOps.remove(channelAuthDel)
    # }}}
    # {{{ _dispatchNone(self): Dispatch None message from server
    def _dispatchNone(self):
        self._log("Disconnected from {}:{}.".format(self.serverHname, self.serverPort))
        self.close()
    # }}}
    # {{{ _dispatchPing(self, message): Dispatch single PING message from server
    def _dispatchPing(self, message):
        self.queue("PONG", message[2])
    # }}}
    # {{{ _dispatchPrivmsg(self, message): Dispatch single PRIVMSG message from server
    def _dispatchPrivmsg(self, message):
        if  message[2].lower() == self.clientChannel.lower()           \
        and message[3].startswith("!pngbot "):
            if (int(time.time()) - self.clientLastMessage) < 30:
                self._log("Ignoring request on {} from {} due to rate limit: {}".format(message[2].lower(), message[0], message[3]))
                return
            elif message[0].split("!")[0].lower() not in self.clientChannelOps:
                self._log("Ignoring request on {} from {} due to lack of authorisation: {}".format(message[2].lower(), message[0], message[3]))
                return
            else:
                self._log("Processing request on {} from {}: {}".format(message[2].lower(), message[0], message[3]))
            asciiUrl = message[3].split(" ")[1]
            asciiTmpFilePath = "tmp.txt"; imgTmpFilePath = "tmp.png";
            if os.path.isfile(asciiTmpFilePath):
                os.remove(asciiTmpFilePath)
            if os.path.isfile(imgTmpFilePath):
                os.remove(imgTmpFilePath)
            try:
                urllib.request.urlretrieve(asciiUrl, asciiTmpFilePath, IrcMiRCARTBot._urlretrieveReportHook)
            except IrcMiRCARTBot.ContentTooLargeException:
                self._log("Download size exceeds quota of 1 MB!")
                self.queue("PRIVMSG", message[2], "4/!\\ Download size exceeds quota of 1 MB!")
                return
            except urllib.error.HTTPError as err:
                self._log("Download failed with HTTP status code {}".format(err.code))
                self.queue("PRIVMSG", message[2], "4/!\\ Download failed with HTTP status code {}!".format(err.code))
                return
            except urllib.error.URLError as err:
                self._log("Invalid URL specified!")
                self.queue("PRIVMSG", message[2], "4/!\\ Invalid URL specified!")
                return
            except ValueError as err:
                self._log("Unknown URL type specified!")
                self.queue("PRIVMSG", message[2], "4/!\\ Unknown URL type specified!")
                return

            canvasStore = MiRCARTCanvasImportStore(inFile=asciiTmpFilePath)
            numRowCols = 0
            for numRow in range(len(canvasStore.outMap)):
                numRowCols = max(numRowCols, len(canvasStore.outMap[numRow]))
            for numRow in range(len(canvasStore.outMap)):
                if len(canvasStore.outMap[numRow]) != numRowCols:
                    for numColOff in range(numRowCols - len(canvasStore.outMap[numRow])):
                        canvasStore.outMap[numRow].append([1, 1, 0, " "])
                canvasStore.outMap[numRow].insert(0, [1, 1, 0, " "])
                canvasStore.outMap[numRow].append([1, 1, 0, " "])
            canvasStore.outMap.insert(0, [[1, 1, 0, " "]] * len(canvasStore.outMap[0]))
            canvasStore.outMap.append([[1, 1, 0, " "]] * len(canvasStore.outMap[0]))
            MiRCARTToPngFile(canvasStore.outMap, "DejaVuSansMono.ttf", 11).export(imgTmpFilePath)
            imgurResponse = self._uploadToImgur(imgTmpFilePath, "MiRCART image", "MiRCART image", "c9a6efb3d7932fd")
            if imgurResponse[0] == 200:
                    self._log("Uploaded as: {}".format(imgurResponse[1]))
                    self.queue("PRIVMSG", message[2], "8/!\\ Uploaded as: {}".format(imgurResponse[1]))
                    self.clientLastMessage = int(time.time())
            else:
                    self._log("Upload failed with HTTP status code {}".format(imgurResponse[0]))
                    self.queue("PRIVMSG", message[2], "4/!\\ Upload failed with HTTP status code {}!".format(imgurResponse[0]))
            if os.path.isfile(asciiTmpFilePath):
                os.remove(asciiTmpFilePath)
            if os.path.isfile(imgTmpFilePath):
                os.remove(imgTmpFilePath)
    # }}}
    # {{{ _dispatchTimer(self): Dispatch single client timer expiration
    def _dispatchTimer(self):
        if self.clientChannelRejoin:
            self._log("Attempting to join {} on {}:{}...".format(self.clientChannel, self.serverHname, self.serverPort))
            self.queue("JOIN", self.clientChannel)
            self.clientNextTimeout = time.time() + 15; self.clientChannelRejoin = True;
    # }}}
    # {{{ _log(self, msg): Log single message to stdout w/ timestamp
    def _log(self, msg):
        print(time.strftime("%Y/%m/%d %H:%M:%S") + " " + msg)
    # }}}
    # {{{ _uploadToImgur(self, imgFilePath, imgName, imgTitle, apiKey): Upload single file to Imgur
    def _uploadToImgur(self, imgFilePath, imgName, imgTitle, apiKey):
        with open(imgFilePath, "rb") as requestImage:
            requestImageData = requestImage.read()
        requestData = {                                     \
            "image": base64.b64encode(requestImageData),    \
            "key":   apiKey,                                \
            "name":  imgName,                               \
            "title": imgTitle,                              \
            "type":  "base64"}
        requestHeaders = {                                  \
            "Authorization": "Client-ID " + apiKey}
        responseHttp = requests.post("https://api.imgur.com/3/upload.json", data=requestData, headers=requestHeaders)
        responseDict = json.loads(responseHttp.text)
        if responseHttp.status_code == 200:
                return [200, responseDict.get("data").get("link")]
        else:
                return [responseHttp.status_code]
    # }}}
    # {{{ _urlretrieveReportHook(count, blockSize, totalSize): Limit downloads to 1 MB
    def _urlretrieveReportHook(count, blockSize, totalSize):
        if (totalSize > pow(2,20)):
            raise IrcMiRCARTBot.ContentTooLargeException
    # }}}
    # {{{ connect(self, timeout=None): Connect to server and (re)initialise w/ optional timeout
    def connect(self, timeout=None):
        self._log("Connecting to {}:{}...".format(self.serverHname, self.serverPort))
        if super().connect(timeout):
                self._log("Connected to {}:{}.".format(self.serverHname, self.serverPort))
                self._log("Registering on {}:{} as {}, {}, {}...".format(self.serverHname, self.serverPort, self.clientNick, self.clientIdent, self.clientGecos))
                self.clientLastMessage = 0; self.clientChannelOps = [];
                self.clientChannelRejoin = False
                return True
        else:
                return False
    # }}}
    # {{{ dispatch(self): Read, parse, and dispatch single line from server
    def dispatch(self):
        while True:
            if self.clientNextTimeout:
                timeNow = time.time()
                if self.clientNextTimeout <= timeNow:
                    self._dispatchTimer()
            self.unqueue()
            serverMessage = self.readline()
            if serverMessage == None:
                self._dispatchNone(); break;
            elif serverMessage == "":
                continue
            elif serverMessage[1] == "001":
                self._dispatch001(serverMessage)
            elif serverMessage[1] == "353":
                self._dispatch353(serverMessage)
            elif serverMessage[1] == "JOIN":
                self._dispatchJoin(serverMessage)
            elif serverMessage[1] == "KICK":
                self._dispatchKick(serverMessage)
            elif serverMessage[1] == "MODE":
                self._dispatchMode(serverMessage)
            elif serverMessage[1] == "PING":
                self._dispatchPing(serverMessage)
            elif serverMessage[1] == "PRIVMSG":
                self._dispatchPrivmsg(serverMessage)
    # }}}

    #
    # __init__(self, serverHname, serverPort="6667", clientNick="pngbot", clientIdent="pngbot", clientGecos="pngbot", clientChannel="#MiRCART"): initialisation method
    def __init__(self, serverHname, serverPort="6667", clientNick="pngbot", clientIdent="pngbot", clientGecos="pngbot", clientChannel="#MiRCART"):
        super().__init__(serverHname, serverPort, clientNick, clientIdent, clientGecos)
        self.clientChannel = clientChannel

#
# Entry point
def main(*argv):
    _IrcMiRCARTBot = IrcMiRCARTBot(*argv[1:])
    while True:
        if _IrcMiRCARTBot.connect(15):
            _IrcMiRCARTBot.dispatch()
            _IrcMiRCARTBot.close()
        time.sleep(15)

if __name__ == "__main__":
    if ((len(sys.argv) - 1) < 1)\
    or ((len(sys.argv) - 1) > 4):
        print("usage: {} "                                                  \
            "<IRC server hostname> "                                        \
            "[<IRC server port; defaults to 6667>] "                        \
            "[<IRC bot nick name; defaults to pngbot>] "                    \
            "[<IRC bot user name; defaults to pngbot>] "                    \
            "[<IRC bot real name; defaults to pngbot>] "                    \
            "[<IRC bot channel name; defaults to #MiRCART>] ".format(sys.argv[0]), file=sys.stderr)
    else:
        main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
