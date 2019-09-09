#!/usr/bin/env python3
#
# ToolSelect.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolSelect(Tool):
    TS_NONE     = 0
    TS_ORIGIN   = 1
    TS_SELECT   = 2
    TS_TARGET   = 3

    # {{{ _dispatchSelectEvent(self, mapPoint, dispatchFn, eventDc, mouseLeftDown, mouseRightDown, selectRect, viewRect)
    def _dispatchSelectEvent(self, mapPoint, dispatchFn, eventDc, mouseLeftDown, mouseRightDown, selectRect, viewRect):
        if mouseLeftDown:
            disp, isCursor = [mapPoint[m] - self.lastAtPoint[m] for m in [0, 1]], True
            newTargetRect = [[selectRect[n][m] + disp[m] for m in [0, 1]] for n in [0, 1]]
            self.lastAtPoint = list(mapPoint)
        elif mouseRightDown:
            disp, isCursor, newTargetRect = [0, 0], False, selectRect.copy()
        else:
            disp, isCursor, newTargetRect = [0, 0], True, selectRect.copy()
        dirty = self.onSelectEvent(disp, dispatchFn, eventDc, isCursor, newTargetRect, selectRect, viewRect)
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
    # {{{ _mouseEventTsNone(self, mapPoint, brushColours, dispatchFn, eventDc, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def _mouseEventTsNone(self, mapPoint, brushColours, dispatchFn, eventDc, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        if mouseLeftDown:
            self.targetRect, self.toolState = [list(mapPoint), []], self.TS_ORIGIN
        else:
            dispatchFn(eventDc, True, [*mapPoint, *brushColours, 0, " "], viewRect)
        return False
    # }}}
    # {{{ _mouseEventTsOrigin(self, mapPoint, brushColours, dispatchFn, eventDc, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def _mouseEventTsOrigin(self, mapPoint, brushColours, dispatchFn, eventDc, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        if mouseLeftDown:
            self.targetRect[1] = list(mapPoint)
            if self.targetRect[0][0] > self.targetRect[1][0]:
                self.targetRect[0][0], self.targetRect[1][0] = self.targetRect[1][0], self.targetRect[0][0]
            if self.targetRect[0][1] > self.targetRect[1][1]:
                self.targetRect[0][1], self.targetRect[1][1] = self.targetRect[1][1], self.targetRect[0][1]
            self.srcRect, self.lastAtPoint, self.toolSelectMap, self.toolState = self.targetRect[0], list(mapPoint), [], self.TS_SELECT
            for numRow in range((self.targetRect[1][1] - self.targetRect[0][1]) + 1):
                self.toolSelectMap.append([])
                for numCol in range((self.targetRect[1][0] - self.targetRect[0][0]) + 1):
                    rectX, rectY = self.targetRect[0][0] + numCol, self.targetRect[0][1] + numRow
                    self.toolSelectMap[numRow].append(self.parentCanvas.canvas.map[rectY][rectX])
            self._drawSelectRect(self.targetRect, dispatchFn, eventDc, viewRect)
        elif mouseRightDown:
            self.targetRect, self.toolState = None, self.TS_NONE
        else:
            self.targetRect[1] = list(mapPoint)
            self._drawSelectRect(self.targetRect, dispatchFn, eventDc, viewRect)
        return False
    # }}}
    # {{{ _mouseEventTsSelect(self, mapPoint, brushColours, dispatchFn, eventDc, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def _mouseEventTsSelect(self, mapPoint, brushColours, dispatchFn, eventDc, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        dirty = False
        if mouseLeftDown                                    \
        and  (mapPoint[0] >= (self.targetRect[0][0] - 1))   \
        and  (mapPoint[0] <= (self.targetRect[1][0] + 1))   \
        and  (mapPoint[1] >= (self.targetRect[0][1] - 1))   \
        and  (mapPoint[1] <= (self.targetRect[1][1] + 1)):
            self.lastAtPoint, self.toolState = list(mapPoint), self.TS_TARGET
        elif mouseRightDown:
            dirty = self._dispatchSelectEvent(mapPoint, dispatchFn, eventDc, mouseLeftDown, mouseRightDown, self.targetRect, viewRect)
            self.targetRect, self.toolState = None, self.TS_NONE
        else:
            dirty = self._dispatchSelectEvent(mapPoint, dispatchFn, eventDc, mouseLeftDown, mouseRightDown, self.targetRect, viewRect)
        return dirty
    # }}}
    # {{{ _mouseEventTsTarget(self, mapPoint, brushColours, dispatchFn, eventDc, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def _mouseEventTsTarget(self, mapPoint, brushColours, dispatchFn, eventDc, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        dirty = False
        if mouseLeftDown:
            self.toolState = self.TS_TARGET
            dirty = self._dispatchSelectEvent(mapPoint, dispatchFn, eventDc, mouseLeftDown, mouseRightDown, self.targetRect, viewRect)
        elif mouseRightDown:
            dirty = self._dispatchSelectEvent(mapPoint, dispatchFn, eventDc, mouseLeftDown, mouseRightDown, self.targetRect, viewRect)
            self.targetRect, self.toolState = None, self.TS_NONE
        else:
            self.toolState = self.TS_SELECT
        return dirty
    # }}}

    #
    # onMouseEvent(self, brushColours, brushSize, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def onMouseEvent(self, brushColours, brushSize, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        dirty = False
        if self.toolState == self.TS_NONE:
            dirty = self._mouseEventTsNone(mapPoint, brushColours, dispatchFn, eventDc, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
        elif self.toolState == self.TS_ORIGIN:
            dirty = self._mouseEventTsOrigin(mapPoint, brushColours, dispatchFn, eventDc, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
        elif self.toolState == self.TS_SELECT:
            dirty = self._mouseEventTsSelect(mapPoint, brushColours, dispatchFn, eventDc, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
        elif self.toolState == self.TS_TARGET:
            dirty = self._mouseEventTsTarget(mapPoint, brushColours, dispatchFn, eventDc, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
        else:
            return False, dirty
        return True, dirty

    #
    # onSelectEvent(self, disp, dispatchFn, eventDc, isCursor, newTargetRect, selectRect, viewRect)
    def onSelectEvent(self, disp, dispatchFn, eventDc, isCursor, newTargetRect, selectRect, viewRect):
        pass

    # __init__(self, *args): initialisation method
    def __init__(self, *args):
        super().__init__(*args)
        self.lastAtPoint, self.srcRect, self.targetRect,    \
            self.toolSelectMap, self.toolState =            \
                None, None, None, None, self.TS_NONE

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
