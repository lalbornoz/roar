#!/usr/bin/env python3
#
# MiRCARTCanonicalise.py -- canonicalise mIRC art {from,to} file (for munki)
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

import os, sys
[sys.path.append(os.path.join(os.getcwd(), "..", "..", path)) for path in ["libcanvas", "librtl"]]

from CanvasImportStore import CanvasImportStore

def canonicalise(inPathName):
    canvasStore = CanvasImportStore(inPathName)
    inMap = canvasStore.outMap.copy(); del canvasStore;
    with open(inPathName, "w+") as outFile:
        for inCurRow in range(len(inMap)):
            lastAttribs, lastColours = CanvasImportStore._CellState.CS_NONE, None
            for inCurCol in range(len(inMap[inCurRow])):
                inCurCell = inMap[inCurRow][inCurCol]
                if lastAttribs != inCurCell[2]:
                    if inCurCell[2] & CanvasImportStore._CellState.CS_BOLD:
                        print("\u0002", end="", file=outFile)
                    if inCurCell[2] & CanvasImportStore._CellState.CS_UNDERLINE:
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
