#!/usr/bin/env python3
#
# RoarCanvasCommandsHelp.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiFrame import GuiCommandDecorator, NID_MENU_SEP
from RoarWindowAbout import RoarWindowAbout
from RoarWindowMelp import RoarWindowMelp
import webbrowser

class RoarCanvasCommandsHelp():
    @GuiCommandDecorator("About roar", "&About roar", None, None, True)
    def canvasAbout(self, event):
        RoarWindowAbout(self.parentFrame)

    @GuiCommandDecorator("View melp?", "View &melp?", None, None, True)
    def canvasMelp(self, event):
        RoarWindowMelp(self.parentFrame)

    @GuiCommandDecorator("Open &issue on GitHub", "Open &issue on GitHub", None, None, True)
    def canvasNewIssueGitHub(self, event):
        webbrowser.open("https://github.com/lalbornoz/roar/issues/new")

    @GuiCommandDecorator("Visit GitHub website", "Visit &GitHub website", None, None, True)
    def canvasVisitGitHub(self, event):
        webbrowser.open("https://www.github.com/lalbornoz/roar")

    #
    # __init__(self)
    def __init__(self):
        self.accels = ()
        self.menus, self.toolBars = (("&Help", self.canvasMelp, NID_MENU_SEP, self.canvasNewIssueGitHub, self.canvasVisitGitHub, NID_MENU_SEP, self.canvasAbout,),), ()

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
