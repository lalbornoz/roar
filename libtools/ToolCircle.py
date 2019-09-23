#!/usr/bin/env python3
#
# ToolCircle.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolCircle(Tool):
    name = "Circle"

    #
    # onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown)
    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        brushColours, brushSize, dirty = list(brushColours), [brushSize[0] * 2, brushSize[1]], False
        originPoint, radius = (brushSize[0] / 2, brushSize[0] / 2), brushSize[0]
        if mouseRightDown:
            brushColours = [brushColours[1], brushColours[0]]
        cells = []
        for brushY in range(-radius, radius + 1):
            cells += [[]]
            for brushX in range(-radius, radius + 1):
                if ((brushX ** 2) + (brushY ** 2) < (((radius ** 2) + radius) * 0.8)):
                    cells[-1] += [[mapPoint[i] + int(originPoint[i] + o) for i, o in zip((0, 1,), (brushX, brushY,))]]
            if cells[-1] == []:
                del cells[-1]
        for numRow in range(len(cells)):
            for numCol in range(len(cells[numRow])):
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
                if mouseLeftDown or mouseRightDown:
                    if not dirty:
                        dirty = True
                    dispatchFn(eventDc, False, patch); dispatchFn(eventDc, True, patch);
                else:
                    dispatchFn(eventDc, True, patch)
        return True, dirty

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
