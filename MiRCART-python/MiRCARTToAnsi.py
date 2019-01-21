#!/usr/bin/env python3
#
# MiRCARTToAnsi.py -- ToAnsi mIRC art {from,to} file (for munki)
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

from MiRCARTCanvasImportStore import MiRCARTCanvasImportStore
import sys

MiRCARTToAnsiColours = [
    97,    # Bright White 
    30,    # Black        
    94,    # Light Blue   
    32,    # Green        
    91,    # Red          
    31,    # Light Red    
    35,    # Pink         
    33,    # Yellow       
    93,    # Light Yellow 
    92,    # Light Green  
    36,    # Cyan         
    96,    # Light Cyan   
    34,    # Blue         
    95,    # Light Pink   
    90,    # Grey         
    37,    # Light Grey   
];

def ToAnsi(inPathName):
    canvasStore = MiRCARTCanvasImportStore(inPathName)
    inMap = canvasStore.outMap.copy(); del canvasStore;
    with open(inPathName, "w+") as outFile:
        for inCurRow in range(len(inMap)):
            lastAttribs = MiRCARTCanvasImportStore._CellState.CS_NONE
            lastColours = None
            for inCurCol in range(len(inMap[inCurRow])):
                inCurCell = inMap[inCurRow][inCurCol]
                if lastAttribs != inCurCell[2]:
                    if inCurCell[2] & MiRCARTCanvasImportStore._CellState.CS_BOLD:
                        print("\u001b[1m", end="", file=outFile)
                    if inCurCell[2] & MiRCARTCanvasImportStore._CellState.CS_UNDERLINE:
                        print("\u001b[4m", end="", file=outFile)
                    lastAttribs = inCurCell[2]
                if lastColours == None or lastColours != inCurCell[:2]:
                    ansiBg = MiRCARTToAnsiColours[int(inCurCell[1])] + 10
                    ansiFg = MiRCARTToAnsiColours[int(inCurCell[0])]
                    print("\u001b[{:02d}m\u001b[{:02d}m{}".format(ansiBg, ansiFg, inCurCell[3]), end="", file=outFile)
                    lastColours = inCurCell[:2]
                else:
                    print(inCurCell[3], end="", file=outFile)
            print("\u001b[0m\n", end="", file=outFile)

#
# Entry point
def main(*argv):
    ToAnsi(argv[1])
if __name__ == "__main__":
    if (len(sys.argv) - 1) != 1:
        print("usage: {} <MiRCART input file pathname>".format(sys.argv[0]), file=sys.stderr)
    else:
        main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
