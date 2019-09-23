#!/usr/bin/env python3
#
# RoarCanvasCommandsHelp.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiFrame import GuiCommandDecorator
from RoarWindowAbout import RoarWindowAbout

class RoarCanvasCommandsHelp():
    @GuiCommandDecorator("About", "&About", None, None, True)
    def canvasAbout(self, event):
        RoarWindowAbout(self.parentFrame)

    #
    # __init__(self)
    def __init__(self):
        self.accels = ()
        self.menus, self.toolBars = (("&Help", self.canvasAbout,),), ()

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
