#!/usr/bin/env python3
#
# MiRCARTToolSelectMove.py -- XXX
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from MiRCARTToolSelect import MiRCARTToolSelect

class MiRCARTToolSelectMove(MiRCARTToolSelect):
    """XXX"""
    name = "Move selection"

    #
    # onSelectEvent(self, event, atPoint, selectRect, brushColours, brushSize, isLeftDown, isRightDown, dispatchFn, eventDc): XXX
    def onSelectEvent(self, event, atPoint, selectRect, brushColours, brushSize, isLeftDown, isRightDown, dispatchFn, eventDc):
        if isLeftDown:
            atPoint = list(atPoint)
            disp = [atPoint[0]-self.toolLastAtPoint[0],                     \
                    atPoint[1]-self.toolLastAtPoint[1]]
            self.toolLastAtPoint = atPoint
            newToolRect = [                                                 \
                    [selectRect[0][0]+disp[0], selectRect[0][1]+disp[1]],   \
                    [selectRect[1][0]+disp[0], selectRect[1][1]+disp[1]]]
            isCursor = True
        elif isRightDown:
            disp = [0, 0]
            newToolRect = selectRect.copy()
            isCursor = False
        else:
            disp = [0, 0]
            newToolRect = selectRect.copy()
            isCursor = True
        for numRow in range(len(self.toolSelectMap)):
            for numCol in range(len(self.toolSelectMap[numRow])):
                dispatchFn(eventDc, isCursor, [self.srcRect[0] + numCol,    \
                    self.srcRect[1] + numRow, 1, 1, 0, " "])
        for numRow in range(len(self.toolSelectMap)):
            for numCol in range(len(self.toolSelectMap[numRow])):
                cellOld = self.toolSelectMap[numRow][numCol]
                rectY = selectRect[0][1] + numRow
                rectX = selectRect[0][0] + numCol
                dispatchFn(eventDc, isCursor, [rectX+disp[0], rectY+disp[1], *cellOld])
        self._drawSelectRect(newToolRect, dispatchFn, eventDc)
        self.toolRect = newToolRect

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
