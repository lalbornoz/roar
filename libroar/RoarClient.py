#!/usr/bin/env python3
#
# RoarClient.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Canvas import Canvas
from GuiCanvasWxBackend import GuiCanvasWxBackend
from GuiFrame import GuiFrame, NID_TOOLBAR_HSEP
from RoarAssetsWindow import RoarAssetsWindow
from RoarCanvasCommands import RoarCanvasCommands
from RoarCanvasWindow import RoarCanvasWindow

from glob import glob
import os, random, sys, wx

class RoarClient(GuiFrame):
    def _getIconPathName(self):
        iconPathNames = glob(os.path.join("assets", "images", "logo*.bmp"))
        return iconPathNames[random.randint(0, len(iconPathNames) - 1)]

    def _initToolBitmaps(self, toolBars):
        basePathName = os.path.join(os.path.dirname(sys.argv[0]), "assets", "images")
        for toolBar in toolBars:
            for toolBarItem in [i for i in toolBar if i != NID_TOOLBAR_HSEP]:
                toolBarItem.attrDict["icon"] = self.loadBitmap(basePathName, toolBarItem.attrDict["icon"])

    def onChar(self, event):
        self.canvasPanel.onKeyboardInput(event)

    def onMouseWheel(self, event):
        self.canvasPanel.GetEventHandler().ProcessEvent(event)

    def onClose(self, event):
        if not self.canvasPanel.commands.exiting:
            closeFlag = self.canvasPanel.commands._promptSaveChanges()
        else:
            closeFlag = True
        if closeFlag:
            event.Skip();

    def onSize(self, event):
        self.canvasPanel.SetMinSize(self.GetSize()); self.canvasPanel.SetSize(wx.DefaultCoord, wx.DefaultCoord, *self.GetSize()); event.Skip();

    def __init__(self, parent, defaultCanvasPos=(0, 75), defaultCanvasSize=(100, 30), defaultCellSize=(7, 14), size=(840, 640), title=""):
        super().__init__(self._getIconPathName(), size, parent, title)
        self.canvas = Canvas(defaultCanvasSize)
        self.canvasPanel = RoarCanvasWindow(GuiCanvasWxBackend, self.canvas, defaultCellSize, RoarCanvasCommands, self.panelSkin, self, defaultCanvasPos, defaultCellSize, defaultCanvasSize)
        self.loadAccels(self.canvasPanel.commands.accels, self.canvasPanel.commands.menus, self.canvasPanel.commands.toolBars)
        self.loadMenus(self.canvasPanel.commands.menus)
        self._initToolBitmaps(self.canvasPanel.commands.toolBars)
        self.loadToolBars(self.canvasPanel.commands.toolBars)

        self.canvasPanel.commands.canvasNew(None)
        self.canvasPanel.commands.canvasTool(self.canvasPanel.commands.canvasTool, 1)(None)
        self.canvasPanel.commands.update(brushSize=self.canvasPanel.brushSize, colours=self.canvasPanel.brushColours)
        self.addWindow(self.canvasPanel, expand=True)
        self.assetsWindow = RoarAssetsWindow(GuiCanvasWxBackend, defaultCellSize, self)
        self.canvasPanel.commands.canvasAssetsWindowShow(None)

        self.canvasPanel.operatorsMenu = wx.Menu()
        for menuItem in self.canvasPanel.commands.menus[3][1:]:
            menuItemWindow = self.canvasPanel.operatorsMenu.Append(menuItem.attrDict["id"], menuItem.attrDict["label"], menuItem.attrDict["caption"])
            self.Bind(wx.EVT_MENU, self.onMenu, menuItemWindow)
        self.canvasPanel.commands.canvasOpenRecent.attrDict["menu"].AppendSeparator()
        self.canvasPanel.commands.canvasClearRecent.attrDict["id"] = wx.NewId()
        menuItemWindow = self.canvasPanel.commands.canvasOpenRecent.attrDict["menu"].Append(self.canvasPanel.commands.canvasClearRecent.attrDict["id"], self.canvasPanel.commands.canvasClearRecent.attrDict["label"], self.canvasPanel.commands.canvasClearRecent.attrDict["caption"])
        self.canvasPanel.commands.canvasOpenRecent.attrDict["menu"].Bind(wx.EVT_MENU, self.canvasPanel.commands.canvasClearRecent, menuItemWindow)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_SIZE, self.onSize)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
