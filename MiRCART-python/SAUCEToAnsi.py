#!/usr/bin/env python3
#
# SAUCEToAnsi.py -- convert SAUCE-encoded ANSi to raw ANSI file (for spoke)
# Copyright (c) 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

import os, re, struct, sys

def SAUCEToAnsi(inPathName, outPathName):
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
                while True:
                    if inFileChar >= inFileCharMax:
                        break
                    else:
                        m = re.match('\x1b\[((?:\d{1,3};?)+)m', inFileData[inFileChar:])
                        if m:
                            row += m[0]; inFileChar += len(m[0]);
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

#
# Entry point
def main(*argv):
    SAUCEToAnsi(argv[1], argv[2])
if __name__ == "__main__":
    if (len(sys.argv) - 1) != 2:
        print("usage: {} <SAUCE input file pathname> <ANSI output file pathname>".format(sys.argv[0]), file=sys.stderr)
    else:
        main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
