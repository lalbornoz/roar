#!/usr/bin/env python3
#
# RoarWindowMelp.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import os, wx

class RoarWindowMelp(wx.Dialog):
    def onButtonRoar(self, event):
        self.Destroy()

    def __init__(self, parent, minSize=(320, 300), title="melp?"):
        super().__init__(parent, size=minSize, title=title)
        self.panel, self.sizer = wx.Panel(self), wx.BoxSizer(wx.VERTICAL)

        with open(os.path.join("assets", "text", "melp.txt"), "r") as fileObject:
            helpLabel = "".join(fileObject.readlines())
        self.title = wx.StaticText(self.panel, label=helpLabel, style=wx.ALIGN_LEFT)
        self.title.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL, underline=False))
        self.buttonRoar = wx.Button(self.panel, label="&explodes.")
        self.buttonRoar.Bind(wx.EVT_BUTTON, self.onButtonRoar)
        self.sizer.AddMany(((self.title, 1, wx.ALL | wx.CENTER | wx.EXPAND, 4), (self.buttonRoar, 0, wx.ALL | wx.CENTER, 4),))
        self.panel.SetSizerAndFit(self.sizer)
        newSize = self.sizer.ComputeFittingWindowSize(self)
        self.SetSize((newSize[0] + 64, newSize[1],)); self.Center();
        self.SetTitle(title)

        self.ShowModal()

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
