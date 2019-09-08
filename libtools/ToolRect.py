#!/usr/bin/env python3
#
# ToolRect.py 
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolRect(Tool):
    name = "Rectangle"

    #
    # onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc)
    def onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc):
        brushColours = brushColours.copy()
        if isLeftDown:
            brushColours[1] = brushColours[0]
        elif isRightDown:
            brushColours[0] = brushColours[1]
        else:
            brushColours[1] = brushColours[0]
        brushSize = brushSize.copy()
        if brushSize[0] > 1:
            brushSize[0] *= 2
        for brushRow in range(brushSize[1]):
            for brushCol in range(brushSize[0]):
                patch = [atPoint[0] + brushCol, atPoint[1] + brushRow, *brushColours, 0, " "]
                if isLeftDown or isRightDown:
                    dispatchFn(eventDc, False, patch); dispatchFn(eventDc, True, patch);
                else:
                    dispatchFn(eventDc, True, patch)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
