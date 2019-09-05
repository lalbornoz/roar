#!/usr/bin/env python3
#
# SAUCEToMiRCART.py -- convert SAUCE-encoded ANSi to mIRC art file (for spoke)
# Copyright (c) 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

import os, sys
[sys.path.append(os.path.join(os.getcwd(), "..", "..", path)) for path in ["libcanvas", "librtl"]]

from CanvasExportStore import CanvasExportStore
from CanvasImportStore import CanvasImportStore

#
# Entry point
def main(*argv):
    if (len(sys.argv) - 1) != 2:
        print("usage: {} <SAUCE input file pathname> <mIRC art output file pathname>".format(sys.argv[0]), file=sys.stderr)
    else:
        canvasImportStore = CanvasImportStore()
        canvasImportStore.importSauceFile(argv[1])
        canvasExportStore = CanvasExportStore()
        with open(argv[2], "w", encoding="utf-8") as outFile:
            canvasExportStore.exportTextFile(canvasImportStore.outMap, canvasImportStore.inSize, outFile)
if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
