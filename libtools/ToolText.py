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
    # onKeyboardEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, keyChar, keyModifiers, mapPoint, viewRect)
    def onKeyboardEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, keyChar, keyModifiers, mapPoint, viewRect):
        if keyModifiers in (wx.MOD_NONE, wx.MOD_SHIFT):
            rc, dirty = True, True
            if self.textPos == None:
                self.textPos = list(mapPoint)
            dispatchFn(eventDc, False, [*self.textPos, *brushColours, 0, keyChar], viewRect)
            if self.textPos[0] < (canvas.size[0] - 1):
                self.textPos[0] += 1
            elif self.textPos[1] < (canvas.size[1] - 1):
                self.textPos[0] = 0; self.textPos[1] += 1;
            else:
                self.textPos = [0, 0]
        else:
            rc, dirty = False, False
        return rc, dirty

    #
    # onMouseEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def onMouseEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        if mouseLeftDown or mouseRightDown:
            self.textPos = list(mapPoint)
        dispatchFn(eventDc, True, [*mapPoint, *brushColours, 0, "_"], viewRect)
        return True, False

    # __init__(self, *args): initialisation method
    def __init__(self, *args):
        super().__init__(*args)
        self.textColours = self.textPos = None

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
