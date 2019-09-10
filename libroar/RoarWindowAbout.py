#!/usr/bin/env python3
#
# RoarWindowAbout.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from glob import glob
import os, random, wx, wx.adv

class RoarWindowAbout(wx.Dialog):
    # {{{ onButtonRoar(self, event)
    def onButtonRoar(self, event):
        self.Destroy()
    # }}}

    #
    # __init__(self, parent, size=(320, 240), title="About roar")
    def __init__(self, parent, size=(320, 240), title="About roar"):
        super().__init__(parent, size=size, title=title)
        self.panel, self.sizer, self.sizerH1, self.sizerH2 = wx.Panel(self), wx.BoxSizer(wx.VERTICAL), wx.BoxSizer(wx.HORIZONTAL), wx.BoxSizer(wx.HORIZONTAL)

        logoPathNames = glob(os.path.join("assets", "images", "logo*.bmp"))
        logoPathName = logoPathNames[random.randint(0, len(logoPathNames) - 1)]
        self.logo = wx.StaticBitmap(self, -1, wx.Bitmap(logoPathName))
        self.sizerH1.Add(self.logo, 0, wx.CENTER)

        self.title = wx.StaticText(self.panel, label="roar -- mIRC art editor for Windows && Linux\nGit revision __ROAR_RELEASE_GIT_SHORT_REV__\nhttps://www.github.com/lalbornoz/roar/\nCopyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>", style=wx.ALIGN_CENTER)
        self.title.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=False))
        self.sizer.Add(self.title)

        labelsText = ["roar!", "ROAR!", "roaaaaaaar!", "ROAROARAOR", "_ROAR_"]
        labelText = labelsText[random.randint(0, len(labelsText) - 1)]
        self.buttonRoar = wx.Button(self.panel, label=labelText, pos=(75, 10))
        self.buttonRoar.Bind(wx.EVT_BUTTON, self.onButtonRoar)
        self.sizerH2.Add(self.buttonRoar, 0, wx.CENTER)

        self.sizer.Add(self.sizerH1, 0, wx.CENTER)
        self.sizer.Add(self.sizerH2, 0, wx.CENTER)
        self.SetSizer(self.sizer); self.sizer.Fit(self.panel);
        self.SetSize(size); self.SetTitle(title); self.Center();

        soundBitePathNames = glob(os.path.join("assets", "audio", "roar*.wav"))
        soundBitePathName = soundBitePathNames[random.randint(0, len(logoPathNames) - 1)]
        self.soundBite = wx.adv.Sound(soundBitePathName)
        if self.soundBite.IsOk():
            self.soundBite.Play(wx.adv.SOUND_ASYNC)

        self.ShowModal()

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
