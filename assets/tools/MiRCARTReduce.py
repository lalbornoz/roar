#!/usr/bin/env python3
#
# MiRCARTReduce.py -- efficiently encode mIRC art {from,to} file
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

import os, sys
[sys.path.append(os.path.join(os.getcwd(), "..", "..", path)) for path in ["libcanvas", "librtl"]]

from CanvasImportStore import CanvasImportStore
import sys

def reduce(inPathName):
    canvasStore = CanvasImportStore(inPathName); inMap = canvasStore.outMap.copy();
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
                if  lastColours == None                     \
                or  (lastColours[0] != inCurCell[:2][0]     \
                and  lastColours[1] != inCurCell[:2][1]):
                    if (inCurCell[3] in set("0123456789")) and (inCurCell[1] < 10):
                        print("\u0003{:d},{:02d}{}".format(*inCurCell[:2], inCurCell[3]), end="", file=outFile)
                    else:
                        print("\u0003{:d},{:d}{}".format(*inCurCell[:2], inCurCell[3]), end="", file=outFile)
                    lastColours = inCurCell[:2]
                elif (lastColours[1] == inCurCell[:2][1])   \
                and  (lastColours[0] != inCurCell[:2][0]):
                    if (inCurCell[3] in set("0123456789")) and (inCurCell[0] < 10):
                        print("\u0003{:02d}{}".format(inCurCell[0], inCurCell[3]), end="", file=outFile)
                    else:
                        print("\u0003{:d}{}".format(inCurCell[0], inCurCell[3]), end="", file=outFile)
                    lastColours[0] = inCurCell[0]
                else:
                    print(inCurCell[3], end="", file=outFile)
            print("\n", end="", file=outFile)

#
# Entry point
def main(*argv):
    reduce(argv[1])
if __name__ == "__main__":
    if (len(sys.argv) - 1) != 1:
        print("usage: {} <MiRCART input file pathname>".format(sys.argv[0]), file=sys.stderr)
    else:
        main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
