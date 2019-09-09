#!/usr/bin/env python3
#
# ToolSelectClone.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from ToolSelect import ToolSelect

class ToolSelectClone(ToolSelect):
    name = "Clone selection"

    #
    # onSelectEvent(self, disp, dispatchFn, eventDc, isCursor, newToolRect, selectRect, viewRect)
    def onSelectEvent(self, disp, dispatchFn, eventDc, isCursor, newToolRect, selectRect, viewRect):
        dirty = False
        for numRow in range(len(self.toolSelectMap)):
            for numCol in range(len(self.toolSelectMap[numRow])):
                cellOld = self.toolSelectMap[numRow][numCol]
                rectX, rectY = selectRect[0][0] + numCol, selectRect[0][1] + numRow
                dirty = False if isCursor else True
                dispatchFn(eventDc, isCursor, [rectX + disp[0], rectY + disp[1], *cellOld], viewRect)
        return dirty

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
