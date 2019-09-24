#!/usr/bin/env python3
#
# ToolLine.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolLine(Tool):
    name = "Line"
    TS_NONE     = 0
    TS_ORIGIN   = 1

    def _getLine(self, brushColours, brushSize, dispatchFn, eventDc, isCursor, originPoint, targetPoint):
        dirty = False
        originPoint, targetPoint = originPoint.copy(), targetPoint.copy()
        pointDelta = self._pointDelta(originPoint, targetPoint)
        lineXSign = 1 if pointDelta[0] > 0 else -1; lineYSign = 1 if pointDelta[1] > 0 else -1;
        pointDelta = [abs(a) for a in pointDelta]
        if pointDelta[0] > pointDelta[1]:
            lineXX, lineXY, lineYX, lineYY = lineXSign, 0, 0, lineYSign
        else:
            lineXX, lineXY, lineYX, lineYY = 0, lineYSign, lineXSign, 0
            pointDelta = [pointDelta[1], pointDelta[0]]
        lineD = 2 * pointDelta[1] - pointDelta[0]; lineY = 0;
        pointsDone = []
        for lineX in range(pointDelta[0] + 1):
            for brushStep in range(brushSize[0]):
                if not ([originPoint[0] + lineX * lineXX + lineY * lineYX + brushStep, originPoint[1] + lineX * lineXY + lineY * lineYY] in pointsDone):
                    patch = [                                                               \
                            originPoint[0] + lineX * lineXX + lineY * lineYX + brushStep,   \
                            originPoint[1] + lineX * lineXY + lineY * lineYY,               \
                            *brushColours, 0, " "]
                    if not isCursor:
                        if not dirty:
                            dirty = True
                        dispatchFn(eventDc, False, patch)
                    else:
                        dispatchFn(eventDc, True, patch)
                    pointsDone += [[originPoint[0] + lineX * lineXX + lineY * lineYX + brushStep, originPoint[1] + lineX * lineXY + lineY * lineYY]]
            if lineD > 0:
                lineD -= pointDelta[0]; lineY += 1;
            lineD += pointDelta[1]
        return dirty

    def _pointDelta(self, a, b):
        return [a2 - a1 for a1, a2 in zip(a, b)]

    def _pointSwap(self, a, b):
        return [b, a]

    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        brushColours, dirty = brushColours.copy(), False
        if mouseLeftDown:
            brushColours[1] = brushColours[0]
        elif mouseRightDown:
            brushColours[0] = brushColours[1]
        else:
            brushColours[1] = brushColours[0]
        if self.toolState == self.TS_NONE:
            if mouseLeftDown or mouseRightDown:
                self.toolOriginPoint, self.toolState = list(mapPoint), self.TS_ORIGIN
            dispatchFn(eventDc, True, [*mapPoint, *brushColours, 0, " "])
        elif self.toolState == self.TS_ORIGIN:
            originPoint, targetPoint = self.toolOriginPoint, list(mapPoint)
            if mouseLeftDown or mouseRightDown:
                dirty = self._getLine(brushColours, brushSize, dispatchFn, eventDc, False, originPoint, targetPoint)
                self.toolOriginPoint, self.toolState = None, self.TS_NONE
            else:
                dirty = self._getLine(brushColours, brushSize, dispatchFn, eventDc, True, originPoint, targetPoint)
        else:
            return False, dirty
        return True, dirty

    def __init__(self, *args):
        super().__init__(*args)
        self.toolOriginPoint, self.toolState = None, self.TS_NONE

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
