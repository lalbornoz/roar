#!/usr/bin/env python3
#
# ToolCircle.py -- XXX
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolCircle(Tool):
    """XXX"""
    name = "Circle"

    #
    # onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc): XXX
    def onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc):
        brushColours = brushColours.copy()
        if isLeftDown:
            brushColours[1] = brushColours[0]
        elif isRightDown:
            brushColours[0] = brushColours[1]
        else:
            brushColours[1] = brushColours[0]
        _brushSize = brushSize[0] * 2
        originPoint, radius = (_brushSize / 2, _brushSize / 2), _brushSize
        for brushY in range(-radius, radius + 1):
            for brushX in range(-radius, radius + 1):
                if ((brushX ** 2) + (brushY ** 2) < (((radius ** 2) + radius) * 0.8)):
                    patch = [                                       \
                        atPoint[0] + int(originPoint[0] + brushX),  \
                        atPoint[1] + int(originPoint[1] + brushY),  \
                        *brushColours, 0, " "]
                    if isLeftDown or isRightDown:
                        dispatchFn(eventDc, False, patch); dispatchFn(eventDc, True, patch);
                    else:
                        dispatchFn(eventDc, True, patch)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
