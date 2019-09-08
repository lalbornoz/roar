#!/usr/bin/env python3
#
# IrcClient.py 
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

from itertools import chain
import select, socket, time

class IrcClient:
    """Non-blocking abstraction over the IRC protocol"""

    # {{{ close(self): Close connection to server
    def close(self):
        if self.clientSocket != None:
            self.clientSocket.close()
        self.clientSocket = self.clientSocketFile = None;
    # }}}
    # {{{ connect(self, localAddr=None, preferFamily=socket.AF_INET, timeout=None): Connect to server and register w/ optional timeout
    def connect(self, localAddr=None, preferFamily=socket.AF_INET, timeout=None):
        gaiInfo = socket.getaddrinfo(self.serverHname, self.serverPort,
                                     preferFamily, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.clientSocket = socket.socket(*gaiInfo[0][:3])
        self.clientSocket.setblocking(0)
        if localAddr != None:
            gaiInfo_ = socket.getaddrinfo(localAddr, None, preferFamily, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            self.clientSocket.bind(gaiInfo_[0][4])
        try:
            self.clientSocket.connect(gaiInfo[0][4])
        except BlockingIOError:
            pass
        if timeout:
            readySet = select.select([], [self.clientSocket.fileno()], [], timeout)
            if len(readySet[1]) == 0:
                self.close(); return False;
        else:
            select.select([], [self.clientSocket.fileno()], [])
        self.clientSocketFile = self.clientSocket.makefile(encoding="utf-8", errors="replace")
        self.clientQueue = []
        self.queue("NICK", self.clientNick)
        self.queue("USER", self.clientIdent, "0", "0", self.clientGecos)
        return True
    # }}}
    # {{{ queue(self, *args): Parse and queue single line to server from list
    def queue(self, *args):
        msg = ""; argNumMax = len(args);
        for argNum in range(argNumMax):
            if argNum == (argNumMax - 1):
                msg += ":" + args[argNum]
            else:
                msg += args[argNum] + " "
        self.clientQueue.append((msg + "\r\n").encode())
    # }}}
    # {{{ readline(self, timeout=30): Read and parse single line from server into canonicalised list, honouring timers
    def readline(self, timeout=30):
        if self.clientNextTimeout:
            timeNow = time.time()
            if self.clientNextTimeout <= timeNow:
                return ""
            else:
                readySet = select.select([self.clientSocket.fileno()], [], [], self.clientNextTimeout - timeNow)
                if  len(readySet[0]) == 0   \
                and (time.time() - timeNow) >= timeout:
                    return ""
        else:
            readySet = select.select([self.clientSocket.fileno()], [], [], timeout)
            if len(readySet[0]) == 0:
                return ""
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
    # {{{ unqueue(self, timeout=15): Send all queued lines to server, honouring timers
    def unqueue(self, timeout=15):
        while self.clientQueue:
            msg = self.clientQueue[0]; msgLen = len(msg); msgBytesSent = 0;
            while msgBytesSent < msgLen:
                if self.clientNextTimeout:
                    timeNow = time.time()
                    if self.clientNextTimeout <= timeNow:
                        self.clientQueue[0] = msg; return True;
                    else:
                        readySet = select.select([], [self.clientSocket.fileno()], [], min(self.clientNextTimeout - timeNow, timeout))
                        if len(readySet[1]) == 0:
                            timeNow_ = time.time()
                            if (timeNow_ - timeNow) >= timeout:
                                return False
                            else:
                                self.clientQueue[0] = msg; return True;
                else:
                    readySet = select.select([], [self.clientSocket.fileno()], [], timeout)
                    if len(readySet[1]) == 0:
                        return False
                msgBytesSent = self.clientSocket.send(msg)
                msg = msg[msgBytesSent:]; msgLen -= msgBytesSent;
            del self.clientQueue[0]
        return True
    # }}}

    #
    # __init__(self, serverHname, serverPort, clientNick, clientIdent, clientGecos): initialisation method
    def __init__(self, serverHname, serverPort, clientNick, clientIdent, clientGecos):
        self.clientGecos, self.clientIdent, self.clientNick = clientGecos, clientIdent, clientNick
        self.clientNextTimeout, self.clientQueue, self.clientSocket, self.clientSocketFile = None, None, None, None
        self.serverHname, self.serverPort = serverHname, serverPort

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
