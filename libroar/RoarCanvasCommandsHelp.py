#!/usr/bin/env python3
#
# RoarCanvasCommandsHelp.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiFrame import GuiCommandDecorator
from RoarWindowAbout import RoarWindowAbout
from RoarWindowMelp import RoarWindowMelp
import webbrowser, wx

class RoarCanvasCommandsHelp():
    @GuiCommandDecorator("About roar", "&About roar", None, None, True)
    def canvasAbout(self, event):
        RoarWindowAbout(self.parentFrame)

    @GuiCommandDecorator("View melp?", "View &melp?", None, [wx.MOD_NONE, wx.WXK_F1], True)
    def canvasMelp(self, event):
        RoarWindowMelp(self.parentFrame)

    @GuiCommandDecorator("Open &issue on GitHub", "Open &issue on GitHub", None, None, True)
    def canvasNewIssueGitHub(self, event):
        webbrowser.open("https://github.com/lalbornoz/roar/issues/new")

    @GuiCommandDecorator("Visit GitHub website", "Visit &GitHub website", None, None, True)
    def canvasVisitGitHub(self, event):
        webbrowser.open("https://www.github.com/lalbornoz/roar")

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
