#!/usr/bin/env python3
#
# ToolLine.py -- XXX
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolLine(Tool):
    """XXX"""
    name = "Line"
    TS_NONE     = 0
    TS_ORIGIN   = 1

    # {{{ _getLine(self, brushColours, brushSize, dispatchFn, eventDc, isCursor, originPoint, targetPoint): XXX
    def _getLine(self, brushColours, brushSize, dispatchFn, eventDc, isCursor, originPoint, targetPoint):
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
        for lineX in range(pointDelta[0] + 1):
            for brushStep in range(brushSize[0]):
                patch = [                                                               \
                        originPoint[0] + lineX * lineXX + lineY * lineYX + brushStep,   \
                        originPoint[1] + lineX * lineXY + lineY * lineYY,               \
                        *brushColours, 0, " "]
                if isCursor:
                    dispatchFn(eventDc, False, patch); dispatchFn(eventDc, True, patch);
                else:
                    dispatchFn(eventDc, True, patch)
            if lineD > 0:
                lineD -= pointDelta[0]; lineY += 1;
            lineD += pointDelta[1]
    # }}}
    # {{{ _pointDelta(self, a, b): XXX
    def _pointDelta(self, a, b):
        return [a2 - a1 for a1, a2 in zip(a, b)]
    # }}}
    # {{{ _pointSwap(self, a, b): XXX
    def _pointSwap(self, a, b):
        return [b, a]
    # }}}

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
        if self.toolState == self.TS_NONE:
            if isLeftDown or isRightDown:
                self.toolColours, self.toolOriginPoint, self.toolState = brushColours, list(atPoint), self.TS_ORIGIN
            dispatchFn(eventDc, True, [*atPoint, *brushColours, 0, " "])
        elif self.toolState == self.TS_ORIGIN:
            originPoint, targetPoint = self.toolOriginPoint, list(atPoint)
            self._getLine(self.toolColours, brushSize, dispatchFn, eventDc, isLeftDown or isRightDown, originPoint, targetPoint)
            if isLeftDown or isRightDown:
                self.toolColours, self.toolOriginPoint, self.toolState = None, None, self.TS_NONE

    # __init__(self, *args): initialisation method
    def __init__(self, *args):
        super().__init__(*args)
        self.toolColours, self.toolOriginPoint, self.toolState = None, None, self.TS_NONE

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
