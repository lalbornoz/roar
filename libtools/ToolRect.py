#!/usr/bin/env python3
#
# ToolRect.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolRect(Tool):
    name = "Rectangle"

    #
    # onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown)
    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        brushColours, dirty = brushColours.copy(), False
        if mouseLeftDown:
            brushColours[1] = brushColours[0]
        elif mouseRightDown:
            brushColours[0] = brushColours[1]
        else:
            brushColours[1] = brushColours[0]
        brushSize = brushSize.copy()
        if brushSize[0] > 1:
            brushSize[0] *= 2
        for brushRow in range(brushSize[1]):
            for brushCol in range(brushSize[0]):
                patch = [mapPoint[0] + brushCol, mapPoint[1] + brushRow, *brushColours, 0, " "]
                if mouseLeftDown or mouseRightDown:
                    if not dirty:
                        dirty = True
                    dispatchFn(eventDc, False, patch); dispatchFn(eventDc, True, patch);
                else:
                    dispatchFn(eventDc, True, patch)
        return True, dirty

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
