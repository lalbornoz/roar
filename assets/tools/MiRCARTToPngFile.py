#!/usr/bin/env python3
#
# MiRCARTToPngFile.py -- convert ASCII w/ mIRC control codes to monospaced PNG (for EFnet #MiRCART)
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

import os, sys
[sys.path.append(os.path.join(os.getcwd(), "..", "..", path)) for path in ["libcanvas", "librtl"]]

from CanvasExportStore import CanvasExportStore
from CanvasImportStore import CanvasImportStore
from getopt import getopt, GetoptError

#
# Entry point
def main(*argv):
    argv0 = argv[0]; optlist, argv = getopt(argv[1:], "f:hs:"); optdict = dict(optlist);
    if len(argv) < 1:
        print("""usage: {} [-f fname] [-h] [-s size] fname...
       -h.........: show this screen
       -f fname...: font file pathname (defaults to: ../fonts/DejaVuSansMono.ttf)
       -s size....: font size (defaults to: 11)""".format(argv0), file=sys.stderr)
    else:
        if not "-f" in optdict:
            optdict["-f"] = os.path.join("..", "fonts", "DejaVuSansMono.ttf")
        optdict["-s"] = 11 if not "-s" in optdict else int(optdict["-s"])
        for inFile in argv:
            canvasImportStore = CanvasImportStore()
            rc, error = canvasImportStore.importTextFile(inFile)
            if rc:
                canvasExportStore = CanvasExportStore()
                canvasExportStore.exportPngFile(canvasImportStore.outMap, optdict["-f"], optdict["-s"], os.path.splitext(inFile)[0] + ".png")
            else:
                print("error: {}".format(error), file=sys.stderr)
if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
