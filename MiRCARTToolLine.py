#!/usr/bin/env python3
#
# MiRCARTToolLine.py -- XXX
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from MiRCARTTool import MiRCARTTool

class MiRCARTToolLine(MiRCARTTool):
    """XXX"""
    toolOriginPoint = toolState = None

    TS_NONE     = 0
    TS_ORIGIN   = 1

    # {{{ _pointDelta(self, a, b): XXX
    def _pointDelta(self, a, b):
        return [a2-a1 for a1, a2 in zip(a, b)]
    # }}}
    # {{{ _pointSwap(self, a, b): XXX
    def _pointSwap(self, a, b):
        return [b, a]
    # }}}
    # {{{ _getLine(self, brushColours, brushSize, eventDc, isCursor, originPoint, targetPoint, dispatchFn): XXX
    def _getLine(self, brushColours, brushSize, eventDc, isCursor, originPoint, targetPoint, dispatchFn):
        originPoint = originPoint.copy(); targetPoint = targetPoint.copy();
        pointDelta = self._pointDelta(originPoint, targetPoint)
        lineXSign = 1 if pointDelta[0] > 0 else -1;
        lineYSign = 1 if pointDelta[1] > 0 else -1;
        pointDelta = [abs(a) for a in pointDelta]
        if pointDelta[0] > pointDelta[1]:
            lineXX, lineXY, lineYX, lineYY = lineXSign, 0, 0, lineYSign
        else:
            pointDelta = [pointDelta[1], pointDelta[0]]
            lineXX, lineXY, lineYX, lineYY = 0, lineYSign, lineXSign, 0
        lineD = 2 * pointDelta[1] - pointDelta[0]; lineY = 0;
        for lineX in range(pointDelta[0] + 1):
            for brushStep in range(brushSize[0]):
                patch = [[                                                          \
                        originPoint[0] + lineX*lineXX + lineY*lineYX + brushStep,   \
                        originPoint[1] + lineX*lineXY + lineY*lineYY],              \
                        brushColours, 0, " "]
                if isCursor:
                    dispatchFn(eventDc, False, patch); dispatchFn(eventDc, True, patch);
                else:
                    dispatchFn(eventDc, True, patch)
            if lineD > 0:
                lineD -= pointDelta[0]; lineY += 1;
            lineD += pointDelta[1]
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
                self.toolOriginPoint = list(atPoint)
                self.toolState = self.TS_ORIGIN
            dispatchFn(eventDc, True, [atPoint, brushColours, 0, " "])
        elif self.toolState == self.TS_ORIGIN:
            targetPoint = list(atPoint)
            originPoint = self.toolOriginPoint
            self._getLine(brushColours, brushSize,  \
                eventDc, isLeftDown or isRightDown, \
                originPoint, targetPoint, dispatchFn)
            if isLeftDown or isRightDown:
                self.toolState = self.TS_NONE

    # __init__(self, *args): initialisation method
    def __init__(self, *args):
        super().__init__(*args)
        self.toolOriginPoint = None
        self.toolState = self.TS_NONE

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
