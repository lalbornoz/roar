#!/usr/bin/env python3
#
# ToolSelectClone.py -- XXX
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from ToolSelect import ToolSelect

class ToolSelectClone(ToolSelect):
    """XXX"""
    name = "Clone selection"

    #
    # onSelectEvent(self, disp, dispatchFn, eventDc, isCursor, newToolRect, selectRect): XXX
    def onSelectEvent(self, disp, dispatchFn, eventDc, isCursor, newToolRect, selectRect):
        for numRow in range(len(self.toolSelectMap)):
            for numCol in range(len(self.toolSelectMap[numRow])):
                cellOld = self.toolSelectMap[numRow][numCol]
                rectX, rectY = selectRect[0][0] + numCol, selectRect[0][1] + numRow
                dispatchFn(eventDc, isCursor, [rectX + disp[0], rectY + disp[1], *cellOld])

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
