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
                        dispatchFn(eventDc, False, patch); dispatchFn(eventDc, True, patch);
                    else:
                        dispatchFn(eventDc, True, patch)
        return True, dirty

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
