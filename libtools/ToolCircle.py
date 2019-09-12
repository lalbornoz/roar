#!/usr/bin/env python3
#
# ToolCircle.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolCircle(Tool):
    name = "Circle"

    #
    # onMouseEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def onMouseEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        brushColours, dirty = brushColours.copy(), False
        if mouseLeftDown:
            brushColours[1] = brushColours[0]
        elif mouseRightDown:
            brushColours[0] = brushColours[1]
        else:
            brushColours[1] = brushColours[0]
        _brushSize = brushSize[0] * 2
        originPoint, radius = (_brushSize / 2, _brushSize / 2), _brushSize
        for brushY in range(-radius, radius + 1):
            for brushX in range(-radius, radius + 1):
                if ((brushX ** 2) + (brushY ** 2) < (((radius ** 2) + radius) * 0.8)):
                    patch = [                                       \
                        mapPoint[0] + int(originPoint[0] + brushX),  \
                        mapPoint[1] + int(originPoint[1] + brushY),  \
                        *brushColours, 0, " "]
                    if mouseLeftDown or mouseRightDown:
                        if not dirty:
                            dirty = True
                        dispatchFn(eventDc, False, patch, viewRect); dispatchFn(eventDc, True, patch, viewRect);
                    else:
                        dispatchFn(eventDc, True, patch, viewRect)
        return True, dirty

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
