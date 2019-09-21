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

    # {{{ _dispatchSelectEvent(self, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseLeftDown, selectRect)
    def _dispatchSelectEvent(self, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseLeftDown, selectRect):
        if mouseLeftDown:
            disp, isCursor = [mapPoint[m] - self.lastAtPoint[m] for m in [0, 1]], True
            newTargetRect = [[selectRect[n][m] + disp[m] for m in [0, 1]] for n in [0, 1]]
            self.lastAtPoint = list(mapPoint)
        else:
            disp, isCursor, newTargetRect = [0, 0], True, selectRect.copy()
        dirty = self.onSelectEvent(canvas, disp, dispatchFn, eventDc, isCursor, keyModifiers, newTargetRect, selectRect)
        self._drawSelectRect(newTargetRect, dispatchFn, eventDc)
        self.targetRect = newTargetRect
        return dirty
    # }}}
    # {{{ _drawSelectRect(self, rect, dispatchFn, eventDc)
    def _drawSelectRect(self, rect, dispatchFn, eventDc):
        rectFrame = [[rect[m][n] for n in [0, 1]] for m in (0, 1)]
        if rectFrame[0][0] > rectFrame[1][0]:
            rectFrame[0][0], rectFrame[1][0] = rectFrame[1][0], rectFrame[0][0]
        if rectFrame[0][1] > rectFrame[1][1]:
            rectFrame[0][1], rectFrame[1][1] = rectFrame[1][1], rectFrame[0][1]
        curColours, rectFrame = [0, 0], [[rectFrame[m[0]][n] + m[1] for n in [0, 1]] for m in [[0, -1], [1, +1]]]
        for rectX in range(rectFrame[0][0], rectFrame[1][0] + 1):
            curColours = [1, 1] if curColours == [0, 0] else [0, 0]
            dispatchFn(eventDc, True, [rectX, rectFrame[0][1], *curColours, 0, " "])
            dispatchFn(eventDc, True, [rectX, rectFrame[1][1], *curColours, 0, " "])
        for rectY in range(rectFrame[0][1], rectFrame[1][1] + 1):
            curColours = [1, 1] if curColours == [0, 0] else [0, 0]
            dispatchFn(eventDc, True, [rectFrame[0][0], rectY, *curColours, 0, " "])
            dispatchFn(eventDc, True, [rectFrame[1][0], rectY, *curColours, 0, " "])
    # }}}
    # {{{ _mouseEventTsNone(self, brushColours, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown)
    def _mouseEventTsNone(self, brushColours, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown):
        self.substract = False
        if self.external:
            dispatchFn(eventDc, True, [*mapPoint, *brushColours, 0, " "])
        else:
            if mouseLeftDown:
                self.targetRect, self.toolState = [list(mapPoint), []], self.TS_ORIGIN
            else:
                dispatchFn(eventDc, True, [*mapPoint, *brushColours, 0, " "])
        return False
    # }}}
    # {{{ _mouseEventTsOrigin(self, brushColours, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown)
    def _mouseEventTsOrigin(self, brushColours, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown):
        self.targetRect[1] = list(mapPoint)
        if mouseLeftDown:
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
            self._drawSelectRect(self.targetRect, dispatchFn, eventDc)
        else:
            self._drawSelectRect(self.targetRect, dispatchFn, eventDc)
        return False
    # }}}
    # {{{ _mouseEventTsSelect(self, brushColours, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown)
    def _mouseEventTsSelect(self, brushColours, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown):
        dirty = False
        if mouseLeftDown:
            if  (mapPoint[0] >= (self.targetRect[0][0] - 1))    \
            and (mapPoint[0] <= (self.targetRect[1][0] + 1))    \
            and (mapPoint[1] >= (self.targetRect[0][1] - 1))    \
            and (mapPoint[1] <= (self.targetRect[1][1] + 1)):
                self.lastAtPoint, self.toolState = list(mapPoint), self.TS_TARGET
            else:
                dirty = self.onSelectEvent(canvas, (0, 0), dispatchFn, eventDc, False, keyModifiers, self.targetRect.copy(), self.targetRect)
                self._drawSelectRect(self.targetRect, dispatchFn, eventDc)
                self.objectMap, self.objectSize, self.targetRect, self.toolState = None, None, None, self.TS_NONE
        else:
            dirty = self._dispatchSelectEvent(canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseLeftDown, self.targetRect)
        return dirty
    # }}}
    # {{{ _mouseEventTsTarget(self, brushColours, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown)
    def _mouseEventTsTarget(self, brushColours, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown):
        if (keyModifiers == wx.MOD_CONTROL) and (self.srcRect == self.targetRect):
            self.substract = True
        dirty = False
        if mouseLeftDown:
            dirty = self._dispatchSelectEvent(canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseLeftDown, self.targetRect)
        else:
            self.toolState = self.TS_SELECT
        return dirty
    # }}}

    # {{{ getRegion(self, canvas)
    def getRegion(self, canvas):
        return self.objectMap
    # }}}
    # {{{ onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown)
    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        dirty = False
        if self.toolState == self.TS_NONE:
            dirty = self._mouseEventTsNone(brushColours, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown)
        elif self.toolState == self.TS_SELECT:
            dirty = self._mouseEventTsSelect(brushColours, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown)
        elif self.toolState == self.TS_ORIGIN:
            dirty = self._mouseEventTsOrigin(brushColours, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown)
        elif self.toolState == self.TS_TARGET:
            dirty = self._mouseEventTsTarget(brushColours, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown)
        else:
            return False, dirty
        return True, dirty
    # }}}
    # {{{ onSelectEvent(self, canvas, disp, dispatchFn, eventDc, isCursor, keyModifiers, newTargetRect, selectRect)
    def onSelectEvent(self, canvas, disp, dispatchFn, eventDc, isCursor, keyModifiers, newTargetRect, selectRect):
        dirty = False
        if self.external:
            for numRow in range(len(self.objectMap)):
                for numCol in range(len(self.objectMap[numRow])):
                    rectX, rectY = selectRect[0][0] + numCol, selectRect[0][1] + numRow
                    dirty = False if isCursor else True
                    cellNew = self.objectMap[numRow][numCol]
                    if (cellNew[1] == -1) and (cellNew[3] == " "):
                        if ((rectY + disp[1]) < canvas.size[1]) and ((rectX + disp[0]) < canvas.size[0]):
                            cellNew = canvas.map[rectY + disp[1]][rectX + disp[0]]
                    dispatchFn(eventDc, isCursor, [rectX + disp[0], rectY + disp[1], *cellNew])
        else:
            if self.substract:
                for numRow in range(self.srcRect[0][1], self.srcRect[1][1]):
                    for numCol in range(self.srcRect[0][0], self.srcRect[1][0]):
                        if  ((numCol < selectRect[0][0]) or (numCol > selectRect[1][0]))    \
                        or  ((numRow < selectRect[0][1]) or (numRow > selectRect[1][1])):
                            dirty = False if isCursor else True
                            dispatchFn(eventDc, isCursor, [numCol, numRow, 1, 1, 0, " "])
            for numRow in range(len(self.objectMap)):
                for numCol in range(len(self.objectMap[numRow])):
                    cellOld = self.objectMap[numRow][numCol]
                    rectX, rectY = selectRect[0][0] + numCol, selectRect[0][1] + numRow
                    dirty = False if isCursor else True
                    dispatchFn(eventDc, isCursor, [rectX + disp[0], rectY + disp[1], *cellOld])
        return dirty
    # }}}
    # {{{ setRegion(self, canvas, mapPoint, objectMap, objectSize, external=True)
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
    # }}}

    # __init__(self, *args): initialisation method
    def __init__(self, *args):
        super().__init__(*args)
        self.external, self.lastAtPoint, self.srcRect, self.substract,          \
            self.targetRect, self.objectMap, self.objectSize, self.toolState =  \
                False, None, None, False, None, [], None, self.TS_NONE

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
