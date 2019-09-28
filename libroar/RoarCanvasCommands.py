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
from RoarCanvasCommandsOperators import RoarCanvasCommandsOperators
from RoarCanvasCommandsTools import RoarCanvasCommandsTools
import os, wx

class RoarCanvasCommands(RoarCanvasCommandsFile, RoarCanvasCommandsEdit, RoarCanvasCommandsTools, RoarCanvasCommandsOperators, RoarCanvasCommandsHelp):
    def _initColourBitmaps(self):
        def _initColourBitmaps_(cmd, cmdAlpha, div):
            for numColour in range(len(cmd.attrList)):
                if numColour < len(Colours):
                    toolBitmapColour = Colours[numColour][0:4]
                    toolBitmap = wx.Bitmap((16, 16))
                    toolBitmapDc = wx.MemoryDC(); toolBitmapDc.SelectObject(toolBitmap);
                    toolBitmapBrush = wx.Brush(wx.Colour([*[int(c / div) for c in toolBitmapColour[:3]], 255]), wx.BRUSHSTYLE_SOLID)
                    toolBitmapDc.SetBrush(toolBitmapBrush)
                    toolBitmapDc.SetBackground(toolBitmapBrush)
                    toolBitmapDc.SetPen(wx.Pen(toolBitmapColour, 1))
                    toolBitmapDc.DrawRectangle(0, 0, 16, 16)
                cmd.attrList[numColour]["icon"] = ["", None, toolBitmap]
            toolBitmapColours = ((0, 0, 0, 255), (255, 255, 255, 255))
            toolBitmap = wx.Bitmap((16, 16))
            toolBitmapDc = wx.MemoryDC(); toolBitmapDc.SelectObject(toolBitmap);
            toolBitmapBrush = [wx.Brush(wx.Colour(c), wx.BRUSHSTYLE_SOLID) for c in toolBitmapColours]
            toolBitmapDc.SetBrush(toolBitmapBrush[1])
            toolBitmapDc.SetBackground(toolBitmapBrush[1])
            toolBitmapDc.SetPen(wx.Pen(wx.Colour(toolBitmapColours[1]), 1))
            toolBitmapDc.DrawRectangle(0, 0, 8, 8)
            toolBitmapDc.DrawRectangle(8, 8, 16, 16)
            cmdAlpha.attrList[0]["icon"] = ["", None, toolBitmap]
        _initColourBitmaps_(RoarCanvasCommandsEdit.canvasColour, RoarCanvasCommandsEdit.canvasColourAlpha, 1.0)
        _initColourBitmaps_(RoarCanvasCommandsEdit.canvasColourBackground, RoarCanvasCommandsEdit.canvasColourAlphaBackground, 1.5)

    def update(self, **kwargs):
        self.lastPanelState.update(kwargs); textItems = [];
        if "cellPos" in self.lastPanelState:
            textItems.append("X: {:03d} Y: {:03d}".format(*self.lastPanelState["cellPos"]))
        if "size" in self.lastPanelState:
            textItems.append("W: {:03d} H: {:03d}".format(*self.lastPanelState["size"]))
        if "brushSize" in self.lastPanelState:
            textItems.append("B: {:02d}x{:02d}".format(*self.lastPanelState["brushSize"]))
        if "colours" in self.lastPanelState:
            textItems.append("FG: {:02d} ({}), BG: {:02d} ({})".format(self.lastPanelState["colours"][0], Colours[self.lastPanelState["colours"][0]][4] if self.lastPanelState["colours"][0] != -1 else "Transparent", self.lastPanelState["colours"][1], Colours[self.lastPanelState["colours"][1]][4] if self.lastPanelState["colours"][1] != -1 else "Transparent"))
            toolBar = self.parentFrame.toolBarItemsById[self.canvasColour(self.canvasColour, self.lastPanelState["colours"][0]).attrDict["id"]][0]
            toolBarBg = self.parentFrame.toolBarItemsById[self.canvasColourBackground(self.canvasColourBackground, self.lastPanelState["colours"][1]).attrDict["id"]][0]
            if self.lastPanelState["colours"][0] != -1:
                toolBar.ToggleTool(self.canvasColour(self.canvasColour, self.lastPanelState["colours"][0]).attrDict["id"], True)
                toolBar.Refresh()
            else:
                toolBar.ToggleTool(self.canvasColourAlpha(self.canvasColourAlpha, 0).attrDict["id"], True)
                toolBar.Refresh()
            if self.lastPanelState["colours"][1] != -1:
                toolBarBg.ToggleTool(self.canvasColourBackground(self.canvasColourBackground, self.lastPanelState["colours"][1]).attrDict["id"], True)
                toolBarBg.Refresh()
            else:
                toolBarBg.ToggleTool(self.canvasColourAlphaBackground(self.canvasColourAlphaBackground, 0).attrDict["id"], True)
                toolBarBg.Refresh()
        if "pathName" in self.lastPanelState:
            if self.lastPanelState["pathName"] != None:
                basePathName = os.path.basename(self.lastPanelState["pathName"])
                textItems.append("F: {}".format(basePathName))
                self.parentFrame.SetTitle("{} - roar".format(basePathName))
            else:
                self.parentFrame.SetTitle("roar")
        if "toolName" in self.lastPanelState:
            textItems.append("T: {}".format(self.lastPanelState["toolName"]))
        if  ("operator" in self.lastPanelState)         \
        and (self.lastPanelState["operator"] != None):
            textItems.append("O: {}".format(self.lastPanelState["operator"]))
        if  "dirty" in self.lastPanelState              \
        and self.lastPanelState["dirty"]:
            textItems.append("*")
        if  "backupStatus" in self.lastPanelState        \
        and self.lastPanelState["backupStatus"] == True:
            textItems.append("Saving backup...")
        self.parentFrame.statusBar.SetStatusText(" | ".join(textItems))
        if  ("undoInhibit" in self.lastPanelState)      \
        and (self.lastPanelState["undoInhibit"]):
            for item in (self.canvasRedo, self.canvasUndo):
                self.parentFrame.menuItemsById[item.attrDict["id"]].Enable(False)
                toolBar = self.parentFrame.toolBarItemsById[item.attrDict["id"]][0]
                toolBar.EnableTool(item.attrDict["id"], False); toolBar.Refresh();
        elif "undoLevel" in self.lastPanelState:
            if  (self.lastPanelState["undoLevel"] >= 0) \
            and (self.lastPanelState["undoLevel"] < (len(self.parentCanvas.canvas.journal.patchesUndo) - 1)):
                self.parentFrame.menuItemsById[self.canvasUndo.attrDict["id"]].Enable(True)
                toolBar = self.parentFrame.toolBarItemsById[self.canvasUndo.attrDict["id"]][0]
                toolBar.EnableTool(self.canvasUndo.attrDict["id"], True); toolBar.Refresh();
            else:
                self.parentFrame.menuItemsById[self.canvasUndo.attrDict["id"]].Enable(False)
                toolBar = self.parentFrame.toolBarItemsById[self.canvasUndo.attrDict["id"]][0]
                toolBar.EnableTool(self.canvasUndo.attrDict["id"], False); toolBar.Refresh();
            if self.lastPanelState["undoLevel"] > 0:
                self.parentFrame.menuItemsById[self.canvasRedo.attrDict["id"]].Enable(True)
                toolBar = self.parentFrame.toolBarItemsById[self.canvasRedo.attrDict["id"]][0]
                toolBar.EnableTool(self.canvasRedo.attrDict["id"], True); toolBar.Refresh();
            else:
                self.parentFrame.menuItemsById[self.canvasRedo.attrDict["id"]].Enable(False)
                toolBar = self.parentFrame.toolBarItemsById[self.canvasRedo.attrDict["id"]][0]
                toolBar.EnableTool(self.canvasRedo.attrDict["id"], False); toolBar.Refresh();

    def __init__(self, parentCanvas, parentFrame):
        accels, menus, toolBars = [], [], []
        self.canvasPathName, self.lastPanelState, self.parentCanvas, self.parentFrame = None, {}, parentCanvas, parentFrame
        for classObject in self.__class__.__bases__:
            classObject.__init__(self)
            if len(self.accels):
                accels += self.accels
            if len(self.menus):
                menus += self.menus
            if len(self.toolBars):
                toolBars += self.toolBars
        self._initColourBitmaps()

        toolBars.append(
            [self.canvasNew, self.canvasOpen, self.canvasSave, self.canvasSaveAs, NID_TOOLBAR_HSEP,
             self.canvasUndo, self.canvasRedo, NID_TOOLBAR_HSEP,
             self.canvasCut, self.canvasCopy, self.canvasPaste, self.canvasDelete, NID_TOOLBAR_HSEP,
             self.canvasAssetsWindowHide, self.canvasAssetsWindowShow, NID_TOOLBAR_HSEP,
            ])
        toolBars.append(
            [self.canvasTool(self.canvasTool, 1), self.canvasTool(self.canvasTool, 7), self.canvasTool(self.canvasTool, 0), self.canvasTool(self.canvasTool, 3), self.canvasTool(self.canvasTool, 4), self.canvasTool(self.canvasTool, 8), self.canvasTool(self.canvasTool, 5), self.canvasTool(self.canvasTool, 2), self.canvasTool(self.canvasTool, 6),
            ])
        toolBars.append(
            [self.canvasColour(self.canvasColour, 0), self.canvasColour(self.canvasColour, 1), self.canvasColour(self.canvasColour, 2), self.canvasColour(self.canvasColour, 3),
             self.canvasColour(self.canvasColour, 4), self.canvasColour(self.canvasColour, 5), self.canvasColour(self.canvasColour, 6), self.canvasColour(self.canvasColour, 7),
             self.canvasColour(self.canvasColour, 8), self.canvasColour(self.canvasColour, 9), self.canvasColour(self.canvasColour, 10), self.canvasColour(self.canvasColour, 11),
             self.canvasColour(self.canvasColour, 12), self.canvasColour(self.canvasColour, 13), self.canvasColour(self.canvasColour, 14), self.canvasColour(self.canvasColour, 15),
             self.canvasColourAlpha(self.canvasColourAlpha, 0), self.canvasColoursFlip, NID_TOOLBAR_HSEP,
             self.canvasBrushSize(self.canvasBrushSize, 1, True), self.canvasBrushSize(self.canvasBrushSize, 1, False), self.canvasBrushSize(self.canvasBrushSize, 0, True), self.canvasBrushSize(self.canvasBrushSize, 0, False), NID_TOOLBAR_HSEP,
             self.canvasBrushSize(self.canvasBrushSize, 2, True), self.canvasBrushSize(self.canvasBrushSize, 2, False),
            ])
        toolBars.append(
            [self.canvasColourBackground(self.canvasColourBackground, 0), self.canvasColourBackground(self.canvasColourBackground, 1), self.canvasColourBackground(self.canvasColourBackground, 2), self.canvasColourBackground(self.canvasColourBackground, 3),
             self.canvasColourBackground(self.canvasColourBackground, 4), self.canvasColourBackground(self.canvasColourBackground, 5), self.canvasColourBackground(self.canvasColourBackground, 6), self.canvasColourBackground(self.canvasColourBackground, 7),
             self.canvasColourBackground(self.canvasColourBackground, 8), self.canvasColourBackground(self.canvasColourBackground, 9), self.canvasColourBackground(self.canvasColourBackground, 10), self.canvasColourBackground(self.canvasColourBackground, 11),
             self.canvasColourBackground(self.canvasColourBackground, 12), self.canvasColourBackground(self.canvasColourBackground, 13), self.canvasColourBackground(self.canvasColourBackground, 14), self.canvasColourBackground(self.canvasColourBackground, 15),
             self.canvasColourAlphaBackground(self.canvasColourAlphaBackground, 0), self.canvasColoursFlip, NID_TOOLBAR_HSEP,
             self.canvasCanvasSize(self.canvasCanvasSize, 1, True), self.canvasCanvasSize(self.canvasCanvasSize, 1, False), self.canvasCanvasSize(self.canvasCanvasSize, 0, True), self.canvasCanvasSize(self.canvasCanvasSize, 0, False), NID_TOOLBAR_HSEP,
             self.canvasCanvasSize(self.canvasCanvasSize, 2, True), self.canvasCanvasSize(self.canvasCanvasSize, 2, False),
            ])
        self.accels, self.menus, self.toolBars = accels, menus, toolBars

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
