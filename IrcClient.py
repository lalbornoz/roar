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
import select, socket, time

class IrcClient:
    """Non-blocking abstraction over the IRC protocol"""
    serverHname = serverPort = None;
    clientNick = clientIdent = clientGecos = None;
    clientSocket = clientSocketFile = None;
    clientNextTimeout = None; clientQueue = None;

    # {{{ close(self): Close connection to server
    def close(self):
        if self.clientSocket != None:
            self.clientSocket.close()
        self.clientSocket = self.clientSocketFile = None;
    # }}}
    # {{{ connect(self, timeout=None): Connect to server and register w/ optional timeout
    def connect(self, timeout=None):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.setblocking(0)
        try:
            self.clientSocket.connect((self.serverHname, int(self.serverPort)))
        except BlockingIOError:
            pass
        if timeout:
            readySet = select.select([], [self.clientSocket.fileno()], [], timeout)
            if len(readySet[1]) == 0:
                self.close(); return False;
        else:
            select.select([], [self.clientSocket.fileno()], [])
        self.clientSocketFile = self.clientSocket.makefile()
        self.clientQueue = []
        self.queue("NICK", self.clientNick)
        self.queue("USER", self.clientIdent, "0", "0", self.clientGecos)
        return True
    # }}}
    # {{{ readline(self): Read and parse single line from server into canonicalised list, honouring timers
    def readline(self):
        if self.clientNextTimeout:
            timeNow = time.time()
            if self.clientNextTimeout <= timeNow:
                return ""
            else:
                readySet = select.select([self.clientSocket.fileno()], [], [], self.clientNextTimeout - timeNow)
        else:
            readySet = select.select([self.clientSocket.fileno()], [], [])
        msg = self.clientSocketFile.readline()
        if len(msg):
            msg = msg.rstrip("\r\n")
        else:
            if len(readySet[0]) == 0:
                return ""
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
    # {{{ queue(self, *args): Parse and queue single line to server from list
    def queue(self, *args):
        msg = ""; argNumMax = len(args);
        for argNum in range(0, argNumMax):
            if argNum == (argNumMax - 1):
                msg += ":" + args[argNum]
            else:
                msg += args[argNum] + " "
        self.clientQueue.append((msg + "\r\n").encode())
    # }}}
    # {{{ unqueue(self): Send all queued lines to server, honouring timers
    def unqueue(self):
        while self.clientQueue:
            msg = self.clientQueue[0]; msgLen = len(msg); msgBytesSent = 0;
            while msgBytesSent < msgLen:
                if self.clientNextTimeout:
                    timeNow = time.time()
                    if self.clientNextTimeout <= timeNow:
                        self.clientQueue[0] = msg; return;
                    else:
                        readySet = select.select([], [self.clientSocket.fileno()], [], self.clientNextTimeout - timeNow)
                        if len(readySet[1]) == 0:
                            self.clientQueue[0] = msg; return;
                else:
                    readySet = select.select([], [self.clientSocket.fileno()], [])
                msgBytesSent = self.clientSocket.send(msg)
                msg = msg[msgBytesSent:]; msgLen -= msgBytesSent;
            del self.clientQueue[0]
    # }}}

    #
    # __init__(self, serverHname, serverPort, clientNick, clientIdent, clientGecos): initialisation method
    def __init__(self, serverHname, serverPort, clientNick, clientIdent, clientGecos):
        self.serverHname = serverHname; self.serverPort = serverPort;
        self.clientNick = clientNick; self.clientIdent = clientIdent; self.clientGecos = clientGecos;

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
