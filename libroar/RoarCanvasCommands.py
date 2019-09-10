#!/usr/bin/env python3
#
# RoarCanvasCommands.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiCanvasColours import Colours
from GuiFrame import NID_TOOLBAR_HSEP
from RoarCanvasCommandsEdit import RoarCanvasCommandsEdit
from RoarCanvasCommandsFile import RoarCanvasCommandsFile
from RoarCanvasCommandsHelp import RoarCanvasCommandsHelp
from RoarCanvasCommandsTools import RoarCanvasCommandsTools
import os, wx

class RoarCanvasCommands(RoarCanvasCommandsFile, RoarCanvasCommandsEdit, RoarCanvasCommandsHelp, RoarCanvasCommandsTools):
    # {{{ _initColourBitmaps(self)
    def _initColourBitmaps(self):
        for numColour in range(len(RoarCanvasCommandsEdit.canvasColour.attrList)):
            if numColour < len(Colours):
                toolBitmapColour = Colours[numColour][0:4]
                toolBitmap = wx.Bitmap((16, 16))
                toolBitmapDc = wx.MemoryDC(); toolBitmapDc.SelectObject(toolBitmap);
                toolBitmapBrush = wx.Brush(wx.Colour(toolBitmapColour), wx.BRUSHSTYLE_SOLID)
                toolBitmapDc.SetBrush(toolBitmapBrush)
                toolBitmapDc.SetBackground(toolBitmapBrush)
                toolBitmapDc.SetPen(wx.Pen(wx.Colour(toolBitmapColour), 1))
                toolBitmapDc.DrawRectangle(0, 0, 16, 16)
            RoarCanvasCommandsEdit.canvasColour.attrList[numColour]["icon"] = ["", None, toolBitmap]
        toolBitmapColours = ((0, 0, 0, 255), (255, 255, 255, 255))
        toolBitmap = wx.Bitmap((16, 16))
        toolBitmapDc = wx.MemoryDC(); toolBitmapDc.SelectObject(toolBitmap);
        toolBitmapBrush = [wx.Brush(wx.Colour(c), wx.BRUSHSTYLE_SOLID) for c in toolBitmapColours]
        toolBitmapDc.SetBrush(toolBitmapBrush[1])
        toolBitmapDc.SetBackground(toolBitmapBrush[1])
        toolBitmapDc.SetPen(wx.Pen(wx.Colour(toolBitmapColours[1]), 1))
        toolBitmapDc.DrawRectangle(0, 0, 8, 8)
        toolBitmapDc.DrawRectangle(8, 8, 16, 16)
        RoarCanvasCommandsEdit.canvasColourAlpha.attrList[0]["icon"] = ["", None, toolBitmap]
    # }}}

    # {{{ update(self, **kwargs)
    def update(self, **kwargs):
        self.lastPanelState.update(kwargs); textItems = [];
        if "cellPos" in self.lastPanelState:
            textItems.append("X: {:03d} Y: {:03d}".format(*self.lastPanelState["cellPos"]))
        if "size" in self.lastPanelState:
            textItems.append("W: {:03d} H: {:03d}".format(*self.lastPanelState["size"]))
        if "brushSize" in self.lastPanelState:
            textItems.append("Brush: {:02d}x{:02d}".format(*self.lastPanelState["brushSize"]))
        if "colours" in self.lastPanelState:
            textItems.append("FG: {:02d}, BG: {:02d}".format(*self.lastPanelState["colours"]))
            textItems.append("{} on {}".format(
                Colours[self.lastPanelState["colours"][0]][4] if self.lastPanelState["colours"][0] != -1 else "Transparent",
                Colours[self.lastPanelState["colours"][1]][4] if self.lastPanelState["colours"][1] != -1 else "Transparent"))
        if "pathName" in self.lastPanelState:
            if self.lastPanelState["pathName"] != None:
                basePathName = os.path.basename(self.lastPanelState["pathName"])
                textItems.append("Current file: {}".format(basePathName))
                self.parentFrame.SetTitle("{} - roar".format(basePathName))
            else:
                self.parentFrame.SetTitle("roar")
        if "toolName" in self.lastPanelState:
            textItems.append("Current tool: {}".format(self.lastPanelState["toolName"]))
        if  "dirty" in self.lastPanelState  \
        and self.lastPanelState["dirty"]:
            textItems.append("*")
        self.parentFrame.statusBar.SetStatusText(" | ".join(textItems))
        if "undoLevel" in self.lastPanelState:
            if self.lastPanelState["undoLevel"] >= 0:
                self.parentFrame.menuItemsById[self.canvasUndo.attrDict["id"]].Enable(True)
                toolBar = self.parentFrame.toolBarItemsById[self.canvasUndo.attrDict["id"]].GetToolBar()
                toolBar.EnableTool(self.canvasUndo.attrDict["id"], True)
            else:
                self.parentFrame.menuItemsById[self.canvasUndo.attrDict["id"]].Enable(False)
                toolBar = self.parentFrame.toolBarItemsById[self.canvasUndo.attrDict["id"]].GetToolBar()
                toolBar.EnableTool(self.canvasUndo.attrDict["id"], False)
            if self.lastPanelState["undoLevel"] > 0:
                self.parentFrame.menuItemsById[self.canvasRedo.attrDict["id"]].Enable(True)
                toolBar = self.parentFrame.toolBarItemsById[self.canvasRedo.attrDict["id"]].GetToolBar()
                toolBar.EnableTool(self.canvasRedo.attrDict["id"], True)
            else:
                self.parentFrame.menuItemsById[self.canvasRedo.attrDict["id"]].Enable(False)
                toolBar = self.parentFrame.toolBarItemsById[self.canvasRedo.attrDict["id"]].GetToolBar()
                toolBar.EnableTool(self.canvasRedo.attrDict["id"], False)
    # }}}

    #
    # __init__(self, parentCanvas, parentFrame):
    def __init__(self, parentCanvas, parentFrame):
        menus, toolBars = [], []
        self.canvasPathName, self.lastPanelState, self.parentCanvas, self.parentFrame = None, {}, parentCanvas, parentFrame
        for classObject in self.__class__.__bases__:
            classObject.__init__(self)
            if len(self.menus):
                menus += self.menus
            if len(self.toolBars):
                toolBars += self.toolBars
        self._initColourBitmaps()

        # XXX
        toolBars.append(
            [self.canvasNew, self.canvasOpen, self.canvasSave, self.canvasSaveAs, NID_TOOLBAR_HSEP,
             self.canvasUndo, self.canvasRedo, NID_TOOLBAR_HSEP,
             self.canvasCut, self.canvasCopy, self.canvasPaste, self.canvasDelete, NID_TOOLBAR_HSEP,
             self.canvasCanvasSize(self.canvasCanvasSize, 1, True), self.canvasCanvasSize(self.canvasCanvasSize, 1, False), self.canvasCanvasSize(self.canvasCanvasSize, 0, True), self.canvasCanvasSize(self.canvasCanvasSize, 0, False), NID_TOOLBAR_HSEP,
             self.canvasCanvasSize(self.canvasCanvasSize, 2, True), self.canvasCanvasSize(self.canvasCanvasSize, 2, False), NID_TOOLBAR_HSEP,
             self.canvasTool(self.canvasTool, 5), self.canvasTool(self.canvasTool, 0), self.canvasTool(self.canvasTool, 2), self.canvasTool(self.canvasTool, 3), self.canvasTool(self.canvasTool, 6), self.canvasTool(self.canvasTool, 1), self.canvasTool(self.canvasTool, 4),
            ])
        # XXX
        toolBars.append(
            [self.canvasColour(self.canvasColour, 0), self.canvasColour(self.canvasColour, 1), self.canvasColour(self.canvasColour, 2), self.canvasColour(self.canvasColour, 3),
             self.canvasColour(self.canvasColour, 4), self.canvasColour(self.canvasColour, 5), self.canvasColour(self.canvasColour, 6), self.canvasColour(self.canvasColour, 7),
             self.canvasColour(self.canvasColour, 8), self.canvasColour(self.canvasColour, 9), self.canvasColour(self.canvasColour, 10), self.canvasColour(self.canvasColour, 11),
             self.canvasColour(self.canvasColour, 12), self.canvasColour(self.canvasColour, 13), self.canvasColour(self.canvasColour, 14), self.canvasColour(self.canvasColour, 15),
             self.canvasColourAlpha(self.canvasColourAlpha, 0), NID_TOOLBAR_HSEP,
             self.canvasBrushSize(self.canvasBrushSize, 1, True), self.canvasBrushSize(self.canvasBrushSize, 0, False), self.canvasBrushSize(self.canvasBrushSize, 1, True), self.canvasBrushSize(self.canvasBrushSize, 1, False), NID_TOOLBAR_HSEP,
             self.canvasBrushSize(self.canvasBrushSize, 2, True), self.canvasBrushSize(self.canvasBrushSize, 2, False),
            ])
        self.menus, self.toolBars = menus, toolBars

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
