#!/usr/bin/env python3
#
# ToolFill.py -- XXX
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolFill(Tool):
    """XXX"""
    name = "Fill"

    #
    # onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc): XXX
    def onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc):
        pointStack, pointsDone = [list(atPoint)], []
        testColour = self.parentCanvas.canvasMap[atPoint[1]][atPoint[0]][0:2]
        if isLeftDown or isRightDown:
            if isRightDown:
                brushColours = [brushColours[1], brushColours[0]]
            while len(pointStack) > 0:
                point = pointStack.pop()
                pointCell = self.parentCanvas.canvasMap[point[1]][point[0]]
                if pointCell[0:2] == testColour:
                    if not point in pointsDone:
                        dispatchFn(eventDc, False, [*point, \
                            brushColours[0], brushColours[0], 0, " "])
                        if point[0] > 0:
                            pointStack.append([point[0] - 1, point[1]])
                        if point[0] < (self.parentCanvas.canvasSize[0] - 1):
                            pointStack.append([point[0] + 1, point[1]])
                        if point[1] > 0:
                            pointStack.append([point[0], point[1] - 1])
                        if point[1] < (self.parentCanvas.canvasSize[1] - 1):
                            pointStack.append([point[0], point[1] + 1])
                        pointsDone += [point]

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
