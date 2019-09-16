#!/usr/bin/env python3
#
# ToolFill.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolFill(Tool):
    name = "Fill"

    #
    # onMouseEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def onMouseEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        dirty, pointsDone, pointStack, testChar, testColour = False, [], [list(mapPoint)], canvas.map[mapPoint[1]][mapPoint[0]][3], canvas.map[mapPoint[1]][mapPoint[0]][0:2]
        if mouseLeftDown or mouseRightDown:
            while len(pointStack) > 0:
                point = pointStack.pop()
                pointCell = canvas.map[point[1]][point[0]]
                if ((pointCell[1] == testColour[1]) and ((pointCell[3] == testChar) or mouseRightDown)) \
                or ((pointCell[3] == " ") and (pointCell[1] == testColour[1])):
                    if not point in pointsDone:
                        if not dirty:
                            dirty = True
                        dispatchFn(eventDc, False, [*point, brushColours[0], brushColours[0], 0, " "], viewRect)
                        if point[0] > 0:
                            pointStack.append([point[0] - 1, point[1]])
                        if point[0] < (canvas.size[0] - 1):
                            pointStack.append([point[0] + 1, point[1]])
                        if point[1] > 0:
                            pointStack.append([point[0], point[1] - 1])
                        if point[1] < (canvas.size[1] - 1):
                            pointStack.append([point[0], point[1] + 1])
                        pointsDone += [point]
        else:
            patch = [mapPoint[0], mapPoint[1], brushColours[0], brushColours[0], 0, " "]
            dispatchFn(eventDc, True, patch, viewRect)
        return True, dirty

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
