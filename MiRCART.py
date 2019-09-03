#!/usr/bin/env python3
#
# MiRCART.py -- mIRC art editor for Windows & Linux
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import os, sys
[sys.path.append(os.path.join(os.getcwd(), path)) for path in   \
    ["libcanvas", "libgui", "librtl", "libtools"]]

from MiRCARTFrame import MiRCARTFrame
import wx

#
# Entry point
def main(*argv):
    wxApp = wx.App(False)
    appFrame = MiRCARTFrame(None)
    if  len(argv) > 1    \
    and len(argv[1]) > 0:
        appFrame.panelCanvas.canvasInterface.canvasPathName = argv[1]
        appFrame.panelCanvas.canvasImportStore.importTextFile(argv[1])
        appFrame.panelCanvas.canvasImportStore.importIntoPanel()
        appFrame.onCanvasUpdate(pathName=argv[1], undoLevel=-1)
    wxApp.MainLoop()
if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
