#!/usr/bin/env python3
#
# roar.py -- mIRC art editor for Windows & Linux
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import os, sys
[sys.path.append(os.path.join(os.getcwd(), path)) for path in   \
    ["libcanvas", "libgui", "libroar", "librtl", "libtools"]]

from RoarClient import RoarClient
import wx

#
# Entry point
def main(*argv):
    wxApp, roarClient = wx.App(False), RoarClient(None)
    if len(argv) >= 1:
        if argv[2].endswith(".lst"):
            roarClient.assetsWindow._load_list(argv[2])
        roarClient.canvasPanel.commands.canvasPathName = argv[1]
        rc, error = roarClient.canvasPanel.canvas.importStore.importTextFile(argv[1])
        if rc:
            roarClient.canvasPanel.update(roarClient.canvasPanel.canvas.importStore.inSize, False, roarClient.canvasPanel.canvas.importStore.outMap)
            roarClient.canvasPanel.commands.update(pathName=argv[1], undoLevel=-1)
        else:
            print("error: {}".format(error), file=sys.stderr)
    wxApp.MainLoop()
if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
