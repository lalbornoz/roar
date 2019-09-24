#!/usr/bin/env python3
#
# CanvasImportStore.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

from CanvasColours import AnsiBgToMiRCARTColours, AnsiFgToMiRCARTColours, AnsiFgBoldToMiRCARTColours
import io, os, re, struct, sys

class CanvasImportStore():
    class _CellState():
        CS_NONE             = 0x00
        CS_BOLD             = 0x01
        CS_ITALIC           = 0x02
        CS_UNDERLINE        = 0x04

    def _flipCellStateBit(self, bit, cellState):
        return cellState & ~bit if cellState & bit else cellState | bit

    def importAnsiBuffer(self, inBuffer, encoding="cp437", width=None):
        curBg, curBgAnsi, curBoldAnsi, curFg, curFgAnsi = -1, 30, False, 15, 37
        done, outMap, outMaxCols = False, [[]], 0
        inBufferData = inBuffer.decode(encoding)
        inBufferChar, inBufferCharMax = 0, len(inBufferData)
        while True:
            if inBufferChar >= inBufferCharMax:
                break
            else:
                m = re.match("\x1b\[((?:\d{1,3};?)+m|\d+[ABCDEFG])", inBufferData[inBufferChar:])
                if m:
                    if m[1][-1] == "C":
                        outMap[-1] += [[curFg, curBg, self._CellState.CS_NONE, " "]] * int(m[1][:-1])
                    elif m[1][-1] == "m":
                        newBg, newFg = -1, -1
                        for ansiCode in [int(c) for c in m[1][:-1].split(";")]:
                            if ansiCode == 0:
                                curBgAnsi, curBoldAnsi, curFgAnsi, newBg, newFg = 30, False, 37, -1, 15
                            elif ansiCode == 1:
                                curBoldAnsi, newFg = True, AnsiFgBoldToMiRCARTColours[curFgAnsi]
                            elif ansiCode == 2:
                                curBoldAnsi, newFg = False, AnsiFgToMiRCARTColours[curFgAnsi]
                            elif ansiCode == 7:
                                curBgAnsi, curFgAnsi, newBg, newFg = curFgAnsi, curBgAnsi, curFg, curBg
                            elif (not curBoldAnsi) and (ansiCode in AnsiBgToMiRCARTColours):
                                curBgAnsi, newBg = ansiCode, AnsiBgToMiRCARTColours[ansiCode]
                            elif curBoldAnsi and (ansiCode in AnsiFgBoldToMiRCARTColours):
                                curFgAnsi, newFg = ansiCode, AnsiFgBoldToMiRCARTColours[ansiCode]
                            elif ansiCode in AnsiFgToMiRCARTColours:
                                newFg = AnsiFgBoldToMiRCARTColours[ansiCode] if curBoldAnsi else AnsiFgToMiRCARTColours[ansiCode]
                                curFgAnsi = ansiCode
                        curBg = newBg if newBg != -1 else curBg; curFg = newFg if newFg != -1 else curFg;
                    inBufferChar += len(m[0])
                elif inBufferData[inBufferChar:inBufferChar + 2] == "\r\n":
                    done = True; inBufferChar += 2;
                elif inBufferData[inBufferChar] in set("\r\n"):
                    done = True; inBufferChar += 1;
                else:
                    outMap[-1].append([curFg, curBg, self._CellState.CS_NONE, inBufferData[inBufferChar]])
                    inBufferChar += 1
                if done or (width == len(outMap[-1])):
                    done, outMaxCols, = False, max(outMaxCols, len(outMap[-1])); outMap.append([]);
        if (len(outMap) > 1)    \
        or ((len(outMap) == 1) and len(outMap[0])):
            for numRow in range(len(outMap)):
                for numCol in range(len(outMap[numRow]), outMaxCols):
                    outMap[numRow].append([15, -1, self._CellState.CS_NONE, " "])
            self.inSize, self.outMap = [outMaxCols, len(outMap)], outMap
            return (True, None)
        else:
            return (False, "empty output map")

    def importAnsiFile(self, inPathName, encoding="cp437"):
        return self.importAnsiBuffer(open(inPathName, "rb").read(), encoding)

    def importSauceFile(self, inPathName, encoding="cp437"):
        with open(inPathName, "rb") as inFile:
            inFileStat = os.stat(inPathName)
            inFile.seek(inFileStat.st_size - 128, os.SEEK_SET); inFile.seek(94, os.SEEK_CUR);
            if inFile.read(2) == b'\x01\x01':
                width = struct.unpack("H", inFile.read(2))[0]
                inFile.seek(0, 0); inFileData = inFile.read(inFileStat.st_size - 128);
                return self.importAnsiBuffer(inFileData, encoding, width)
            else:
                return (False, "only character based ANSi SAUCE files are supported")

    def importTextBuffer(self, inFile):
        try:
            inLine, outMap, outMaxCols = inFile.readline(), [], 0
            while inLine:
                inCellState, inCurCol, inCurColours, inMaxCol = self._CellState.CS_NONE, 0, (15, -1), len(inLine); outMap.append([]);
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
                            elif (m[2] != None) and (m[3] == None):
                                inCurColours = (int(m[2]), int(inCurColours[1]))
                            else:
                                inCurColours = (15, -1)
                            inCurCol += len(m[0])
                        else:
                            inCurColours = (15, -1); inCurCol += 1;
                    elif inChar == "\u0006":
                        inCellState = self._flipCellStateBit(self._CellState.CS_ITALIC, inCellState); inCurCol += 1;
                    elif inChar == "\u000f":
                        inCellState |= self._CellState.CS_NONE; inCurColours = (15, -1); inCurCol += 1;
                    elif inChar == "\u0016":
                        inCurColours = (inCurColours[1], inCurColours[0]); inCurCol += 1;
                    elif inChar == "\u001f":
                        inCellState = self._flipCellStateBit(self._CellState.CS_UNDERLINE, inCellState); inCurCol += 1;
                    elif inChar == "\t":
                        for tabChar in range(8 - len(outMap[-1]) % 8):
                            outMap[-1].append([*inCurColours, inCellState, inChar])
                        inCurCol += 1
                    else:
                        outMap[-1].append([*inCurColours, inCellState, inChar]); inCurCol += 1;
                inLine, outMaxCols = inFile.readline(), max(outMaxCols, len(outMap[-1]))
            if (len(outMap) > 1)    \
            or ((len(outMap) == 1) and len(outMap[0])):
                for numRow in range(len(outMap)):
                    for numCol in range(len(outMap[numRow]), outMaxCols):
                        outMap[numRow].append([15, -1, self._CellState.CS_NONE, " "])
                self.inSize, self.outMap = [outMaxCols, len(outMap)], outMap
                return (True, None)
            else:
                return (False, "empty output map")
        except:
            return (False, sys.exc_info()[1])

    def importTextFile(self, pathName):
        with open(pathName, "r", encoding="utf-8-sig") as inFile:
            return self.importTextBuffer(inFile)

    def __init__(self, inFile=None):
        self.inSize, self.outMap = None, None
        if inFile != None:
            self.importTextFile(inFile)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
