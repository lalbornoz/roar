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

    def _getLine(self, brushColours, brushSize, isCursor, originPoint, targetPoint):
        originPoint, patches, targetPoint = originPoint.copy(), [], targetPoint.copy()
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
                    patches += [[                                                           \
                            originPoint[0] + lineX * lineXX + lineY * lineYX + brushStep,   \
                            originPoint[1] + lineX * lineXY + lineY * lineYY,               \
                            *brushColours, 0, " "]]
                    pointsDone += [[originPoint[0] + lineX * lineXX + lineY * lineYX + brushStep, originPoint[1] + lineX * lineXY + lineY * lineYY]]
            if lineD > 0:
                lineD -= pointDelta[0]; lineY += 1;
            lineD += pointDelta[1]
        return patches

    def _pointDelta(self, a, b):
        return [a2 - a1 for a1, a2 in zip(a, b)]

    def _pointSwap(self, a, b):
        return [b, a]

    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        brushColours, isCursor, patches, rc = brushColours.copy(), not (mouseLeftDown or mouseRightDown), [], False
        if mouseLeftDown:
            brushColours[1] = brushColours[0]
        elif mouseRightDown:
            brushColours[0] = brushColours[1]
        else:
            brushColours[1] = brushColours[0]
        if self.toolState == self.TS_NONE:
            if mouseLeftDown or mouseRightDown:
                self.toolOriginPoint, self.toolState = list(mapPoint), self.TS_ORIGIN
            patches, rc = [], True
            for brushCol in range(brushSize[0]):
                if  ((mapPoint[0] + brushCol) < canvas.size[0]) \
                and (mapPoint[1] < canvas.size[1]):
                    patches += [[mapPoint[0] + brushCol, mapPoint[1], *brushColours, 0, " "]]
        elif self.toolState == self.TS_ORIGIN:
            originPoint, targetPoint = self.toolOriginPoint, list(mapPoint)
            if mouseLeftDown or mouseRightDown:
                patches = self._getLine(brushColours, brushSize, False, originPoint, targetPoint)
                self.toolOriginPoint, self.toolState = None, self.TS_NONE
            else:
                patches = self._getLine(brushColours, brushSize, True, originPoint, targetPoint)
            rc = True
        return rc, patches if not isCursor else None, patches if isCursor else None

    def __init__(self, *args):
        super().__init__(*args)
        self.toolOriginPoint, self.toolState = None, self.TS_NONE

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
