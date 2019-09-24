#!/usr/bin/env python3
#
# ToolRect.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolRect(Tool):
    name = "Rectangle"

    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        brushColours, brushSize, dirty = list(brushColours), list(brushSize), False
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
                if mouseLeftDown or mouseRightDown:
                    if not dirty:
                        dirty = True
                    dispatchFn(eventDc, False, patch); dispatchFn(eventDc, True, patch);
                else:
                    dispatchFn(eventDc, True, patch)
        return True, dirty

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
