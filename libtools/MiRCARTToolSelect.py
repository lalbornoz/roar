#!/usr/bin/env python3
#
# MiRCARTToolSelect.py -- XXX
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from MiRCARTTool import MiRCARTTool

class MiRCARTToolSelect(MiRCARTTool):
    """XXX"""
    TS_NONE     = 0
    TS_ORIGIN   = 1
    TS_SELECT   = 2
    TS_TARGET   = 3

    # {{{ _dispatchSelectEvent(self, atPoint, dispatchFn, eventDc, isLeftDown, isRightDown, selectRect): XXX
    def _dispatchSelectEvent(self, atPoint, dispatchFn, eventDc, isLeftDown, isRightDown, selectRect):
        if isLeftDown:
            disp, isCursor = [atPoint[m] - self.lastAtPoint[m] for m in [0, 1]], True
            newTargetRect = [[selectRect[n][m] + disp[m] for m in [0, 1]] for n in [0, 1]]
            self.lastAtPoint = list(atPoint)
        elif isRightDown:
            disp, isCursor, newTargetRect = [0, 0], False, selectRect.copy()
        else:
            disp, isCursor, newTargetRect = [0, 0], True, selectRect.copy()
        self.onSelectEvent(disp, dispatchFn, eventDc, isCursor, newTargetRect, selectRect)
        self._drawSelectRect(newTargetRect, dispatchFn, eventDc)
        self.targetRect = newTargetRect
    # }}}
    # {{{ _drawSelectRect(self, rect, dispatchFn, eventDc): XXX
    def _drawSelectRect(self, rect, dispatchFn, eventDc):
        rectFrame = [[rect[m[0]][n] + m[1] for n in [0, 1]] for m in [[0, -1], [1, +1]]]
        if rectFrame[0][0] > rectFrame[1][0]:
            rectFrame[0][0], rectFrame[1][0] = rectFrame[1][0], rectFrame[0][0]
        if rectFrame[0][1] > rectFrame[1][1]:
            rectFrame[0][1], rectFrame[1][1] = rectFrame[1][1], rectFrame[0][1]
        curColours = [0, 0]
        for rectX in range(rectFrame[0][0], rectFrame[1][0]+1):
            curColours = [1, 1] if curColours == [0, 0] else [0, 0]
            dispatchFn(eventDc, True, [rectX, rectFrame[0][1], *curColours, 0, " "])
            dispatchFn(eventDc, True, [rectX, rectFrame[1][1], *curColours, 0, " "])
        for rectY in range(rectFrame[0][1], rectFrame[1][1]+1):
            curColours = [1, 1] if curColours == [0, 0] else [0, 0]
            dispatchFn(eventDc, True, [rectFrame[0][0], rectY, *curColours, 0, " "])
            dispatchFn(eventDc, True, [rectFrame[1][0], rectY, *curColours, 0, " "])
    # }}}
    # {{{ _mouseEventTsNone(self, atPoint, brushColours, dispatchFn, eventDc, isDragging, isLeftDown, isRightDown): XXX
    def _mouseEventTsNone(self, atPoint, brushColours, dispatchFn, eventDc, isDragging, isLeftDown, isRightDown):
        if isLeftDown:
            self.targetRect, self.toolState = [list(atPoint), []], self.TS_ORIGIN
        else:
            dispatchFn(eventDc, True, [*atPoint, *brushColours, 0, " "])
    # }}}
    # {{{ _mouseEventTsOrigin(self, atPoint, brushColours, dispatchFn, eventDc, isDragging, isLeftDown, isRightDown): XXX
    def _mouseEventTsOrigin(self, atPoint, brushColours, dispatchFn, eventDc, isDragging, isLeftDown, isRightDown):
        if isLeftDown:
            self.targetRect[1] = list(atPoint)
            if self.targetRect[0][0] > self.targetRect[1][0]:
                self.targetRect[0][0], self.targetRect[1][0] = self.targetRect[1][0], self.targetRect[0][0]
            if self.targetRect[0][1] > self.targetRect[1][1]:
                self.targetRect[0][1], self.targetRect[1][1] = self.targetRect[1][1], self.targetRect[0][1]
            self.srcRect, self.lastAtPoint, self.toolSelectMap, self.toolState = self.targetRect[0], list(atPoint), [], self.TS_SELECT
            for numRow in range((self.targetRect[1][1] - self.targetRect[0][1]) + 1):
                self.toolSelectMap.append([])
                for numCol in range((self.targetRect[1][0] - self.targetRect[0][0]) + 1):
                    rectX, rectY = self.targetRect[0][0] + numCol, self.targetRect[0][1] + numRow
                    self.toolSelectMap[numRow].append(self.parentCanvas.canvasMap[rectY][rectX])
            self._drawSelectRect(self.targetRect, dispatchFn, eventDc)
        elif isRightDown:
            self.targetRect, self.toolState = None, self.TS_NONE
        else:
            self.targetRect[1] = list(atPoint)
            self._drawSelectRect(self.targetRect, dispatchFn, eventDc)
    # }}}
    # {{{ _mouseEventTsSelect(self, atPoint, brushColours, dispatchFn, eventDc, isDragging, isLeftDown, isRightDown): XXX
    def _mouseEventTsSelect(self, atPoint, brushColours, dispatchFn, eventDc, isDragging, isLeftDown, isRightDown):
        if isLeftDown                                       \
        and  (atPoint[0] >= (self.targetRect[0][0] - 1))    \
        and  (atPoint[0] <= (self.targetRect[1][0] + 1))    \
        and  (atPoint[1] >= (self.targetRect[0][1] - 1))    \
        and  (atPoint[1] <= (self.targetRect[1][1] + 1)):
            self.lastAtPoint, self.toolState = list(atPoint), self.TS_TARGET
        elif isRightDown:
            self._dispatchSelectEvent(atPoint, dispatchFn, eventDc, isLeftDown, isRightDown, self.targetRect)
            self.targetRect, self.toolState = None, self.TS_NONE
        else:
            self._dispatchSelectEvent(atPoint, dispatchFn, eventDc, isLeftDown, isRightDown, self.targetRect)
    # }}}
    # {{{ _mouseEventTsTarget(self, atPoint, brushColours, dispatchFn, eventDc, isDragging, isLeftDown, isRightDown): XXX
    def _mouseEventTsTarget(self, atPoint, brushColours, dispatchFn, eventDc, isDragging, isLeftDown, isRightDown):
        if isLeftDown:
            self.toolState = self.TS_TARGET
            self._dispatchSelectEvent(atPoint, dispatchFn, eventDc, isLeftDown, isRightDown, self.targetRect)
        elif isRightDown:
            self._dispatchSelectEvent(atPoint, dispatchFn, eventDc, isLeftDown, isRightDown, self.targetRect)
            self.targetRect, self.toolState = None, self.TS_NONE
        else:
            self.toolState = self.TS_SELECT
    # }}}

    #
    # onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc): XXX
    def onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc):
        if self.toolState == self.TS_NONE:
            self._mouseEventTsNone(atPoint, brushColours, dispatchFn, eventDc, isDragging, isLeftDown, isRightDown)
        elif self.toolState == self.TS_ORIGIN:
            self._mouseEventTsOrigin(atPoint, brushColours, dispatchFn, eventDc, isDragging, isLeftDown, isRightDown)
        elif self.toolState == self.TS_SELECT:
            self._mouseEventTsSelect(atPoint, brushColours, dispatchFn, eventDc, isDragging, isLeftDown, isRightDown)
        elif self.toolState == self.TS_TARGET:
            self._mouseEventTsTarget(atPoint, brushColours, dispatchFn, eventDc, isDragging, isLeftDown, isRightDown)

    #
    # onSelectEvent(self, disp, dispatchFn, eventDc, isCursor, newTargetRect, selectRect): XXX
    def onSelectEvent(self, disp, dispatchFn, eventDc, isCursor, newTargetRect, selectRect):
        pass

    # __init__(self, *args): initialisation method
    def __init__(self, *args):
        super().__init__(*args)
        self.lastAtPoint, self.srcRect, self.targetRect,    \
            self.toolSelectMap, self.toolState =            \
                None, None, None, None, self.TS_NONE

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
