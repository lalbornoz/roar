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
import os, socket, sys
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

#
# Entry point
def main(argv0, ircServerHname, ircServerPort="6667", ircClientNick="pngbot", ircClientIdent="pngbot", ircClientGecos="pngbot", ircClientChannel="#MiRCART"):
    _IrcBot = IrcBot(ircServerHname, ircServerPort, ircClientNick, ircClientIdent, ircClientGecos)
    print("Connecting to {}:{}...".format(ircServerHname, ircServerPort))
    _IrcBot.connect()
    print("Connected to {}:{}.".format(ircServerHname, ircServerPort))
    print("Registering on {}:{} as {}, {}, {}...".format(ircServerHname, ircServerPort, ircClientNick, ircClientIdent, ircClientGecos))
    while True:
        ircServerMessage = _IrcBot.readline()
        if ircServerMessage == None:
            print("Disconnected from {}:{}.".format(ircServerHname, ircServerPort))
            _IrcBot.close(); break;
        elif ircServerMessage[1] == "001":
            print("Registered on {}:{} as {}, {}, {}.".format(ircServerHname, ircServerPort, ircClientNick, ircClientIdent, ircClientGecos))
            print("Joining {} on {}:{}...".format(ircClientChannel, ircServerHname, ircServerPort))
            _IrcBot.sendline("JOIN", ircClientChannel)
        elif ircServerMessage[1] == "PING":
            _IrcBot.sendline("PONG", ircServerMessage[2])
        elif ircServerMessage[1] == "PRIVMSG"           \
        and  ircServerMessage[2] == ircClientChannel    \
        and  ircServerMessage[3].startswith("!pngbot "):
            asciiUrl = ircServerMessage[3].split(" ")[1]
            asciiTmpFilePath = "tmp.txt"; imgTmpFilePath = "tmp.png";
            if os.path.isfile(asciiTmpFilePath):
                os.remove(asciiTmpFilePath)
            if os.path.isfile(imgTmpFilePath):
                os.remove(imgTmpFilePath)
            urllib.request.urlretrieve(asciiUrl, asciiTmpFilePath)
            _MiRCART = mirc2png.MiRCART(asciiTmpFilePath, imgTmpFilePath, "DejaVuSansMono.ttf", 11)
            imgurResponseHttp = requests.post("https://api.imgur.com/3/upload.json", data={"key":"c9a6efb3d7932fd", "image":base64.b64encode(open(imgTmpFilePath, "rb").read()), "type":"base64", "name":"tmp.png", "title":"tmp.png"}, headers={"Authorization": "Client-ID c9a6efb3d7932fd"})
            imgurResponse = json.loads(imgurResponseHttp.text)
            imgurResponseUrl = imgurResponse.get("data").get("link")
            _IrcBot.sendline("PRIVMSG", ircServerMessage[2], "Uploaded as {}".format(imgurResponseUrl))
            os.remove(asciiTmpFilePath); os.remove(imgTmpFilePath);

if __name__ == "__main__":
    if ((len(sys.argv) - 1) < 1)\
    or ((len(sys.argv) - 1) > 4):
        print("usage: {} "                                          \
            "<IRC server hostname> "                                \
            "[<IRC server port; defaults to 6667>] "                \
            "[<IRC bot nick name; defaults to pngbot>] "            \
            "[<IRC bot user name; defaults to pngbot>] "            \
            "[<IRC bot real name; defaults to pngbot>] "            \
            "[<IRC bot channel name; defaults to #MiRCART>] ".format(sys.argv[0]), file=sys.stderr)
    else:
        main(*sys.argv)

# vim:expandtab foldmethod=marker sw=8 ts=8 tw=120
