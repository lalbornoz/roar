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
    # {{{ _ParseState(): Parsing loop state
    class _ParseState():
        PS_CHAR             = 1
        PS_COLOUR_DIGIT0    = 2
        PS_COLOUR_DIGIT1    = 3
    # }}}

    # {{{ _flipCellStateBit(self, cellState, bit): XXX
    def _flipCellStateBit(self, cellState, bit):
        return cellState & ~bit if cellState & bit else cellState | bit
    # }}}
    # {{{ _parseCharAsColourSpec(self, colourSpec, curColours): XXX
    def _parseCharAsColourSpec(self, colourSpec, curColours):
        if len(colourSpec) > 0:
            colourSpec = colourSpec.split(",")
            if  len(colourSpec) == 2    \
            and len(colourSpec[1]) > 0:
                return (int(colourSpec[0] or curColours[0]), int(colourSpec[1]))
            elif len(colourSpec) == 1   \
            or   len(colourSpec[1]) == 0:
                return (int(colourSpec[0]), curColours[1])
        else:
            return (15, 1)
    # }}}

    # {{{ importAnsiFile(self, inPathName, encoding="cp437"): XXX
    def importAnsiFile(self, inPathName, encoding="cp437"):
        return self.importAnsiFileBuffer(open(inPathName, "rb"), encoding)
    # }}}
    # {{{ importAnsiFileBuffer(self, inFile, encoding="cp437"): XXX
    def importAnsiFileBuffer(self, inFile, encoding="cp437"):
        self.inSize, self.outMap = None, None; inMaxCols, inSize, outMap = 0, [0, 0], [[]];
        inFileData, row, rowChars = inFile.read().decode(encoding), "", 0
        inFileChar, inFileCharMax = 0, len(inFileData)
        curBg, curFg, done, inCurRow = 1, 15, False, 0; curBgAnsi, curBoldAnsi, curFgAnsi = 30, False, 37;
        while True:
            if inFileChar >= inFileCharMax:
                break
            else:
                m = re.match('\x1b\[((?:\d{1,3};?)+)m', inFileData[inFileChar:])
                if m:
                    newBg, newFg = -1, -1
                    for ansiCode in m[1].split(";"):
                        ansiCode = int(ansiCode)
                        if ansiCode == 0:
                            curBgAnsi, curBoldAnsi, curFgAnsi = 30, False, 37; newBg, newFg = 1, 15;
                        elif ansiCode == 1:
                            curBoldAnsi, newFg = True, AnsiFgBoldToMiRCARTColours[curFgAnsi]
                        elif ansiCode == 2:
                            curBoldAnsi, newFg = False, AnsiFgToMiRCARTColours[curFgAnsi]
                        elif ansiCode == 7:
                            newBg, newFg = curFg, curBg; curBgAnsi, curFgAnsi = curFgAnsi, curBgAnsi;
                        elif ansiCode in AnsiBgToMiRCARTColours:
                            curBgAnsi, newBg = ansiCode, AnsiBgToMiRCARTColours[ansiCode]
                        elif ansiCode in AnsiFgToMiRCARTColours:
                            if curBoldAnsi:
                                newFg = AnsiFgBoldToMiRCARTColours[ansiCode]
                            else:
                                newFg = AnsiFgToMiRCARTColours[ansiCode]
                            curFgAnsi = ansiCode
                        elif ansiCode in AnsiFgBoldToMiRCARTColours:
                            curFgAnsi, newFg = ansiCode, AnsiFgBoldToMiRCARTColours[ansiCode]
                    if  ((newBg != -1) and (newFg != -1))   \
                    and ((newBg == curFg) and (newFg == curBg)):
                        curBg, curFg = newBg, newFg
                    elif ((newBg != -1) and (newFg != -1))  \
                    and  ((newBg != curBg) and (newFg != curFg)):
                        curBg, curFg = newBg, newFg
                    elif (newBg != -1) and (newBg != curBg):
                        curBg = newBg
                    elif (newFg != -1) and (newFg != curFg):
                        curFg = newFg
                    inFileChar += len(m[0])
                else:
                    m = re.match('\x1b\[(\d+)C', inFileData[inFileChar:])
                    if m:
                        for numRepeat in range(int(m[1])):
                            outMap[inCurRow].append([curFg, curBg, self._CellState.CS_NONE, " "])
                        inFileChar += len(m[0])
                    elif inFileData[inFileChar:inFileChar+2] == "\r\n":
                        inFileChar += 2; done = True;
                    elif inFileData[inFileChar] == "\r" \
                    or   inFileData[inFileChar] == "\n":
                        inFileChar += 1; done = True;
                    else:
                        outMap[inCurRow].append([curFg, curBg, self._CellState.CS_NONE, inFileData[inFileChar]])
                        inFileChar += 1; rowChars += 1;
                if done:
                    inMaxCols = max(inMaxCols, len(outMap[inCurRow])); inSize[1] += 1;
                    done = False; rowChars = 0; inCurRow += 1; outMap.append([]);
        inSize[0] = inMaxCols
        for numRow in range(inSize[1]):
            for numCol in range(len(outMap[numRow]), inSize[0]):
                outMap[numRow].append([curFg, curBg, self._CellState.CS_NONE, " "])
        self.inSize, self.outMap = inSize, outMap
    # }}}
    # {{{ importIntoPanel(self): XXX
    def importIntoPanel(self):
        self.parentCanvas.onStoreUpdate(self.inSize, self.outMap)
    # }}}
    # {{{ importNew(self, newCanvasSize=None): XXX
    def importNew(self, newCanvasSize=None):
        newMap = [[[1, 1, 0, " "]                   \
                for x in range(newCanvasSize[0])]   \
                    for y in range(newCanvasSize[1])]
        self.parentCanvas.onStoreUpdate(newCanvasSize, newMap)
    # }}}
    # {{{ importSauceFile(self, inPathName): XXX
    def importSauceFile(self, inPathName):
        with open(inPathName, "rb") as inFile:
            self.inSize, self.outMap = None, None; inMaxCols, inSize, outMap = 0, [0, 0], [[]];
            inFileStat = os.stat(inPathName)
            inFile.seek(inFileStat.st_size - 128, 0)
            inFile.seek(5 + 2 + 35 + 20 + 20 + 8 + 4, 1)
            if  (inFile.read(1) == b'\x01') \
            and (inFile.read(1) == b'\x01'):
                width, height = struct.unpack("H", inFile.read(2))[0], struct.unpack("H", inFile.read(2))[0]
                inFile.seek(0, 0)
                inFileData, row, rowChars = inFile.read(inFileStat.st_size - 128).decode("cp437"), "", 0
                inFileChar, inFileCharMax = 0, len(inFileData)
                curBg, curFg, inCurRow = 1, 15, 0; curBgAnsi, curBoldAnsi, curFgAnsi = 30, False, 37;
                while True:
                    if inFileChar >= inFileCharMax:
                        break
                    else:
                        m = re.match('\x1b\[((?:\d{1,3};?)+)m', inFileData[inFileChar:])
                        if m:
                            newBg, newFg = -1, -1
                            for ansiCode in m[1].split(";"):
                                ansiCode = int(ansiCode)
                                if ansiCode == 0:
                                    curBgAnsi, curBoldAnsi, curFgAnsi = 30, False, 37; newBg, newFg = 1, 15;
                                elif ansiCode == 1:
                                    curBoldAnsi, newFg = True, AnsiFgBoldToMiRCARTColours[curFgAnsi]
                                elif ansiCode == 2:
                                    curBoldAnsi, newFg = False, AnsiFgToMiRCARTColours[curFgAnsi]
                                elif ansiCode == 7:
                                    newBg, newFg = curFg, curBg; curBgAnsi, curFgAnsi = curFgAnsi, curBgAnsi;
                                elif ansiCode in AnsiBgToMiRCARTColours:
                                    curBgAnsi, newBg = ansiCode, AnsiBgToMiRCARTColours[ansiCode]
                                elif ansiCode in AnsiFgToMiRCARTColours:
                                    if curBoldAnsi:
                                        newFg = AnsiFgBoldToMiRCARTColours[ansiCode]
                                    else:
                                        newFg = AnsiFgToMiRCARTColours[ansiCode]
                                    curFgAnsi = ansiCode
                                elif ansiCode in AnsiFgBoldToMiRCARTColours:
                                    curFgAnsi, newFg = ansiCode, AnsiFgBoldToMiRCARTColours[ansiCode]
                            if  ((newBg != -1) and (newFg != -1))   \
                            and ((newBg == curFg) and (newFg == curBg)):
                                curBg, curFg = newBg, newFg
                            elif ((newBg != -1) and (newFg != -1))  \
                            and  ((newBg != curBg) and (newFg != curFg)):
                                curBg, curFg = newBg, newFg
                            elif (newBg != -1) and (newBg != curBg):
                                curBg = newBg
                            elif (newFg != -1) and (newFg != curFg):
                                curFg = newFg
                            inFileChar += len(m[0])
                        else:
                            m = re.match('\x1b\[(\d+)C', inFileData[inFileChar:])
                            if m:
                                for numRepeat in range(int(m[1])):
                                    outMap[inCurRow].append([curFg, curBg, self._CellState.CS_NONE, " "])
                                inFileChar += len(m[0])
                            elif inFileData[inFileChar:inFileChar+2] == "\r\n":
                                inFileChar += 2; rowChars = width;
                            elif inFileData[inFileChar] == "\r"     \
                            or   inFileData[inFileChar] == "\n":
                                inFileChar += 1; rowChars = width;
                            else:
                                outMap[inCurRow].append([curFg, curBg, self._CellState.CS_NONE, inFileData[inFileChar]])
                                inFileChar += 1; rowChars += 1;
                        if rowChars >= width:
                            inMaxCols = max(inMaxCols, len(outMap[inCurRow])); inSize[1] += 1;
                            rowChars = 0; inCurRow += 1; outMap.append([]);
                inSize[0] = inMaxCols
                for numRow in range(inSize[1]):
                    for numCol in range(len(outMap[numRow]), inSize[0]):
                        outMap[numRow].append([curFg, curBg, self._CellState.CS_NONE, " "])
                self.inSize, self.outMap = inSize, outMap
    # }}}
    # {{{ importTextFile(self, pathName): XXX
    def importTextFile(self, pathName):
        return self.importTextFileBuffer(open(pathName, "r", encoding="utf-8-sig"))
    # }}}
    # {{{ importTextFileBuffer(self, inFile): XXX
    def importTextFileBuffer(self, inFile):
        self.inSize, self.outMap = None, None
        inCurColourSpec, inCurRow, inMaxCols, inSize, outMap = "", -1, 0, [0, 0], []
        inLine = inFile.readline()
        while inLine:
            inCellState = self._CellState.CS_NONE
            inParseState = self._ParseState.PS_CHAR
            inCurCol = 0; inMaxCol = len(inLine);
            inCurColourDigits = 0; inCurColours = (15, 1); inCurColourSpec = "";
            inCurRow += 1; outMap.append([]); inRowCols = 0; inSize[1] += 1;
            while inCurCol < inMaxCol:
                inChar = inLine[inCurCol]
                if inChar in set("\r\n"):                                   \
                    inCurCol += 1
                elif inParseState == self._ParseState.PS_CHAR:
                    inCurCol += 1
                    if inChar == "":
                        inCellState = self._flipCellStateBit(               \
                            inCellState, self._CellState.CS_BOLD)
                    elif inChar == "":
                        inParseState = self._ParseState.PS_COLOUR_DIGIT0
                    elif inChar == "":
                        inCellState = self._flipCellStateBit(               \
                            inCellState, self._CellState.CS_ITALIC)
                    elif inChar == "":
                        inCellState |= self._CellState.CS_NONE
                        inCurColours = (15, 1)
                    elif inChar == "":
                        inCurColours = (inCurColours[1], inCurColours[0])
                    elif inChar == "":
                        inCellState = self._flipCellStateBit(               \
                            inCellState, self._CellState.CS_UNDERLINE)
                    else:
                        inRowCols += 1
                        outMap[inCurRow].append([*inCurColours, inCellState, inChar])
                elif inParseState == self._ParseState.PS_COLOUR_DIGIT0      \
                or   inParseState == self._ParseState.PS_COLOUR_DIGIT1:
                    if  inChar == ","                                       \
                    and inParseState == self._ParseState.PS_COLOUR_DIGIT0:
                        if  (inCurCol + 1) < inMaxCol                       \
                        and not inLine[inCurCol + 1] in set("0123456789"):
                            inCurColours = self._parseCharAsColourSpec(     \
                                inCurColourSpec, inCurColours)
                            inCurColourDigits = 0; inCurColourSpec = "";
                            inParseState = self._ParseState.PS_CHAR
                        else:
                            inCurCol += 1
                            inCurColourDigits = 0; inCurColourSpec += inChar;
                            inParseState = self._ParseState.PS_COLOUR_DIGIT1
                    elif inChar in set("0123456789")                        \
                    and  inCurColourDigits == 0:
                        inCurCol += 1
                        inCurColourDigits += 1; inCurColourSpec += inChar;
                    elif inChar in set("0123456789")                        \
                    and  inCurColourDigits == 1                             \
                    and  inCurColourSpec[-1] == "0":
                        inCurCol += 1
                        inCurColourDigits += 1; inCurColourSpec += inChar;
                    elif inChar in set("012345")                            \
                    and  inCurColourDigits == 1                             \
                    and  inCurColourSpec[-1] == "1":
                        inCurCol += 1
                        inCurColourDigits += 1; inCurColourSpec += inChar;
                    else:
                        inCurColours = self._parseCharAsColourSpec(         \
                            inCurColourSpec, inCurColours)
                        inCurColourDigits = 0; inCurColourSpec = "";
                        inParseState = self._ParseState.PS_CHAR
            inMaxCols = max(inMaxCols, inRowCols)
            inLine = inFile.readline()
        inSize[0] = inMaxCols; self.inSize, self.outMap = inSize, outMap;
        inFile.close()
    # }}}

    #
    # __init__(self, inFile=None, parentCanvas=None): initialisation method
    def __init__(self, inFile=None, parentCanvas=None):
        self.inSize, self.outMap, self.parentCanvas = None, None, parentCanvas
        if inFile != None:
            self.importTextFile(inFile)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
