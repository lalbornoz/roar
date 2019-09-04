#!/usr/bin/env python3
#
# SAUCEToMiRCART.py -- convert SAUCE-encoded ANSi to mIRC art file (for spoke)
# Copyright (c) 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

import os, re, struct, sys

AnsiBgToMiRCARTColours = {
    107: 0,  # Bright White
    40:  1,  # Black
    104: 2,  # Blue
    42:  3,  # Green
    101: 4,  # Red
    41:  5,  # Light Red
    45:  6,  # Pink
    43:  7,  # Yellow
    103: 8,  # Light Yellow
    102: 9,  # Light Green
    46:  10, # Cyan
    106: 11, # Light Cyan
    44:  12, # Light Blue
    105: 13, # Light Pink
    100: 14, # Grey
    47:  15, # Light Grey
};

AnsiFgToMiRCARTColours = {
    97: 0,  # Bright White
    30: 1,  # Black
    94: 2,  # Blue
    32: 3,  # Green
    91: 4,  # Red
    31: 5,  # Light Red
    35: 6,  # Pink
    33: 7,  # Yellow
    93: 8,  # Light Yellow
    92: 9,  # Light Green
    36: 10, # Cyan
    96: 11, # Light Cyan
    34: 12, # Light Blue
    95: 13, # Light Pink
    90: 14, # Grey
    37: 15, # Light Grey
};

AnsiFgBoldToMiRCARTColours = {
    97: 0,  # Bright White
    30: 14, # Grey
    94: 12, # Light Blue
    32: 9,  # Light Green
    91: 4,  # Light Red
    31: 4,  # Light Red
    35: 13, # Light Pink
    33: 8,  # Light Yellow
    93: 8,  # Light Yellow
    92: 9,  # Light Green
    36: 11, # Light Cyan
    96: 11, # Light Cyan
    34: 12, # Light Blue
    95: 13, # Light Pink
    90: 14, # Grey
    37: 0,  # Bright White
};

def SAUCEToMiRCART(inPathName, outPathName):
    with open(inPathName, "rb") as inFile:
        inFileStat = os.stat(inPathName)
        inFile.seek(inFileStat.st_size - 128, 0)
        inFile.seek(5 + 2 + 35 + 20 + 20 + 8 + 4, 1)
        if (inFile.read(1) != b'\x01')                              \
        or (inFile.read(1) != b'\x01'):
            print("error: only character based ANSi SAUCE files are supported.", file=sys.stderr)
            return 1
        else:
            width, height = struct.unpack("H", inFile.read(2))[0], struct.unpack("H", inFile.read(2))[0]
            with open(outPathName, "w+") as outFile:
                inFile.seek(0, 0)
                inFileData, row, rowChars = inFile.read(inFileStat.st_size - 128).decode("cp437"), "", 0
                inFileChar, inFileCharMax = 0, len(inFileData)
                curBg, curFg = 1, 15; curBgAnsi, curBoldAnsi, curFgAnsi = 30, False, 37;
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
                                row += "\u0016"; curBg, curFg = newBg, newFg;
                            elif ((newBg != -1) and (newFg != -1))  \
                            and  ((newBg != curBg) and (newFg != curFg)):
                                row += "\u0003{},{}".format(newFg, newBg); curBg, curFg = newBg, newFg;
                            elif (newBg != -1) and (newBg != curBg):
                                row += "\u0003{},{}".format(curFg, newBg); curBg = newBg;
                            elif (newFg != -1) and (newFg != curFg):
                                row += "\u0003{}".format(newFg); curFg = newFg;
                            inFileChar += len(m[0])
                        else:
                            m = re.match('\x1b\[(\d+)C', inFileData[inFileChar:])
                            if m:
                                row += m[0]; inFileChar += len(m[0]); rowChars += int(m[1]);
                            elif inFileData[inFileChar:inFileChar+2] == "\r\n":
                                inFileChar += 2; rowChars = width;
                            elif inFileData[inFileChar] == "\r"     \
                            or   inFileData[inFileChar] == "\n":
                                inFileChar += 1; rowChars = width;
                            else:
                                row += inFileData[inFileChar]; inFileChar += 1; rowChars += 1;
                        if rowChars >= width:
                            print(row, file=outFile); row = ""; rowChars = 0;
                            if (curBg != 1) and (curFg != 15):
                                row += "\u0003{},{}".format(curFg, curBg);
                            elif curBg != 1:
                                row += "\u0003{},{}".format(curFg, curBg);
                            elif curFg != 1:
                                row += "\u0003{}".format(curFg);
#
# Entry point
def main(*argv):
    SAUCEToMiRCART(argv[1], argv[2])
if __name__ == "__main__":
    if (len(sys.argv) - 1) != 2:
        print("usage: {} <SAUCE input file pathname> <mIRC art output file pathname>".format(sys.argv[0]), file=sys.stderr)
    else:
        main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
