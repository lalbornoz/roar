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
    # __init__(self, parent, minSize=(320, 300), title="About roar")
    def __init__(self, parent, minSize=(320, 300), title="About roar"):
        super().__init__(parent, size=minSize, title=title)
        self.panel, self.sizer, self.sizerH = wx.Panel(self), wx.BoxSizer(wx.VERTICAL), [wx.BoxSizer(wx.HORIZONTAL), wx.BoxSizer(wx.HORIZONTAL), wx.BoxSizer(wx.HORIZONTAL)]

        logoPathNames = glob(os.path.join("assets", "images", "logo*.bmp"))
        logoPathName = logoPathNames[random.randint(0, len(logoPathNames) - 1)]
        self.logo = wx.StaticBitmap(self.panel, -1, wx.Bitmap(logoPathName))
        self.sizerH[0].Add(self.logo, 0, wx.ALL | wx.CENTER, 4)

        self.title = wx.StaticText(self.panel, label="roar -- mIRC art editor for Windows && Linux\nGit revision __ROAR_RELEASE_GIT_SHORT_REV__\nhttps://www.github.com/lalbornoz/roar/\nCopyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>", style=wx.ALIGN_CENTER)
        self.title.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=False))
        self.sizerH[1].Add(self.title, 0, wx.ALL | wx.CENTER, 3)

        labelsText = ["&roar!", "&ROAR!", "&roaaaaaaar!", "&ROAROARAOR", "_&ROAR_"]
        labelText = labelsText[random.randint(0, len(labelsText) - 1)]
        self.buttonRoar = wx.Button(self.panel, label=labelText)
        self.buttonRoar.Bind(wx.EVT_BUTTON, self.onButtonRoar)
        self.sizerH[2].Add(self.buttonRoar, 0, wx.ALL | wx.CENTER, 2)

        [self.sizer.Add(sizer, 0, wx.CENTER) for sizer in self.sizerH]
        self.panel.SetSizerAndFit(self.sizer)
        self.SetClientSize(self.sizer.ComputeFittingClientSize(self)); self.Center();
        self.SetTitle(title)

        soundBitePathNames = glob(os.path.join("assets", "audio", "roar*.wav"))
        soundBitePathName = soundBitePathNames[random.randint(0, len(logoPathNames) - 1)]
        self.soundBite = wx.adv.Sound(soundBitePathName)
        if self.soundBite.IsOk():
            self.soundBite.Play(wx.adv.SOUND_ASYNC)
        self.ShowModal()

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
