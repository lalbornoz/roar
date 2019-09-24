#!/usr/bin/env python3
#
# ToolPickColour.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool

class ToolPickColour(Tool):
    name = "Pick colour"

    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        if  (mapPoint[0] < canvas.size[0])  \
        and (mapPoint[1] < canvas.size[1]):
            if mouseLeftDown:
                if canvas.map[mapPoint[1]][mapPoint[0]][3] == " ":
                    brushColours[0] = canvas.map[mapPoint[1]][mapPoint[0]][1]
                else:
                    brushColours[0] = canvas.map[mapPoint[1]][mapPoint[0]][0]
            elif mouseRightDown:
                brushColours[1] = canvas.map[mapPoint[1]][mapPoint[0]][1]
        dispatchFn(eventDc, True, [*mapPoint, *brushColours, 0, "░"])
        return True, False

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
