#!/usr/bin/env python3
#
# RoarCanvasCommands.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiCanvasColours import Colours
from GuiFrame import NID_MENU_SEP, NID_TOOLBAR_HSEP
from RoarCanvasCommandsEdit import RoarCanvasCommandsEdit
from RoarCanvasCommandsFile import RoarCanvasCommandsFile
from RoarCanvasCommandsHelp import RoarCanvasCommandsHelp
from RoarCanvasCommandsOperators import RoarCanvasCommandsOperators
from RoarCanvasCommandsTools import RoarCanvasCommandsTools
from ToolObject import ToolObject
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

    def _initInterface(self):
        accels = ()
        menus = (
            ("&File",
                self.canvasNew, self.canvasOpen, self.canvasOpenRecent, self.canvasRestore, self.canvasSave, self.canvasSaveAs, NID_MENU_SEP,
                ("&Export...", self.canvasExportAsAnsi, self.canvasExportToClipboard, self.canvasExportImgur, self.canvasExportPastebin, self.canvasExportAsPng,),
                ("&Import...", self.canvasImportAnsi, self.canvasImportFromClipboard, self.canvasImportSauce,),
                NID_MENU_SEP,
                self.canvasExit,
            ),
            ("&Edit",
                self.canvasUndo, self.canvasRedo, NID_MENU_SEP,
                self.canvasCut, self.canvasCopy, self.canvasPaste,
                self.canvasDelete, NID_MENU_SEP,
                ("Brush size", self.canvasBrushSize(self.canvasBrushSize, 0, True), self.canvasBrushSize(self.canvasBrushSize, 0, False), self.canvasBrushSize(self.canvasBrushSize, 1, True), self.canvasBrushSize(self.canvasBrushSize, 1, False), NID_MENU_SEP,
                    self.canvasBrushSize(self.canvasBrushSize, 2, True), self.canvasBrushSize(self.canvasBrushSize, 2, False),),
                ("Canvas size", self.canvasCanvasSize(self.canvasCanvasSize, 1, True), self.canvasCanvasSize(self.canvasCanvasSize, 1, False), self.canvasCanvasSize(self.canvasCanvasSize, 0, True), self.canvasCanvasSize(self.canvasCanvasSize, 0, False), NID_MENU_SEP,
                    self.canvasCanvasSize(self.canvasCanvasSize, 2, True), self.canvasCanvasSize(self.canvasCanvasSize, 2, False),),
                self.canvasColoursFlip,
                NID_MENU_SEP,
                self.canvasBrush(self.canvasBrush, 0), NID_MENU_SEP,
                self.canvasAssetsWindowHide, self.canvasAssetsWindowShow,
            ),
            ("&Tools",
                self.canvasTool(self.canvasTool, 1), self.canvasTool(self.canvasTool, 7), self.canvasTool(self.canvasTool, 0), self.canvasTool(self.canvasTool, 3), self.canvasTool(self.canvasTool, 4), self.canvasTool(self.canvasTool, 8), self.canvasTool(self.canvasTool, 5), self.canvasTool(self.canvasTool, 2), self.canvasTool(self.canvasTool, 6),
            ),
            ("&Operators",
                self.canvasOperator(self.canvasOperator, 0), self.canvasOperator(self.canvasOperator, 1), self.canvasOperator(self.canvasOperator, 2), self.canvasOperator(self.canvasOperator, 3), self.canvasOperator(self.canvasOperator, 4),
            ),
            ("&Help",
                self.canvasMelp, NID_MENU_SEP, self.canvasNewIssueGitHub, self.canvasVisitGitHub, NID_MENU_SEP, self.canvasAbout,
            ),
        )
        toolBars = (
            (self.canvasNew, self.canvasOpen, self.canvasSave, self.canvasSaveAs, NID_TOOLBAR_HSEP,
             self.canvasUndo, self.canvasRedo, NID_TOOLBAR_HSEP,
             self.canvasCut, self.canvasCopy, self.canvasPaste, self.canvasDelete, NID_TOOLBAR_HSEP,
             self.canvasAssetsWindowHide, self.canvasAssetsWindowShow, NID_TOOLBAR_HSEP,
            ),
            (self.canvasTool(self.canvasTool, 1), self.canvasTool(self.canvasTool, 7), self.canvasTool(self.canvasTool, 0), self.canvasTool(self.canvasTool, 3), self.canvasTool(self.canvasTool, 4), self.canvasTool(self.canvasTool, 8), self.canvasTool(self.canvasTool, 5), self.canvasTool(self.canvasTool, 2), self.canvasTool(self.canvasTool, 6),),
            (self.canvasColour(self.canvasColour, 0), self.canvasColour(self.canvasColour, 1), self.canvasColour(self.canvasColour, 2), self.canvasColour(self.canvasColour, 3),
             self.canvasColour(self.canvasColour, 4), self.canvasColour(self.canvasColour, 5), self.canvasColour(self.canvasColour, 6), self.canvasColour(self.canvasColour, 7),
             self.canvasColour(self.canvasColour, 8), self.canvasColour(self.canvasColour, 9), self.canvasColour(self.canvasColour, 10), self.canvasColour(self.canvasColour, 11),
             self.canvasColour(self.canvasColour, 12), self.canvasColour(self.canvasColour, 13), self.canvasColour(self.canvasColour, 14), self.canvasColour(self.canvasColour, 15),
             self.canvasColourAlpha(self.canvasColourAlpha, 0), self.canvasColoursFlip, NID_TOOLBAR_HSEP,
             self.canvasBrushSize(self.canvasBrushSize, 1, True), self.canvasBrushSize(self.canvasBrushSize, 1, False), self.canvasBrushSize(self.canvasBrushSize, 0, True), self.canvasBrushSize(self.canvasBrushSize, 0, False), NID_TOOLBAR_HSEP,
             self.canvasBrushSize(self.canvasBrushSize, 2, True), self.canvasBrushSize(self.canvasBrushSize, 2, False),
            ),
            (self.canvasColourBackground(self.canvasColourBackground, 0), self.canvasColourBackground(self.canvasColourBackground, 1), self.canvasColourBackground(self.canvasColourBackground, 2), self.canvasColourBackground(self.canvasColourBackground, 3),
             self.canvasColourBackground(self.canvasColourBackground, 4), self.canvasColourBackground(self.canvasColourBackground, 5), self.canvasColourBackground(self.canvasColourBackground, 6), self.canvasColourBackground(self.canvasColourBackground, 7),
             self.canvasColourBackground(self.canvasColourBackground, 8), self.canvasColourBackground(self.canvasColourBackground, 9), self.canvasColourBackground(self.canvasColourBackground, 10), self.canvasColourBackground(self.canvasColourBackground, 11),
             self.canvasColourBackground(self.canvasColourBackground, 12), self.canvasColourBackground(self.canvasColourBackground, 13), self.canvasColourBackground(self.canvasColourBackground, 14), self.canvasColourBackground(self.canvasColourBackground, 15),
             self.canvasColourAlphaBackground(self.canvasColourAlphaBackground, 0), self.canvasColoursFlip, NID_TOOLBAR_HSEP,
             self.canvasCanvasSize(self.canvasCanvasSize, 1, True), self.canvasCanvasSize(self.canvasCanvasSize, 1, False), self.canvasCanvasSize(self.canvasCanvasSize, 0, True), self.canvasCanvasSize(self.canvasCanvasSize, 0, False), NID_TOOLBAR_HSEP,
             self.canvasCanvasSize(self.canvasCanvasSize, 2, True), self.canvasCanvasSize(self.canvasCanvasSize, 2, False),
            ),
        )
        return accels, menus, toolBars

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
                toolBar.ToggleTool(self.canvasColour(self.canvasColour, self.lastPanelState["colours"][0]).attrDict["id"], True); toolBar.Refresh()
            else:
                toolBar.ToggleTool(self.canvasColourAlpha(self.canvasColourAlpha, 0).attrDict["id"], True); toolBar.Refresh()
            if self.lastPanelState["colours"][1] != -1:
                toolBarBg.ToggleTool(self.canvasColourBackground(self.canvasColourBackground, self.lastPanelState["colours"][1]).attrDict["id"], True); toolBarBg.Refresh()
            else:
                toolBarBg.ToggleTool(self.canvasColourAlphaBackground(self.canvasColourAlphaBackground, 0).attrDict["id"], True); toolBarBg.Refresh()
        if "pathName" in self.lastPanelState:
            if self.lastPanelState["pathName"] != None:
                basePathName = os.path.basename(self.lastPanelState["pathName"])
                textItems.append("F: {}".format(basePathName))
                self.parentFrame.SetTitle("{} - roar".format(basePathName))
            else:
                self.parentFrame.SetTitle("roar")
        if "currentTool" in self.lastPanelState:
            self.parentFrame.menuItemsById[self.canvasTool.attrList[self.lastPanelState["currentToolIdx"]]["id"]].Check(True)
            toolBar = self.parentFrame.toolBarItemsById[self.canvasTool.attrList[self.lastPanelState["currentToolIdx"]]["id"]][0]
            toolBar.ToggleTool(self.canvasTool.attrList[self.lastPanelState["currentToolIdx"]]["id"], True); toolBar.Refresh();
            if (self.lastPanelState["currentTool"] != None) and (self.lastPanelState["currentTool"].__class__ == ToolObject):
                self.parentFrame.menuItemsById[self.canvasOperator.attrList[4]["id"]].Enable(True)
            else:
                self.parentFrame.menuItemsById[self.canvasOperator.attrList[4]["id"]].Enable(False)
            textItems.append("T: {}".format(self.lastPanelState["currentTool"].name if (self.lastPanelState["currentTool"] != None) else "Cursor"))
        if ("operator" in self.lastPanelState) and (self.lastPanelState["operator"] != None):
            textItems.append("O: {}".format(self.lastPanelState["operator"]))
        if ("dirty" in self.lastPanelState) and self.lastPanelState["dirty"]:
            textItems.append("*")
        if ("backupStatus" in self.lastPanelState) and (self.lastPanelState["backupStatus"] == True):
            textItems.append("Saving backup...")
        self.parentFrame.statusBar.SetStatusText(" | ".join(textItems))
        if "undoLevel" in self.lastPanelState:
            if  (self.lastPanelState["undoLevel"] >= 0) \
            and (self.lastPanelState["undoLevel"] < (len(self.parentCanvas.canvas.patchesUndo) - 1)):
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
        [classObject.__init__(self) for classObject in self.__class__.__bases__]
        self._initColourBitmaps(); self.accels, self.menus, self.toolBars = self._initInterface();
        self.canvasPathName, self.lastPanelState, self.parentCanvas, self.parentFrame = None, {}, parentCanvas, parentFrame

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
