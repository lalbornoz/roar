#!/usr/bin/env python3
#
# RoarWindowAbout.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from glob import glob
import os, random, wx, wx.adv

class RoarWindowAbout(wx.Dialog):
    def onButtonRoar(self, event):
        self.Destroy()

    def __init__(self, parent, minSize=(320, 300), title="About roar"):
        super().__init__(parent, size=minSize, title=title)
        self.panel, self.sizer, self.sizerV = wx.Panel(self), wx.FlexGridSizer(2, 2, 4, 4), wx.BoxSizer(wx.VERTICAL)
        self.panel.SetBackgroundColour(wx.Colour(0, 0, 0)); self.panel.SetForegroundColour(wx.Colour(0, 187, 0));

        logoPathNames = glob(os.path.join("assets", "images", "logo*.bmp"))
        logoPathName = logoPathNames[random.randint(0, len(logoPathNames) - 1)]
        self.logo = wx.StaticBitmap(self.panel, -1, wx.Bitmap(logoPathName))

        self.title = wx.StaticText(self.panel, label="roar -- mIRC art editor for Windows && Linux\n__ROAR_RELEASE_VERSION__\nhttps://www.github.com/lalbornoz/roar/\nCopyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>\nhttps://www.lucioillanes.de\n", style=wx.ALIGN_CENTER)
        self.title.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=False))
        labelsText = ["&roar!", "&ROAR!", "&roaaaaaaar!", "&ROAROARAOR", "_&ROAR_"]
        labelText = labelsText[random.randint(0, len(labelsText) - 1)]
        self.buttonRoar = wx.Button(self.panel, label=labelText)
        self.buttonRoar.Bind(wx.EVT_BUTTON, self.onButtonRoar)
        self.sizerV.AddMany(((self.title, 0, wx.ALL | wx.CENTER, 4), (self.buttonRoar, 0, wx.ALL | wx.CENTER, 4),))

        self.sizer.AddMany((
            (self.logo, 0, wx.ALL | wx.CENTER, 4),
            (self.sizerV, 0, wx.ALL | wx.CENTER, 3),))
        self.panel.SetSizerAndFit(self.sizer)
        self.SetClientSize(self.sizer.ComputeFittingClientSize(self)); self.Center();
        self.SetTitle(title)

        soundBitePathNames = glob(os.path.join("assets", "audio", "roar*.wav"))
        soundBitePathName = soundBitePathNames[random.randint(0, len(soundBitePathNames) - 1)]
        self.soundBite = wx.adv.Sound(soundBitePathName)
        if self.soundBite.IsOk():
            self.soundBite.Play(wx.adv.SOUND_ASYNC)
        self.ShowModal()

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
