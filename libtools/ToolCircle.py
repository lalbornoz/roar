#!/usr/bin/env python3
#
# ToolCircle.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool
import wx

class ToolCircle(Tool):
    name = "Circle"
    TS_NONE     = 0
    TS_ORIGIN   = 1

    def _drawCircle(self, brushColours, canvas, mapPoint, originPoint, radius):
        cells, patches = [], []
        for brushY in range(-radius, radius + 1):
            cells += [[]]
            for brushX in range(-radius, radius + 1):
                if ((brushX ** 2) + (brushY ** 2) < (((radius ** 2) + radius) * 0.8)):
                    cells[-1] += [[mapPoint[i] + int(originPoint[i] + o) for i, o in zip((0, 1,), (brushX, brushY,))]]
            if cells[-1] == []:
                del cells[-1]
        for numRow in range(len(cells)):
            for numCol in range(len(cells[numRow])):
                point = cells[numRow][numCol]
                if  ((point[0] >= 0) and (point[1] >= 0))                                           \
                and (point[0] < canvas.size[0]) and (point[1] < canvas.size[1]):
                    if ((numRow == 0) or (numRow == (len(cells) - 1)))                              \
                    or ((numCol == 0) or (numCol == (len(cells[numRow]) - 1))):
                        patch = [*cells[numRow][numCol], brushColours[0], brushColours[0], 0, " "]
                    elif ((numRow > 0) and (cells[numRow][numCol][0] < cells[numRow - 1][0][0]))    \
                    or   ((numRow < len(cells)) and (cells[numRow][numCol][0] < cells[numRow + 1][0][0])):
                        patch = [*cells[numRow][numCol], brushColours[0], brushColours[0], 0, " "]
                    elif ((numRow > 0) and (cells[numRow][numCol][0] > cells[numRow - 1][-1][0]))   \
                    or   ((numRow < len(cells)) and (cells[numRow][numCol][0] > cells[numRow + 1][-1][0])):
                        patch = [*cells[numRow][numCol], brushColours[0], brushColours[0], 0, " "]
                    elif brushColours[1] == -1:
                        if  (cells[numRow][numCol][0] < canvas.size[0])                             \
                        and (cells[numRow][numCol][1] < canvas.size[1]):
                            patch = [cells[numRow][numCol][0], cells[numRow][numCol][1], *canvas.map[cells[numRow][numCol][1]][cells[numRow][numCol][0]]]
                        else:
                            patch = [*cells[numRow][numCol], brushColours[1], brushColours[1], 0, " "]
                    else:
                        patch = [*cells[numRow][numCol], brushColours[1], brushColours[1], 0, " "]
                    patches += [patch]
        return patches

    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        brushColours, brushSize = [brushColours[1], brushColours[0]] if mouseRightDown else brushColours, brushSize[0] * 2
        if self.toolState == self.TS_NONE:
            originPoint, radius, targetPoint = list(mapPoint), brushSize, (brushSize / 2,) * 2
            if (keyModifiers == wx.MOD_CONTROL) and (mouseLeftDown or mouseRightDown):
                self.brushColours, isCursor, self.originPoint, self.toolState = brushColours, True, originPoint, self.TS_ORIGIN
            else:
                isCursor = not (mouseLeftDown or mouseRightDown)
        elif self.toolState == self.TS_ORIGIN:
            if mapPoint[0] > self.originPoint[0]:
                brushSize += (mapPoint[0] - self.originPoint[0]); brushSize = brushSize + (brushSize % 2);
            brushColours, originPoint, radius, targetPoint = self.brushColours, self.originPoint, brushSize, (brushSize / 2,) * 2
            if not (mouseLeftDown or mouseRightDown):
                self.brushColours, isCursor, self.originPoint, self.toolState = None, False, None, self.TS_NONE
            else:
                isCursor = True
        patches = self._drawCircle(brushColours, canvas, originPoint, targetPoint, radius)
        return True, patches if not isCursor else None, patches if isCursor else None

    def __init__(self, *args):
        super().__init__(*args); self.brushColours, self.originPoint, self.toolState = None, None, self.TS_NONE;

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
