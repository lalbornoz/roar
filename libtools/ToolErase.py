#!/usr/bin/env python3
#
# ToolErase.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolErase(Tool):
    name = "Erase"

    #
    # onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown)
    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        brushColours, brushSize, dirty = list(brushColours), list(brushSize), False
        if mouseRightDown:
            brushColours = [brushColours[0], brushColours[0]]
        else:
            brushColours = [brushColours[1], brushColours[1]]
        if brushSize[0] > 1:
            brushSize[0] *= 2
        for brushRow in range(brushSize[1]):
            for brushCol in range(brushSize[0]):
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
