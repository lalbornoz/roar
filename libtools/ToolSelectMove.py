#!/usr/bin/env python3
#
# ToolSelectMove.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from ToolSelect import ToolSelect

class ToolSelectMove(ToolSelect):
    name = "Move selection"

    #
    # onSelectEvent(self, disp, dispatchFn, eventDc, isCursor, newToolRect, selectRect, viewRect)
    def onSelectEvent(self, disp, dispatchFn, eventDc, isCursor, newToolRect, selectRect, viewRect):
        dirty = False
        for numRow in range(self.srcRect[0][1], self.srcRect[1][1]):
            for numCol in range(self.srcRect[0][0], self.srcRect[1][0]):
                if  ((numCol < selectRect[0][0]) or (numCol > selectRect[1][0]))    \
                or  ((numRow < selectRect[0][1]) or (numRow > selectRect[1][1])):
                    dirty = False if isCursor else True
                    dispatchFn(eventDc, isCursor, [numCol, numRow, 1, 1, 0, " "], viewRect)
        for numRow in range(len(self.toolSelectMap)):
            for numCol in range(len(self.toolSelectMap[numRow])):
                cellOld = self.toolSelectMap[numRow][numCol]
                rectX, rectY = selectRect[0][0] + numCol, selectRect[0][1] + numRow
                dirty = False if isCursor else True
                dispatchFn(eventDc, isCursor, [rectX + disp[0], rectY + disp[1], *cellOld], viewRect)
        return dirty

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
