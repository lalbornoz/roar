#!/usr/bin/env python3
#
# mirc2png -- convert ASCII w/ mIRC control codes to monospaced PNG (for EFnet #MiRCART)
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

from itertools import chain
import base64
import json
import mirc2png
import os, socket, sys, time
import requests
import urllib.request

class IrcBot:
    """Blocking abstraction over the IRC protocol"""
    serverHname = serverPort = None;
    clientNick = clientIdent = clientGecos = None;
    clientSocket = clientSocketFile = None;

    # {{{ connect(): Connect to server and register
    def connect(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.serverHname, int(self.serverPort)))
        self.clientSocketFile = self.clientSocket.makefile()
        self.sendline("NICK", self.clientNick)
        self.sendline("USER", self.clientIdent, "0", "0", self.clientGecos)
    # }}}
    # {{{ close(): Close connection to server
    def close(self):
        if self.clientSocket != None:
            self.clientSocket.close()
        self.clientSocket = self.clientSocketFile = None;
    # }}}
    # {{{ readline(): Read and parse single line from server into canonicalised list
    def readline(self):
        msg = self.clientSocketFile.readline()
        if len(msg):
            msg = msg.rstrip("\r\n")
        else:
            return None
        msg = msg.split(" :", 1)
        if len(msg) == 1:
            msg = list(chain.from_iterable(m.split(" ") for m in msg))
        elif len(msg) == 2:
            msg = msg[0].split(" ") + [msg[1]]
        if msg[0][0] == ':':
            msg = [msg[0][1:]] + msg[1:]
        else:
            msg = [""] + msg[1:]
        return msg
    # }}}
    # {{{ sendline(): Parse and send single line to server from list
    def sendline(self, *args):
        msg = ""; argNumMax = len(args);
        for argNum in range(0, argNumMax):
            if argNum == (argNumMax - 1):
                msg += ":" + args[argNum]
            else:
                msg += args[argNum] + " "
        return self.clientSocket.send((msg + "\r\n").encode())
    # }}}
    # {{{ Initialisation method
    def __init__(self, serverHname, serverPort, clientNick, clientIdent, clientGecos):
        self.serverHname = serverHname; self.serverPort = serverPort;
        self.clientNick = clientNick; self.clientIdent = clientIdent; self.clientGecos = clientGecos;
    # }}}

class IrcMiRCARTBot(IrcBot):
    """IRC<->MiRCART bot"""
    clientChannelLastMessage = clientChannelOps = clientChannel = None

    # {{{ connect(): Connect to server and (re)initialise
    def connect(self):
        print("Connecting to {}:{}...".format(self.serverHname, self.serverPort))
        super().connect()
        print("Connected to {}:{}.".format(self.serverHname, self.serverPort))
        print("Registering on {}:{} as {}, {}, {}...".format(self.serverHname, self.serverPort, self.clientNick, self.clientIdent, self.clientGecos))
        self.clientLastMessage = 0; self.clientChannelOps = [];
    # }}}
    # {{{ dispatch(): Read, parse, and dispatch single line from server
    def dispatch(self):
        while True:
            serverMessage = self.readline()
            if serverMessage == None:
                print("Disconnected from {}:{}.".format(self.serverHname, self.serverPort))
                self.close(); break;
            elif serverMessage[1] == "001":
                print("Registered on {}:{} as {}, {}, {}.".format(self.serverHname, self.serverPort, self.clientNick, self.clientIdent, self.clientGecos))
                print("Joining {} on {}:{}...".format(self.clientChannel, self.serverHname, self.serverPort))
                self.sendline("JOIN", self.clientChannel)
            elif serverMessage[1] == "353"                                  \
            and  serverMessage[4].lower() == self.clientChannel.lower():
                for channelNickSpec in serverMessage[5].split(" "):
                    if  channelNickSpec[0] == "@"                           \
                    and len(channelNickSpec[1:]):
                        self.clientChannelOps.append(channelNickSpec[1:])
                        print("Authorising {} on {}".format(channelNickSpec[1:], serverMessage[2]))
            elif serverMessage[1] == "MODE"                                 \
            and  serverMessage[2].lower() == self.clientChannel.lower():
                channelModeType = "+"; channelModeArg = 4;
                channelAuthAdd = ""; channelAuthDel = "";
                for channelModeChar in serverMessage[3]:
                    if channelModeChar[0] == "-":
                        channelModeType = "-"
                    elif channelModeChar[0] == "+":
                        channelModeType = "+"
                    elif channelModeChar[0].isalpha():
                        if channelModeChar[0] == "o":
                            if channelModeType == "+":
                                channelAuthAdd = serverMessage[channelModeArg]; channelAuthDel = "";
                            elif channelModeType == "-":
                                channelAuthAdd = ""; channelAuthDel = serverMessage[channelModeArg];
                        channelModeArg += 1
                if  len(channelAuthAdd)                                     \
                and channelAuthAdd not in self.clientChannelOps:
                    print("Authorising {} on {}".format(channelAuthAdd, serverMessage[2]))
                    self.clientChannelOps.append(channelAuthAdd)
                elif len(channelAuthDel)                                    \
                and  channelAuthDel in self.clientChannelOps:
                    print("Deauthorising {} on {}".format(channelAuthDel, serverMessage[2]))
                    self.clientChannelOps.remove(channelAuthDel)
            elif serverMessage[1] == "PING":
                self.sendline("PONG", serverMessage[2])
            elif serverMessage[1] == "PRIVMSG"                              \
            and  serverMessage[2].lower() == self.clientChannel.lower()     \
            and  serverMessage[3].startswith("!pngbot "):
                if (int(time.time()) - self.clientLastMessage) < 45:
                    continue
                else:
                    self.clientLastMessage = int(time.time())
                asciiUrl = serverMessage[3].split(" ")[1]
                asciiTmpFilePath = "tmp.txt"; imgTmpFilePath = "tmp.png";
                if os.path.isfile(asciiTmpFilePath):
                    os.remove(asciiTmpFilePath)
                if os.path.isfile(imgTmpFilePath):
                    os.remove(imgTmpFilePath)
                urllib.request.urlretrieve(asciiUrl, asciiTmpFilePath)
                _MiRCART = mirc2png.MiRCART(asciiTmpFilePath, imgTmpFilePath, "DejaVuSansMono.ttf", 11)
                imgurResponse = self.uploadToImgur(imgTmpFilePath, "MiRCART image", "MiRCART image", "c9a6efb3d7932fd")
                if imgurResponse[0] == 200:
                        self.sendline("PRIVMSG", serverMessage[2], "8/!\\ Uploaded as: {}".format(imgurResponse[1]))
                else:
                        self.sendline("PRIVMSG", serverMessage[2], "4/!\\ Uploaded failed with HTTP status code {}!".format(imgurResponse[0]))
                if os.path.isfile(asciiTmpFilePath):
                    os.remove(asciiTmpFilePath)
                if os.path.isfile(imgTmpFilePath):
                    os.remove(imgTmpFilePath)
    # }}}
    # {{{ uploadToImgur(): Upload single file to Imgur
    def uploadToImgur(self, imgFilePath, imgName, imgTitle, apiKey):
        requestImageData = open(imgFilePath, "rb").read()
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
    # {{{ Initialisation method
    def __init__(self, serverHname, serverPort="6667", clientNick="pngbot", clientIdent="pngbot", clientGecos="pngbot", clientChannel="#MiRCART"):
        super().__init__(serverHname, serverPort, clientNick, clientIdent, clientGecos)
        self.clientChannel = clientChannel
    # }}}

#
# Entry point
def main(*argv):
    _IrcMiRCARTBot = IrcMiRCARTBot(*argv[1:])
    while True:
        _IrcMiRCARTBot.connect()
        _IrcMiRCARTBot.dispatch()
        _IrcMiRCARTBot.close()

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

# vim:expandtab foldmethod=marker sw=8 ts=8 tw=120
