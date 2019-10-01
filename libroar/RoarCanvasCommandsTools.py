#!/usr/bin/env python3
#
# RoarCanvasCommandsTools.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiFrame import GuiSelectDecorator
from ToolCircle import ToolCircle
from ToolErase import ToolErase
from ToolFill import ToolFill
from ToolLine import ToolLine
from ToolObject import ToolObject
from ToolPickColour import ToolPickColour
from ToolRect import ToolRect
from ToolText import ToolText
import wx

class RoarCanvasCommandsTools():
    @GuiSelectDecorator(0, "Circle", "&Circle", ["toolCircle.png"], [wx.MOD_NONE, wx.WXK_F4], False)
    @GuiSelectDecorator(1, "Cursor", "C&ursor", ["toolCursor.png"], [wx.MOD_NONE, wx.WXK_F2], False)
    @GuiSelectDecorator(2, "Erase", "&Erase", ["toolErase.png"], [wx.MOD_NONE, wx.WXK_F9], False)
    @GuiSelectDecorator(3, "Fill", "&Fill", ["toolFill.png"], [wx.MOD_NONE, wx.WXK_F5], False)
    @GuiSelectDecorator(4, "Line", "&Line", ["toolLine.png"], [wx.MOD_NONE, wx.WXK_F6], False)
    @GuiSelectDecorator(5, "Object", "&Object", ["toolObject.png"], [wx.MOD_NONE, wx.WXK_F8], False)
    @GuiSelectDecorator(6, "Pick colour", "&Pick colour", ["toolPickColour.png"], [wx.MOD_NONE, wx.WXK_F10], False)
    @GuiSelectDecorator(7, "Rectangle", "&Rectangle", ["toolRect.png"], [wx.MOD_NONE, wx.WXK_F3], True)
    @GuiSelectDecorator(8, "Text", "&Text", ["toolText.png"], [wx.MOD_NONE, wx.WXK_F7], False)
    def canvasTool(self, f, idx):
        def canvasTool_(event):
            if  (self.currentTool.__class__ == ToolObject)                  \
            and (self.currentTool.toolState >  self.currentTool.TS_NONE)    \
            and self.currentTool.external:
                self.parentCanvas.dropTarget.done()
            self.lastTool, self.currentTool = self.currentTool, [ToolCircle, None, ToolErase, ToolFill, ToolLine, ToolObject, ToolPickColour, ToolRect, ToolText][idx]
            if self.currentTool != None:
                self.currentTool = self.currentTool()
            self.currentOperator, self.operatorState = None, None
            self.parentFrame.menuItemsById[self.canvasTool.attrList[idx]["id"]].Check(True)
            if self.currentTool.__class__ == ToolObject:
                self.parentFrame.menuItemsById[self.canvasOperator.attrList[4]["id"]].Enable(True)
            else:
                self.parentFrame.menuItemsById[self.canvasOperator.attrList[4]["id"]].Enable(False)
            toolBar = self.parentFrame.toolBarItemsById[self.canvasTool.attrList[idx]["id"]][0]
            toolBar.ToggleTool(self.canvasTool.attrList[idx]["id"], True); toolBar.Refresh();
            if self.currentTool != None:
                self.update(operator=None, toolName=self.currentTool.name)
            else:
                self.update(operator=None, toolName="Cursor")
            viewRect = self.parentCanvas.GetViewStart()
            eventDc = self.parentCanvas.backend.getDeviceContext(self.parentCanvas.GetClientSize(), self.parentCanvas, viewRect)
            self.parentCanvas.applyTool(eventDc, True, None, None, None, self.parentCanvas.brushPos, False, False, False, self.currentTool, viewRect, force=True)
        setattr(canvasTool_, "attrDict", f.attrList[idx])
        setattr(canvasTool_, "isSelect", True)
        return canvasTool_

    def __init__(self):
        self.accels = ()
        self.menus = (
            ("&Tools",
                self.canvasTool(self.canvasTool, 1), self.canvasTool(self.canvasTool, 7), self.canvasTool(self.canvasTool, 0), self.canvasTool(self.canvasTool, 3), self.canvasTool(self.canvasTool, 4), self.canvasTool(self.canvasTool, 8), self.canvasTool(self.canvasTool, 5), self.canvasTool(self.canvasTool, 2), self.canvasTool(self.canvasTool, 6),
            ),
        )
        self.toolBars = ()
        self.currentTool, self.lastTool = None, None

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
