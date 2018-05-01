#!/usr/bin/env python3
#
# MiRCARTCanonicalise.py -- canonicalise mIRC art {from,to} file (for munki)
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

from MiRCARTCanvasImportStore import MiRCARTCanvasImportStore
import sys

def canonicalise(inPathName):
    canvasStore = MiRCARTCanvasImportStore(inPathName)
    inMap = canvasStore.outMap.copy(); del canvasStore;
    with open(inPathName, "w+") as outFile:
        lastAttribs = MiRCARTCanvasImportStore._CellState.CS_NONE
        lastColours = None
        for inCurRow in range(len(inMap)):
            for inCurCol in range(len(inMap[inCurRow])):
                inCurCell = inMap[inCurRow][inCurCol]
                if lastAttribs != inCurCell[2]:
                    if inCurCell[2] & MiRCARTCanvasImportStore._CellState.CS_BOLD:
                        print("\u0002", end="", file=outFile)
                    if inCurCell[2] & MiRCARTCanvasImportStore._CellState.CS_UNDERLINE:
                        print("\u001f", end="", file=outFile)
                    lastAttribs = inCurCell[2]
                if lastColours == None or lastColours != inCurCell[:2]:
                    print("\u0003{:02d},{:02d}{}".format(*inCurCell[:2], inCurCell[3]), end="", file=outFile)
                    lastColours = inCurCell[:2]
                else:
                    print(inCurCell[3], end="", file=outFile)
            print("\n", end="", file=outFile)

#
# Entry point
def main(*argv):
    canonicalise(argv[1])
if __name__ == "__main__":
    if (len(sys.argv) - 1) != 1:
        print("usage: {} <MiRCART input file pathname>".format(sys.argv[0]), file=sys.stderr)
    else:
        main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
