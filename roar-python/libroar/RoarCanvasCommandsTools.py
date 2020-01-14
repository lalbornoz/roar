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
            if  (self.currentTool.__class__ == ToolObject)              \
            and (self.currentTool.toolState > self.currentTool.TS_NONE) \
            and self.currentTool.external:
                self.parentCanvas.dropTarget.done()
            self.lastTool, self.currentTool = self.currentTool, [ToolCircle, None, ToolErase, ToolFill, ToolLine, ToolObject, ToolPickColour, ToolRect, ToolText][idx]
            if self.currentTool != None:
                self.currentTool = self.currentTool()
            self.currentOperator, self.operatorState = None, None
            self.update(currentTool=self.currentTool, currentToolIdx=idx, operator=None)
            self.parentCanvas.applyTool(None, True, None, None, None, self.parentCanvas.brushPos, False, False, False, self.currentTool, None, force=True)
        setattr(canvasTool_, "attrDict", f.attrList[idx])
        setattr(canvasTool_, "isSelect", True)
        return canvasTool_

    def __init__(self):
        self.currentTool, self.lastTool = None, None

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
