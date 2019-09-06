#!/usr/bin/env python3
#
# CanvasImportStore.py -- XXX
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

from Colours import AnsiBgToMiRCARTColours, AnsiFgToMiRCARTColours, AnsiFgBoldToMiRCARTColours
import os, re, struct, sys

class CanvasImportStore():
    """XXX"""
    # {{{ _CellState(): Cell state
    class _CellState():
        CS_NONE             = 0x00
        CS_BOLD             = 0x01
        CS_ITALIC           = 0x02
        CS_UNDERLINE        = 0x04
    # }}}

    # {{{ _flipCellStateBit(self, bit, cellState): XXX
    def _flipCellStateBit(self, bit, cellState):
        return cellState & ~bit if cellState & bit else cellState | bit
    # }}}

    # {{{ importAnsiBuffer(self, inFile, encoding="cp437", width=None): XXX
    def importAnsiBuffer(self, inFile, encoding="cp437", width=None):
        curBg, curBgAnsi, curBoldAnsi, curFg, curFgAnsi = 1, 30, False, 15, 37
        done, outMap, outMaxCols = False, [[]], 0
        inFileData = inFile.read().decode(encoding)
        inFileChar, inFileCharMax = 0, len(inFileData)
        while True:
            if inFileChar >= inFileCharMax:
                break
            else:
                m = re.match("\x1b\[((?:\d{1,3};?)+m|\d+C)", inFileData[inFileChar:])
                if m:
                    if m[1][-1] == "C":
                        outMap[-1] += [[curFg, curBg, self._CellState.CS_NONE, " "]] * int(m[1][:-1])
                    elif m[1][-1] == "m":
                        newBg, newFg = -1, -1
                        for ansiCode in [int(c) for c in m[1][:-1].split(";")]:
                            if ansiCode == 0:
                                curBgAnsi, curBoldAnsi, curFgAnsi, newBg, newFg = 30, False, 37, 1, 15
                            elif ansiCode == 1:
                                curBoldAnsi, newFg = True, AnsiFgBoldToMiRCARTColours[curFgAnsi]
                            elif ansiCode == 2:
                                curBoldAnsi, newFg = False, AnsiFgToMiRCARTColours[curFgAnsi]
                            elif ansiCode == 7:
                                curBgAnsi, curFgAnsi, newBg, newFg = curFgAnsi, curBgAnsi, curFg, curBg
                            elif ansiCode in AnsiBgToMiRCARTColours:
                                curBgAnsi, newBg = ansiCode, AnsiBgToMiRCARTColours[ansiCode]
                            elif ansiCode in AnsiFgBoldToMiRCARTColours:
                                curFgAnsi, newFg = ansiCode, AnsiFgBoldToMiRCARTColours[ansiCode]
                            elif ansiCode in AnsiFgToMiRCARTColours:
                                newFg = AnsiFgBoldToMiRCARTColours[ansiCode] if curBoldAnsi else AnsiFgToMiRCARTColours[ansiCode]
                                curFgAnsi = ansiCode
                        curBg = newBg if newBg != -1 else curBg; curFg = newFg if newFg != -1 else curFg;
                    inFileChar += len(m[0])
                elif inFileData[inFileChar:inFileChar + 2] == "\r\n":
                    done = True; inFileChar += 2;
                elif inFileData[inFileChar] in set("\r\n"):
                    done = True; inFileChar += 1;
                else:
                    outMap[-1].append([curFg, curBg, self._CellState.CS_NONE, inFileData[inFileChar]])
                    inFileChar += 1
                if done or (width == len(outMap[-1])):
                    done, outMaxCols, = False, max(outMaxCols, len(outMap[-1])); outMap.append([]);
        if len(outMap[0]):
            for numRow in range(len(outMap)):
                for numCol in range(len(outMap[numRow]), outMaxCols):
                    outMap[numRow].append([curFg, curBg, self._CellState.CS_NONE, " "])
            self.inSize, self.outMap = [outMaxCols, len(outMap)], outMap
            return (True, None)
        else:
            return (False, "empty output map")
    # }}}
    # {{{ importAnsiFile(self, inPathName, encoding="cp437"): XXX
    def importAnsiFile(self, inPathName, encoding="cp437"):
        return self.importAnsiBuffer(open(inPathName, "rb"), encoding)
    # }}}
    # {{{ importSauceFile(self, inPathName): XXX
    def importSauceFile(self, inPathName):
        with open(inPathName, "rb") as inFile:
            inFileStat = os.stat(inPathName); inFile.seek(inFileStat.st_size - 128, 0); inFile.seek(94);
            if inFile.read(2) == b'\x01\x01':
                width = struct.unpack("H", inFile.read(2))[0]
                inFile.seek(0, 0); inFileData = inFile.read(inFileStat.st_size - 128);
                return self.importAnsiFileBuffer(io.StringIO(inFileData), width)
            else:
                return (False, "only character based ANSi SAUCE files are supported")
    # }}}
    # {{{ importTextBuffer(self, inFile): XXX
    def importTextBuffer(self, inFile):
        inLine, outMap, outMaxCols = inFile.readline(), [], 0
        while inLine:
            inCellState, inCurCol, inCurColours, inMaxCol = self._CellState.CS_NONE, 0, (15, 1), len(inLine); outMap.append([]);
            while inCurCol < inMaxCol:
                inChar = inLine[inCurCol]
                if inChar in set("\r\n"):
                    inCurCol += 1
                elif inChar == "\u0002":
                    inCellState = self._flipCellStateBit(self._CellState.CS_BOLD, inCellState); inCurCol += 1;
                elif inChar == "\u0003":
                    m = re.match("\u0003((1[0-5]|0?[0-9])?(?:,(1[0-5]|0?[0-9]))?)", inLine[inCurCol:])
                    if m:
                        if (m[2] != None) and (m[3] != None):
                            inCurColours = (int(m[2]), int(m[3]))
                        elif (m[2] == None) and (m[3] != None):
                            inCurColours = (int(m[2]), int(curColours[1]))
                        else:
                            inCurColours = (15, 1)
                        inCurCol += len(m[0])
                    else:
                        inCurColours = (15, 1); inCurCol += 1;
                elif inChar == "\u0006":
                    inCellState = self._flipCellStateBit(self._CellState.CS_ITALIC, inCellState); inCurCol += 1;
                elif inChar == "\u000f":
                    inCellState |= self._CellState.CS_NONE; inCurColours = (15, 1); inCurCol += 1;
                elif inChar == "\u0016":
                    inCurColours = (inCurColours[1], inCurColours[0]); inCurCol += 1;
                elif inChar == "\u001f":
                    inCellState = self._flipCellStateBit(self._CellState.CS_UNDERLINE, inCellState); inCurCol += 1;
                else:
                    outMap[-1].append([*inCurColours, inCellState, inChar]); inCurCol += 1;
            inLine, outMaxCols = inFile.readline(), max(outMaxCols, len(outMap[-1]))
        if len(outMap[0]):
            self.inSize, self.outMap = [outMaxCols, len(outMap)], outMap
            return (True, None)
        else:
            return (False, "empty output map")
    # }}}
    # {{{ importTextFile(self, pathName): XXX
    def importTextFile(self, pathName):
        with open(pathName, "r", encoding="utf-8-sig") as inFile:
            return self.importTextBuffer(inFile)
    # }}}

    #
    # __init__(self, inFile=None): initialisation method
    def __init__(self, inFile=None):
        self.inSize, self.outMap = None, None
        if inFile != None:
            self.importTextFile(inFile)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
