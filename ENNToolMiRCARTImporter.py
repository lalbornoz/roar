#!/usr/bin/env python3
#
# ENNTool -- mIRC art animation tool (for EFnet #MiRCART) (WIP)
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT license.
#
# TODO:
# 1) un-Quick'n'Dirty-ify
#

import chardet

class ENNToolMiRCARTImporter(object):
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
        if cellState & bit:
            return cellState & ~bit
        else:
            return cellState | bit
    # }}}
    # {{{ _parseCharAsColourSpec(self, colourSpec, curColours): XXX
    def _parseCharAsColourSpec(self, colourSpec, curColours):
        if len(colourSpec) > 0:
            colourSpec = colourSpec.split(",")
            if  len(colourSpec) == 2                             \
            and len(colourSpec[1]) > 0:
                return [int(colourSpec[0] or curColours[0]),    \
                    int(colourSpec[1])]
            elif len(colourSpec) == 1                           \
            or   len(colourSpec[1]) == 0:
                return [int(colourSpec[0]), curColours[1]]
        else:
            return [15, 1]
    # }}}
    # {{{ fromTextFile(self, pathName): XXX
    def fromTextFile(self, pathName):
        with open(pathName, "rb") as fileObject:
            inFileEncoding = chardet.detect(fileObject.read())["encoding"]
        self.inFile = open(pathName, "r", encoding=inFileEncoding)
        self.inSize = self.outMap = None;
        inCurColourSpec = ""; inCurRow = -1;
        inLine = self.inFile.readline()
        inSize = [0, 0]; outMap = []; inMaxCols = 0;
        while inLine:
            inCellState = self._CellState.CS_NONE
            inParseState = self._ParseState.PS_CHAR
            inCurCol = 0; inMaxCol = len(inLine);
            inCurColourDigits = 0; inCurColours = [15, 1]; inCurColourSpec = "";
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
                        inCurColours = [15, 1]
                    elif inChar == "":
                        inCurColours = [inCurColours[1], inCurColours[0]]
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
                            inCurColours = self._parseCharAsColourSpec(      \
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
            inLine = self.inFile.readline()
        inSize[0] = inMaxCols; self.inSize = inSize; self.outMap = outMap;
        self.inFile.close()
    # }}}
    # {{{ __init__(self, inFile): initialisation method
    def __init__(self, inFile):
        self.inFile = inFile; self.inSize = self.outMap = None;
        self.fromTextFile(inFile)
    # }}}

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
