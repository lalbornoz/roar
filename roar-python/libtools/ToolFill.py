#!/usr/bin/env python3
#
# ToolFill.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool
import wx

class ToolFill(Tool):
    name = "Fill"

    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        isCursor, patches, pointsDone, pointStack, testChar, testColour = not (mouseLeftDown or mouseRightDown), [], [], [list(mapPoint)], canvas.map[mapPoint[1]][mapPoint[0]][3], canvas.map[mapPoint[1]][mapPoint[0]][0:2]
        if mouseLeftDown or mouseRightDown:
            fillColour = brushColours[0] if mouseLeftDown else brushColours[1]
            while len(pointStack) > 0:
                point = pointStack.pop()
                pointCell = canvas.map[point[1]][point[0]]
                if ((pointCell[1] == testColour[1]) and ((pointCell[3] == testChar) or (keyModifiers == wx.MOD_CONTROL)))   \
                or ((pointCell[3] == " ") and (pointCell[1] == testColour[1])):
                    if not point in pointsDone:
                        patches += [[*point, fillColour, fillColour, 0, " "]]
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
            patches = [[mapPoint[0], mapPoint[1], brushColours[0], brushColours[0], 0, " "]]
        return True, patches if not isCursor else None, patches if isCursor else None

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
