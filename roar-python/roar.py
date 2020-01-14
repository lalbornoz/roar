#!/usr/bin/env python3
#
# roar.py -- mIRC art editor for Windows & Linux
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import os, sys
[sys.path.append(os.path.join(os.getcwd(), path)) for path in   \
    ["libcanvas", "libgui", "libroar", "librtl", "liboperators", "libtools"]]

from RoarClient import RoarClient
from RtlPlatform import getLocalConfPathName
import wx

#
# Entry point
def main(*argv):
    localConfDirName = getLocalConfPathName()
    if not os.path.exists(localConfDirName):
        os.makedirs(localConfDirName)
    wxApp, roarClient = wx.App(False), RoarClient(None)
    argv0, argv = argv[0], argv[1:]
    roarClient.canvasPanel.commands._recentDirLoad(); roarClient.canvasPanel.commands._recentLoad();
    if len(argv) >= 1:
        if (len(argv) >= 2) and (argv[1].endswith(".lst")):
            roarClient.assetsWindow._load_list(argv[1])
        roarClient.canvasPanel.commands.canvasPathName = argv[0]
        roarClient.canvasPanel._snapshotsReset()
        rc, error = roarClient.canvasPanel.canvas.importStore.importTextFile(argv[0])
        if rc:
            roarClient.canvasPanel.update(roarClient.canvasPanel.canvas.importStore.inSize, False, roarClient.canvasPanel.canvas.importStore.outMap, dirty=False)
            roarClient.canvasPanel.commands.update(pathName=argv[0], undoLevel=-1)
            roarClient.canvasPanel.commands._recentPush(argv[0])
            roarClient.canvasPanel.commands.canvasTool(roarClient.canvasPanel.commands.canvasTool, 1)(None)
        else:
            print("error: {}".format(error), file=sys.stderr)
    else:
        roarClient.canvasPanel.commands.canvasNew(None)
        roarClient.canvasPanel.commands.canvasTool(roarClient.canvasPanel.commands.canvasTool, 1)(None)
    wxApp.MainLoop()
if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
