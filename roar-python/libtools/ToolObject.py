#!/usr/bin/env python3
#
# ToolObject.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool
import wx

class ToolObject(Tool):
    name = "Object"
    TS_NONE     = 0
    TS_ORIGIN   = 1
    TS_SELECT   = 2
    TS_TARGET   = 3

    def _dispatchSelectEvent(self, canvas, keyModifiers, mapPoint, mouseLeftDown, selectRect):
        if mouseLeftDown:
            disp, isCursor = [mapPoint[m] - self.lastAtPoint[m] for m in [0, 1]], True
            newTargetRect = [[selectRect[n][m] + disp[m] for m in [0, 1]] for n in [0, 1]]
            self.lastAtPoint = list(mapPoint)
        else:
            disp, isCursor, newTargetRect = [0, 0], True, selectRect.copy()
        rc, patches, patchesCursor = self.onSelectEvent(canvas, disp, isCursor, keyModifiers, newTargetRect, selectRect)
        patchesCursor = [] if patchesCursor == None else patchesCursor
        patchesCursor += self._drawSelectRect(newTargetRect)
        self.targetRect = newTargetRect
        return rc, patches, patchesCursor

    def _drawSelectRect(self, rect):
        patches = []
        rectFrame = [[rect[m][n] for n in [0, 1]] for m in (0, 1)]
        if rectFrame[0][0] > rectFrame[1][0]:
            rectFrame[0][0], rectFrame[1][0] = rectFrame[1][0], rectFrame[0][0]
        if rectFrame[0][1] > rectFrame[1][1]:
            rectFrame[0][1], rectFrame[1][1] = rectFrame[1][1], rectFrame[0][1]
        curColours, rectFrame = [0, 0], [[rectFrame[m[0]][n] + m[1] for n in [0, 1]] for m in [[0, -1], [1, +1]]]
        for rectX in range(rectFrame[0][0], rectFrame[1][0] + 1):
            curColours = [1, 1] if curColours == [0, 0] else [0, 0]
            patches += [[rectX, rectFrame[0][1], *curColours, 0, " "], [rectX, rectFrame[1][1], *curColours, 0, " "]]
        for rectY in range(rectFrame[0][1], rectFrame[1][1] + 1):
            curColours = [1, 1] if curColours == [0, 0] else [0, 0]
            patches += [[rectFrame[0][0], rectY, *curColours, 0, " "], [rectFrame[1][0], rectY, *curColours, 0, " "]]
        return patches

    def _mouseEventTsNone(self, brushColours, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown):
        patchesCursor = [[*mapPoint, brushColours[0], brushColours[0], 0, " "]]; self.substract = False;
        if (not self.external) and mouseLeftDown:
            self.targetRect, self.toolState = [list(mapPoint), []], self.TS_ORIGIN
        return True, None, patchesCursor

    def _mouseEventTsOrigin(self, brushColours, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown):
        self.targetRect[1] = list(mapPoint)
        if not mouseLeftDown:
            if self.targetRect[0][0] > self.targetRect[1][0]:
                self.targetRect[0][0], self.targetRect[1][0] = self.targetRect[1][0], self.targetRect[0][0]
            if self.targetRect[0][1] > self.targetRect[1][1]:
                self.targetRect[0][1], self.targetRect[1][1] = self.targetRect[1][1], self.targetRect[0][1]
            self.lastAtPoint, self.srcRect, self.objectMap, self.toolState = list(mapPoint), self.targetRect, [], self.TS_SELECT
            for numRow in range((self.targetRect[1][1] - self.targetRect[0][1]) + 1):
                self.objectMap.append([])
                for numCol in range((self.targetRect[1][0] - self.targetRect[0][0]) + 1):
                    rectX, rectY = self.targetRect[0][0] + numCol, self.targetRect[0][1] + numRow
                    self.objectMap[numRow].append(canvas.map[rectY][rectX])
        return True, None, self._drawSelectRect(self.targetRect)

    def _mouseEventTsSelect(self, brushColours, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown):
        rc, patches, patchesCursor = False, None, None
        if mouseLeftDown:
            if  (mapPoint[0] >= (self.targetRect[0][0] - 1))    \
            and (mapPoint[0] <= (self.targetRect[1][0] + 1))    \
            and (mapPoint[1] >= (self.targetRect[0][1] - 1))    \
            and (mapPoint[1] <= (self.targetRect[1][1] + 1)):
                self.lastAtPoint, self.toolState = list(mapPoint), self.TS_TARGET
            else:
                rc, patches, patchesCursor = self.onSelectEvent(canvas, (0, 0), False, keyModifiers, self.targetRect.copy(), self.targetRect)
                patchesCursor = [] if patchesCursor == None else patchesCursor
                patchesCursor += self._drawSelectRect(self.targetRect)
                self.objectMap, self.objectSize, self.targetRect, self.toolState = None, None, None, self.TS_NONE
        else:
            rc, patches, patchesCursor = self._dispatchSelectEvent(canvas, keyModifiers, mapPoint, mouseLeftDown, self.targetRect)
        return rc, patches, patchesCursor

    def _mouseEventTsTarget(self, brushColours, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown):
        rc, patches, patchesCursor = False, None, None
        if (keyModifiers == wx.MOD_CONTROL) and (self.srcRect == self.targetRect):
            self.substract = True
        if mouseLeftDown:
            rc, patches, patchesCursor = self._dispatchSelectEvent(canvas, keyModifiers, mapPoint, mouseLeftDown, self.targetRect)
        else:
            self.toolState = self.TS_SELECT
        return rc, patches, patchesCursor

    def getRegion(self, canvas):
        return self.objectMap

    def onKeyboardEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, keyChar, keyCode, keyModifiers, mapPoint):
        if  (ord(keyChar) == wx.WXK_ESCAPE) and (self.toolState >= self.TS_SELECT):
            rc, patches, patchesCursor = self.onSelectEvent(canvas, (0, 0), False, keyModifiers, self.targetRect.copy(), self.targetRect)
            patchesCursor = [] if patchesCursor == None else patchesCursor
            patchesCursor += self._drawSelectRect(self.targetRect)
            self.objectMap, self.objectSize, self.targetRect, self.toolState = None, None, None, self.TS_NONE
        else:
            rc, patches, patchesCursor = False, None, None
        return rc, patches, patchesCursor

    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        if self.toolState == self.TS_NONE:
            rc, patches, patchesCursor = self._mouseEventTsNone(brushColours, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown)
        elif self.toolState == self.TS_SELECT:
            rc, patches, patchesCursor = self._mouseEventTsSelect(brushColours, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown)
        elif self.toolState == self.TS_ORIGIN:
            rc, patches, patchesCursor = self._mouseEventTsOrigin(brushColours, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown)
        elif self.toolState == self.TS_TARGET:
            rc, patches, patchesCursor = self._mouseEventTsTarget(brushColours, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown)
        else:
            rc, patches, patchesCursor = False, None, None
        return rc, patches, patchesCursor

    def onSelectEvent(self, canvas, disp, isCursor, keyModifiers, newTargetRect, selectRect):
        patches = []
        if self.external:
            for numRow in range(len(self.objectMap)):
                for numCol in range(len(self.objectMap[numRow])):
                    rectX, rectY = selectRect[0][0] + numCol, selectRect[0][1] + numRow
                    cellNew = self.objectMap[numRow][numCol]
                    if (cellNew[1] == -1) and (cellNew[3] == " "):
                        if ((rectY + disp[1]) < canvas.size[1]) and ((rectX + disp[0]) < canvas.size[0]):
                            cellNew = canvas.map[rectY + disp[1]][rectX + disp[0]]
                    patches += [[rectX + disp[0], rectY + disp[1], *cellNew]]
        else:
            if self.substract:
                for numRow in range(self.srcRect[0][1], self.srcRect[1][1]):
                    for numCol in range(self.srcRect[0][0], self.srcRect[1][0]):
                        if  ((numCol < selectRect[0][0]) or (numCol > selectRect[1][0]))    \
                        or  ((numRow < selectRect[0][1]) or (numRow > selectRect[1][1])):
                            patches += [[numCol, numRow, 1, 1, 0, " "]]
            for numRow in range(len(self.objectMap)):
                for numCol in range(len(self.objectMap[numRow])):
                    cellOld = self.objectMap[numRow][numCol]
                    rectX, rectY = selectRect[0][0] + numCol, selectRect[0][1] + numRow
                    cellNew = self.objectMap[numRow][numCol]
                    if (cellNew[1] == -1) and (cellNew[3] == " "):
                        if ((rectY + disp[1]) < canvas.size[1]) and ((rectX + disp[0]) < canvas.size[0]):
                            cellNew = canvas.map[rectY + disp[1]][rectX + disp[0]]
                    patches += [[rectX + disp[0], rectY + disp[1], *cellNew]]
        return True, patches if not isCursor else None, patches if isCursor else None

    def setRegion(self, canvas, mapPoint, objectMap, objectSize, external=True):
        self.external, self.toolState = external, self.TS_SELECT
        if mapPoint != None:
            self.lastAtPoint = list(mapPoint)
        if self.targetRect == None:
            self.targetRect = [list(self.lastAtPoint), [(a + b) - (0 if a == b else 1) for a, b in zip(self.lastAtPoint, objectSize)]]
        elif self.objectSize != objectSize:
            if self.objectSize == None:
                self.objectSize = objectSize
            self.targetRect[1] = [t + d for t, d in zip(self.targetRect[1], (b - a for a, b in zip(self.objectSize, objectSize)))]
        if self.srcRect == None:
            self.srcRect = self.targetRect
        self.objectMap, self.objectSize = objectMap, objectSize

    def __init__(self, *args):
        super().__init__(*args)
        self.external, self.lastAtPoint, self.srcRect, self.substract,          \
            self.targetRect, self.objectMap, self.objectSize, self.toolState =  \
                False, None, None, False, None, [], None, self.TS_NONE

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
