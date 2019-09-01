#!/usr/bin/env python3
#
# MiRCARTToolSelect.py -- XXX
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from MiRCARTTool import MiRCARTTool

class MiRCARTToolSelect(MiRCARTTool):
    """XXX"""
    toolColours = toolRect = toolState = None
    toolLastAtPoint = None
    toolSelectMap = None
    srcRect = None

    TS_NONE     = 0
    TS_ORIGIN   = 1
    TS_TARGET   = 2

    # {{{ _drawSelectRect(self, rect, dispatchFn, eventDc): XXX
    def _drawSelectRect(self, rect, dispatchFn, eventDc):
        rectFrame = [                           \
                [rect[0][0]-1, rect[0][1]-1],   \
                [rect[1][0]+1, rect[1][1]+1]]
        if rectFrame[0][0] > rectFrame[1][0]:
            rectFrame[0][0], rectFrame[1][0] =  \
                rectFrame[1][0], rectFrame[0][0]
        if rectFrame[0][1] > rectFrame[1][1]:
            rectFrame[0][1], rectFrame[1][1] =  \
                rectFrame[1][1], rectFrame[0][1]
        curColours = [0, 0]
        for rectX in range(rectFrame[0][0], rectFrame[1][0]+1):
            if curColours == [0, 0]:
                curColours = [1, 1]
            else:
                curColours = [0, 0]
            dispatchFn(eventDc, True,           \
                    [rectX, rectFrame[0][1], *curColours, 0, " "])
            dispatchFn(eventDc, True,           \
                    [rectX, rectFrame[1][1], *curColours, 0, " "])
        for rectY in range(rectFrame[0][1], rectFrame[1][1]+1):
            if curColours == [0, 0]:
                curColours = [1, 1]
            else:
                curColours = [0, 0]
            dispatchFn(eventDc, True,           \
                    [rectFrame[0][0], rectY, *curColours, 0, " "])
            dispatchFn(eventDc, True,           \
                    [rectFrame[1][0], rectY, *curColours, 0, " "])
    # }}}

    #
    # onSelectEvent(self, event, atPoint, selectRect, brushColours, brushSize, isLeftDown, isRightDown, dispatchFn, eventDc): XXX
    def onSelectEvent(self, event, atPoint, selectRect, brushColours, brushSize, isLeftDown, isRightDown, dispatchFn, eventDc):
        pass

    #
    # onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc): XXX
    def onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc):
        if self.toolState == self.TS_NONE:
            if isLeftDown or isRightDown:
                self.toolColours = [0, 1]
                self.toolRect = [list(atPoint), []]
                self.toolState = self.TS_ORIGIN
            else:
                dispatchFn(eventDc, True,                                       \
                    [*atPoint, *brushColours, 0, " "])
        elif self.toolState == self.TS_ORIGIN:
            self.toolRect[1] = list(atPoint)
            if isLeftDown or isRightDown:
                if self.toolRect[0][0] > self.toolRect[1][0]:
                    self.toolRect[0][0], self.toolRect[1][0] =                  \
                        self.toolRect[1][0], self.toolRect[0][0]
                if self.toolRect[0][1] > self.toolRect[1][1]:
                    self.toolRect[0][1], self.toolRect[1][1] =                  \
                        self.toolRect[1][1], self.toolRect[0][1]
                self.srcRect = self.toolRect[0]
                self.toolLastAtPoint = list(atPoint)
                self.toolState = self.TS_TARGET
                self.toolSelectMap = []
                for numRow in range((self.toolRect[1][1] - self.toolRect[0][1]) + 1):
                    self.toolSelectMap.append([])
                    for numCol in range((self.toolRect[1][0] - self.toolRect[0][0]) + 1):
                        rectY = self.toolRect[0][1] + numRow
                        rectX = self.toolRect[0][0] + numCol
                        self.toolSelectMap[numRow].append(                      \
                            self.parentCanvas.canvasMap[rectY][rectX])
            self._drawSelectRect(self.toolRect, dispatchFn, eventDc)
        elif self.toolState == self.TS_TARGET:
            if isRightDown:
                self.onSelectEvent(event, atPoint, self.toolRect,               \
                    brushColours, brushSize, isLeftDown, isRightDown,           \
                    dispatchFn, eventDc)
                self.toolColours = None
                self.toolRect = None
                self.toolState = self.TS_NONE
            else:
                self.onSelectEvent(event, atPoint, self.toolRect,               \
                    brushColours, brushSize, isLeftDown, isRightDown,           \
                    dispatchFn, eventDc)

    # __init__(self, *args): initialisation method
    def __init__(self, *args):
        super().__init__(*args)
        self.toolColours = None
        self.toolRect = None
        self.toolState = self.TS_NONE
        self.toolLastAtPoint = None
        self.toolSelectMap = None

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
