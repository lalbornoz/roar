#!/usr/bin/env python3
#
# ToolErase.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolErase(Tool):
    name = "Erase"

    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        brushColours, brushSize, dirty = list(brushColours), list(brushSize), False
        if brushSize[0] > 1:
            brushSize[0] *= 2
        for brushRow in range(brushSize[1]):
            for brushCol in range(brushSize[0]):
                if mouseLeftDown:
                    patch = [mapPoint[0] + brushCol, mapPoint[1] + brushRow, brushColours[1], brushColours[1], 0, " "]
                    if not dirty:
                        dirty = True
                    dispatchFn(eventDc, False, patch); dispatchFn(eventDc, True, patch);
                elif mouseRightDown                                 \
                and  ((mapPoint[0] + brushCol) < canvas.size[0])    \
                and  ((mapPoint[1] + brushRow) < canvas.size[1])    \
                and  (canvas.map[mapPoint[1] + brushRow][mapPoint[0] + brushCol][1] == brushColours[1]):
                    patch = [mapPoint[0] + brushCol, mapPoint[1] + brushRow, canvas.map[mapPoint[1] + brushRow][mapPoint[0] + brushCol][0], brushColours[0], *canvas.map[mapPoint[1] + brushRow][mapPoint[0] + brushCol][2:]]
                    if not dirty:
                        dirty = True
                    dispatchFn(eventDc, False, patch); dispatchFn(eventDc, True, patch);
                else:
                    patch = [mapPoint[0] + brushCol, mapPoint[1] + brushRow, brushColours[1], brushColours[1], 0, " "]
                    dispatchFn(eventDc, True, patch)
        return True, dirty

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
