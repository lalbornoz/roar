#!/usr/bin/env python3
#
# ToolRect.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolRect(Tool):
    name = "Rectangle"

    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        brushColours, brushSize, isCursor, patches = list(brushColours), list(brushSize), not (mouseLeftDown or mouseRightDown), []
        if mouseRightDown:
            brushColours = [brushColours[1], brushColours[0]]
        if brushSize[0] > 1:
            brushSize[0] *= 2
        for brushRow in range(brushSize[1]):
            for brushCol in range(brushSize[0]):
                if (brushCol in [0, brushSize[0] - 1])              \
                or (brushRow in [0, brushSize[1] - 1]):
                    patchColours = [brushColours[0]] * 2
                    patch = [mapPoint[0] + brushCol, mapPoint[1] + brushRow, *patchColours, 0, " "]
                elif brushColours[1] == -1:
                    if  ((mapPoint[0] + brushCol) < canvas.size[0]) \
                    and ((mapPoint[1] + brushRow) < canvas.size[1]):
                        patch = [mapPoint[0] + brushCol, mapPoint[1] + brushRow, *canvas.map[mapPoint[1] + brushRow][mapPoint[0] + brushCol]]
                    else:
                        patch = [mapPoint[0] + brushCol, mapPoint[1] + brushRow, -1, -1, 0, " "]
                else:
                    patchColours = [brushColours[1]] * 2
                    patch = [mapPoint[0] + brushCol, mapPoint[1] + brushRow, *patchColours, 0, " "]
                patches += [patch]
        return True, patches if not isCursor else None, patches if isCursor else None

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
