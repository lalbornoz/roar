#!/usr/bin/env python3
#
# ToolText.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool
import wx

class ToolText(Tool):
    name = "Text"

    #
    # onKeyboardEvent(self, event, atPoint, brushColours, brushSize, keyChar, dispatchFn, eventDc, viewRect)
    def onKeyboardEvent(self, event, atPoint, brushColours, brushSize, keyChar, dispatchFn, eventDc, viewRect):
        keyModifiers = event.GetModifiers()
        if  keyModifiers != wx.MOD_NONE \
        and keyModifiers != wx.MOD_SHIFT:
            return True
        else:
            if self.textPos == None:
                self.textPos = list(atPoint)
        dispatchFn(eventDc, False, [*self.textPos, *brushColours, 0, keyChar], viewRect)
        if self.textPos[0] < (self.parentCanvas.canvas.size[0] - 1):
            self.textPos[0] += 1
        elif self.textPos[1] < (self.parentCanvas.canvas.size[1] - 1):
            self.textPos[0] = 0; self.textPos[1] += 1;
        else:
            self.textPos = [0, 0]
        return False

    #
    # onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc, viewRect)
    def onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc, viewRect):
        if isLeftDown or isRightDown:
            self.textPos = list(atPoint)
        dispatchFn(eventDc, True, [*atPoint, *brushColours, 0, "_"], viewRect)

    # __init__(self, *args): initialisation method
    def __init__(self, *args):
        super().__init__(*args)
        self.textColours = self.textPos = None

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
