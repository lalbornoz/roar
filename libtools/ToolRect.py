#!/usr/bin/env python3
#
# ToolRect.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool
import wx

class ToolRect(Tool):
    name = "Rectangle"
    TS_NONE     = 0
    TS_ORIGIN   = 1

    def _drawRect(self, brushColours, canvas, rect):
        patches = []
        for brushRow in range(rect[3] - rect[1]):
            for brushCol in range(rect[2] - rect[0]):
                if (brushCol in [0, (rect[2] - rect[0]) - 1]) or (brushRow in [0, (rect[3] - rect[1]) - 1]):
                    patchColours = [brushColours[0]] * 2
                    patch = [rect[0] + brushCol, rect[1] + brushRow, *patchColours, 0, " "]
                elif brushColours[1] == -1:
                    if  ((rect[0] + brushCol) < canvas.size[0]) \
                    and ((rect[1] + brushRow) < canvas.size[1]):
                        patch = [rect[0] + brushCol, rect[1] + brushRow, *canvas.map[rect[1] + brushRow][rect[0] + brushCol]]
                    else:
                        patch = [rect[0] + brushCol, rect[1] + brushRow, -1, -1, 0, " "]
                else:
                    patchColours = [brushColours[1]] * 2
                    patch = [rect[0] + brushCol, rect[1] + brushRow, *patchColours, 0, " "]
                patches += [patch]
        return patches

    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        brushColours = [brushColours[1], brushColours[0]] if mouseRightDown else brushColours
        brushSize, patches = list(brushSize), []; brushSize[0] *= 2 if brushSize[0] > 1 else brushSize[0];
        if self.toolState == self.TS_NONE:
            if (keyModifiers == wx.MOD_CONTROL) and (mouseLeftDown or mouseRightDown):
                self.brushColours, isCursor, self.originPoint, self.toolState = list(brushColours), True, list(mapPoint), self.TS_ORIGIN
            else:
                isCursor = not (mouseLeftDown or mouseRightDown)
            rect = [*mapPoint, *[a + b for a, b in zip(brushSize, mapPoint)]]
        elif self.toolState == self.TS_ORIGIN:
            rect = [*self.originPoint, *mapPoint]
            if keyModifiers != wx.MOD_CONTROL:
                brushColours, isCursor, self.brushColours, self.originPoint, self.toolState = self.brushColours, False, None, None, self.TS_NONE
            else:
                isCursor = True
        patches = self._drawRect(brushColours, canvas, rect)
        return True, patches if not isCursor else None, patches if isCursor else None

    def __init__(self, *args):
        super().__init__(*args); self.brushColours, self.originPoint, self.toolState = None, None, self.TS_NONE;

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
