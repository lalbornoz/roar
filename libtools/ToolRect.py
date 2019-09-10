#!/usr/bin/env python3
#
# ToolRect.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolRect(Tool):
    name = "Rectangle"

    #
    # onMouseEvent(self, brushColours, brushSize, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def onMouseEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
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
                    dispatchFn(eventDc, False, patch, viewRect); dispatchFn(eventDc, True, patch, viewRect);
                else:
                    dispatchFn(eventDc, True, patch, viewRect)
        return True, dirty

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
