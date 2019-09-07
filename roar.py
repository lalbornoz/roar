#!/usr/bin/env python3
#
# roar.py -- mIRC art editor for Windows & Linux
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import os, sys
[sys.path.append(os.path.join(os.getcwd(), path)) for path in   \
    ["libcanvas", "libgui", "librtl", "libtools"]]

from GuiFrame import GuiFrame
import wx

#
# Entry point
def main(*argv):
    wxApp = wx.App(False)
    appFrame = GuiFrame(None)
    if  len(argv) > 1    \
    and len(argv[1]) > 0:
        appFrame.canvasPanel.interface.canvasPathName = argv[1]
        rc, error = appFrame.canvasPanel.canvas.importStore.importTextFile(argv[1])
        if rc:
            appFrame.canvasPanel.update(appFrame.canvasPanel.canvas.importStore.inSize, False, appFrame.canvasPanel.canvas.importStore.outMap)
            appFrame.update(pathName=argv[1], undoLevel=-1)
        else:
            print("error: {}".format(error), file=sys.stderr)
    wxApp.MainLoop()
if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
