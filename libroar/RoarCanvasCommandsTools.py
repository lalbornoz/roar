#!/usr/bin/env python3
#
# RoarCanvasCommandsTools.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiFrame import GuiSelectDecorator
from ToolCircle import ToolCircle
from ToolFill import ToolFill
from ToolLine import ToolLine
from ToolRect import ToolRect
from ToolSelectClone import ToolSelectClone
from ToolSelectMove import ToolSelectMove
from ToolText import ToolText
import wx

class RoarCanvasCommandsTools():
    # {{{ canvasTool(self, f, idx)
    @GuiSelectDecorator(0, "Circle", "&Circle", ["toolCircle.png"], [wx.ACCEL_CTRL, ord("C")], False)
    @GuiSelectDecorator(1, "Clone", "Cl&one", ["toolClone.png"], [wx.ACCEL_CTRL, ord("E")], False)
    @GuiSelectDecorator(2, "Fill", "&Fill", ["toolFill.png"], [wx.ACCEL_CTRL, ord("F")], False)
    @GuiSelectDecorator(3, "Line", "&Line", ["toolLine.png"], [wx.ACCEL_CTRL, ord("L")], False)
    @GuiSelectDecorator(4, "Move", "&Move", ["toolMove.png"], [wx.ACCEL_CTRL, ord("M")], False)
    @GuiSelectDecorator(5, "Rectangle", "&Rectangle", ["toolRect.png"], [wx.ACCEL_CTRL, ord("R")], True)
    @GuiSelectDecorator(6, "Text", "&Text", ["toolText.png"], [wx.ACCEL_CTRL, ord("T")], False)
    def canvasTool(self, f, idx):
        def canvasTool_(event):
            self.lastTool, self.currentTool = self.currentTool, [ToolCircle, ToolSelectClone, ToolFill, ToolLine, ToolSelectMove, ToolRect, ToolText][idx]()
            self.parentFrame.menuItemsById[self.canvasTool.attrList[idx]["id"]].Check(True)
            toolBar = self.parentFrame.toolBarItemsById[self.canvasTool.attrList[idx]["id"]].GetToolBar()
            toolBar.ToggleTool(self.canvasTool.attrList[idx]["id"], True)
            self.update(toolName=self.currentTool.name)
            viewRect = self.parentCanvas.GetViewStart()
            eventDc = self.parentCanvas.backend.getDeviceContext(self.parentCanvas.GetClientSize(), self.parentCanvas, viewRect)
            self.parentCanvas.applyTool(eventDc, True, None, None, self.parentCanvas.brushPos, False, False, False, self.currentTool, viewRect)
        setattr(canvasTool_, "attrDict", f.attrList[idx])
        setattr(canvasTool_, "isSelect", True)
        return canvasTool_
    # }}}

    #
    # __init__(self)
    def __init__(self):
        self.menus = (
            ("&Tools",
                self.canvasTool(self.canvasTool, 5), self.canvasTool(self.canvasTool, 0), self.canvasTool(self.canvasTool, 2), self.canvasTool(self.canvasTool, 3), self.canvasTool(self.canvasTool, 6), self.canvasTool(self.canvasTool, 1), self.canvasTool(self.canvasTool, 4),
            ),
        )
        self.toolBars = ()
        self.currentTool, self.lastTool = None, None

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
