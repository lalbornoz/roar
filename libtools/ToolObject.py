#!/usr/bin/env python3
#
# ToolObject.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolObject(Tool):
    name = "External object"
    TS_NONE     = 0
    TS_SELECT   = 1
    TS_TARGET   = 2

    # {{{ _dispatchSelectEvent(self, canvas, dispatchFn, eventDc, mapPoint, mouseLeftDown, mouseRightDown, selectRect, viewRect)
    def _dispatchSelectEvent(self, canvas, dispatchFn, eventDc, mapPoint, mouseLeftDown, mouseRightDown, selectRect, viewRect):
        if mouseLeftDown:
            disp, isCursor = [mapPoint[m] - self.lastAtPoint[m] for m in [0, 1]], True
            newTargetRect = [[selectRect[n][m] + disp[m] for m in [0, 1]] for n in [0, 1]]
            self.lastAtPoint = list(mapPoint)
        elif mouseRightDown:
            disp, isCursor, newTargetRect = [0, 0], False, selectRect.copy()
        else:
            disp, isCursor, newTargetRect = [0, 0], True, selectRect.copy()
        dirty = self.onSelectEvent(canvas, disp, dispatchFn, eventDc, isCursor, newTargetRect, selectRect, viewRect)
        self._drawSelectRect(newTargetRect, dispatchFn, eventDc, viewRect)
        self.targetRect = newTargetRect
        return dirty
    # }}}
    # {{{ _drawSelectRect(self, rect, dispatchFn, eventDc, viewRect)
    def _drawSelectRect(self, rect, dispatchFn, eventDc, viewRect):
        rectFrame = [[rect[m[0]][n] + m[1] for n in [0, 1]] for m in [[0, -1], [1, +1]]]
        if rectFrame[0][0] > rectFrame[1][0]:
            rectFrame[0][0], rectFrame[1][0] = rectFrame[1][0], rectFrame[0][0]
        if rectFrame[0][1] > rectFrame[1][1]:
            rectFrame[0][1], rectFrame[1][1] = rectFrame[1][1], rectFrame[0][1]
        curColours = [0, 0]
        for rectX in range(rectFrame[0][0], rectFrame[1][0] + 1):
            curColours = [1, 1] if curColours == [0, 0] else [0, 0]
            dispatchFn(eventDc, True, [rectX, rectFrame[0][1], *curColours, 0, " "], viewRect)
            dispatchFn(eventDc, True, [rectX, rectFrame[1][1], *curColours, 0, " "], viewRect)
        for rectY in range(rectFrame[0][1], rectFrame[1][1] + 1):
            curColours = [1, 1] if curColours == [0, 0] else [0, 0]
            dispatchFn(eventDc, True, [rectFrame[0][0], rectY, *curColours, 0, " "], viewRect)
            dispatchFn(eventDc, True, [rectFrame[1][0], rectY, *curColours, 0, " "], viewRect)
    # }}}
    # {{{ _mouseEventTsNone(self, brushColours, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def _mouseEventTsNone(self, brushColours, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        dispatchFn(eventDc, True, [*mapPoint, *brushColours, 0, " "], viewRect)
        return False
    # }}}
    # {{{ _mouseEventTsSelect(self, brushColours, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def _mouseEventTsSelect(self, brushColours, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        dirty = False
        if mouseLeftDown                                    \
        and  (mapPoint[0] >= (self.targetRect[0][0] - 1))   \
        and  (mapPoint[0] <= (self.targetRect[1][0] + 1))   \
        and  (mapPoint[1] >= (self.targetRect[0][1] - 1))   \
        and  (mapPoint[1] <= (self.targetRect[1][1] + 1)):
            self.lastAtPoint, self.toolState = list(mapPoint), self.TS_TARGET
        elif mouseRightDown:
            dirty = self._dispatchSelectEvent(canvas, dispatchFn, eventDc, mapPoint, mouseLeftDown, mouseRightDown, self.targetRect, viewRect)
            self.targetRect, self.toolState = None, self.TS_NONE
        else:
            dirty = self._dispatchSelectEvent(canvas, dispatchFn, eventDc, mapPoint, mouseLeftDown, mouseRightDown, self.targetRect, viewRect)
        return dirty
    # }}}
    # {{{ _mouseEventTsTarget(self, brushColours, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def _mouseEventTsTarget(self, brushColours, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        dirty = False
        if mouseLeftDown:
            dirty = self._dispatchSelectEvent(canvas, dispatchFn, eventDc, mapPoint, mouseLeftDown, mouseRightDown, self.targetRect, viewRect)
        elif mouseRightDown:
            dirty = self._dispatchSelectEvent(canvas, dispatchFn, eventDc, mapPoint, mouseLeftDown, mouseRightDown, self.targetRect, viewRect)
            self.targetRect, self.toolState = None, self.TS_NONE
        else:
            self.toolState = self.TS_SELECT
        return True, dirty
    # }}}

    #
    # onMouseEvent(self, brushColours, brushSize, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def onMouseEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        dirty = False
        if self.toolState == self.TS_NONE:
            dirty = self._mouseEventTsNone(brushColours, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
        elif self.toolState == self.TS_SELECT:
            dirty = self._mouseEventTsSelect(brushColours, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
        elif self.toolState == self.TS_TARGET:
            dirty = self._mouseEventTsTarget(brushColours, canvas, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
        else:
            return False, dirty
        return True, dirty

    #
    # onSelectEvent(self, canvas, disp, dispatchFn, eventDc, isCursor, newTargetRect, selectRect, viewRect)
    def onSelectEvent(self, canvas, disp, dispatchFn, eventDc, isCursor, newTargetRect, selectRect, viewRect):
        dirty = False
        for numRow in range(len(self.objectMap)):
            for numCol in range(len(self.objectMap[numRow])):
                rectX, rectY = selectRect[0][0] + numCol, selectRect[0][1] + numRow
                dirty = False if isCursor else True
                cellNew = self.objectMap[numRow][numCol]
                if (cellNew[1] == -1) and (cellNew[3] == " "):
                    if (rectY < canvas.size[1]) and (rectX < canvas.size[0]):
                        cellNew = canvas.map[rectY][rectX]
                dispatchFn(eventDc, isCursor, [rectX + disp[0], rectY + disp[1], *cellNew], viewRect)
        return dirty

    # __init__(self, canvas, mapPoint, objectMap, objectSize): initialisation method
    def __init__(self, canvas, mapPoint, objectMap, objectSize):
        super().__init__()
        self.lastAtPoint, self.srcRect = list(mapPoint), list(mapPoint)
        self.objectMap, self.objectSize = objectMap, objectSize
        self.targetRect = [list(mapPoint), [(a + b) - (0 if a == b else 1) for a, b in zip(mapPoint, objectSize)]]
        self.toolSelectMap, self.toolState = [], self.TS_SELECT
        for numRow in range((self.targetRect[1][1] - self.targetRect[0][1]) + 1):
            self.toolSelectMap.append([])
            for numCol in range((self.targetRect[1][0] - self.targetRect[0][0]) + 1):
                rectX, rectY = self.targetRect[0][0] + numCol, self.targetRect[0][1] + numRow
                if (rectX < canvas.size[0]) and (rectY < canvas.size[1]):
                    self.toolSelectMap[numRow].append(canvas.map[rectY][rectX])
                else:
                    self.toolSelectMap[numRow].append([1, 1, 0, " "])

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
