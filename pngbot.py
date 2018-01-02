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
            msg = [""] + msg[0:]
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
    # {{{ dispatchNone(): Dispatch None message from server
    def dispatchNone(self):
        print("Disconnected from {}:{}.".format(self.serverHname, self.serverPort))
        self.close()
    # }}}
    # {{{ dispatch001(): Dispatch single 001 (RPL_WELCOME)
    def dispatch001(self, message):
        print("Registered on {}:{} as {}, {}, {}.".format(self.serverHname, self.serverPort, self.clientNick, self.clientIdent, self.clientGecos))
        print("Joining {} on {}:{}...".format(self.clientChannel, self.serverHname, self.serverPort))
        self.sendline("JOIN", self.clientChannel)
    # }}}
    # {{{ dispatch353(): Dispatch single 353 (RPL_NAMREPLY)
    def dispatch353(self, message):
        if message[4].lower() == self.clientChannel.lower():
            for channelNickSpec in message[5].split(" "):
                if  channelNickSpec[0] == "@"                               \
                and len(channelNickSpec[1:]):
                    self.clientChannelOps.append(channelNickSpec[1:].lower())
                    print("Authorising {} on {}".format(channelNickSpec[1:].lower(), message[4].lower()))
    # }}}
    # {{{ dispatchMode(): Dispatch single MODE message from server
    def dispatchMode(self, message):
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
                print("Authorising {} on {}".format(channelAuthAdd, message[2].lower()))
                self.clientChannelOps.append(channelAuthAdd)
            elif len(channelAuthDel)                                            \
            and  channelAuthDel in self.clientChannelOps:
                channelAuthDel = channelAuthDel.lower()
                print("Deauthorising {} on {}".format(channelAuthDel, message[2].lower()))
                self.clientChannelOps.remove(channelAuthDel)
    # }}}
    # {{{ dispatchPing(): Dispatch single PING message from server
    def dispatchPing(self, message):
        self.sendline("PONG", message[2])
    # }}}
    # {{{ dispatchPrivmsg(): Dispatch single PRIVMSG message from server
    def dispatchPrivmsg(self, message):
        if  message[2].lower() == self.clientChannel.lower()           \
        and message[3].startswith("!pngbot "):
            if (int(time.time()) - self.clientLastMessage) < 45:
                print("Ignoring request on {} from {} due to rate limit: {}".format(message[2].lower(), message[0], message[3]))
                return
            elif message[0].split("!")[0].lower() not in self.clientChannelOps:
                print("Ignoring request on {} from {} due to lack of authorisation: {}".format(message[2].lower(), message[0], message[3]))
                return
            else:
                print("Processing request on {} from {}: {}".format(message[2].lower(), message[0], message[3]))
                self.clientLastMessage = int(time.time())
            asciiUrl = message[3].split(" ")[1]
            asciiTmpFilePath = "tmp.txt"; imgTmpFilePath = "tmp.png";
            if os.path.isfile(asciiTmpFilePath):
                os.remove(asciiTmpFilePath)
            if os.path.isfile(imgTmpFilePath):
                os.remove(imgTmpFilePath)
            urllib.request.urlretrieve(asciiUrl, asciiTmpFilePath)
            _MiRCART = mirc2png.MiRCART(asciiTmpFilePath, imgTmpFilePath, "DejaVuSansMono.ttf", 11)
            imgurResponse = self.uploadToImgur(imgTmpFilePath, "MiRCART image", "MiRCART image", "c9a6efb3d7932fd")
            if imgurResponse[0] == 200:
                    print("Uploaded as: {}".format(imgurResponse[1]))
                    self.sendline("PRIVMSG", message[2], "8/!\\ Uploaded as: {}".format(imgurResponse[1]))
            else:
                    print("Upload failed with HTTP status code {}".format(imgurResponse[0]))
                    self.sendline("PRIVMSG", message[2], "4/!\\ Uploaded failed with HTTP status code {}!".format(imgurResponse[0]))
            if os.path.isfile(asciiTmpFilePath):
                os.remove(asciiTmpFilePath)
            if os.path.isfile(imgTmpFilePath):
                os.remove(imgTmpFilePath)
    # }}}
    # {{{ dispatch(): Read, parse, and dispatch single line from server
    def dispatch(self):
        while True:
            serverMessage = self.readline()
            if serverMessage == None:
                self.dispatchNone(); break;
            elif serverMessage[1] == "001":
                self.dispatch001(serverMessage)
            elif serverMessage[1] == "353":
                self.dispatch353(serverMessage)
            elif serverMessage[1] == "MODE":
                self.dispatchMode(serverMessage)
            elif serverMessage[1] == "PING":
                self.dispatchPing(serverMessage)
            elif serverMessage[1] == "PRIVMSG":
                self.dispatchPrivmsg(serverMessage)
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
