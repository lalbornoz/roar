#!/usr/bin/env python3
#
# MiRCARTToAnsi.py -- ToAnsi mIRC art {from,to} file (for munki)
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

import os, sys
[sys.path.append(os.path.join(os.getcwd(), "..", "..", path)) for path in ["libcanvas", "librtl"]]

from CanvasExportStore import CanvasExportStore
from CanvasImportStore import CanvasImportStore

#
# Entry point
def main(*argv):
    if (len(sys.argv) - 1) != 1:
        print("usage: {} <MiRCART input file pathname>".format(sys.argv[0]), file=sys.stderr)
    else:
        canvasImportStore = CanvasImportStore()
        rc, error = canvasImportStore.importTextFile(argv[1])
        if rc:
            canvasExportStore = CanvasExportStore()
            canvasExportStore.exportAnsiFile(canvasImportStore.outMap, canvasImportStore.inSize, sys.stdout)
        else:
            print("error: {}".format(error), file=sys.stderr)
if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
