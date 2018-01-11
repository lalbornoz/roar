#!/usr/bin/env python3
#
# MiRCARTToolFill.py -- XXX
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from MiRCARTTool import MiRCARTTool

class MiRCARTToolFill(MiRCARTTool):
    """XXX"""
    name = "Fill"

    #
    # onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc): XXX
    def onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc):
        pointStack = [list(atPoint)]
        testColour = self.parentCanvas.canvasMap[atPoint[1]][atPoint[0]][0][1]
        if isLeftDown or isRightDown:
            if isRightDown:
                brushColours = [brushColours[1], brushColours[0]]
            while len(pointStack) > 0:
                point = pointStack.pop()
                pointCell = self.parentCanvas.canvasMap[point[1]][point[0]]
                if pointCell[0][1] == testColour:
                    dispatchFn(eventDc, False, [point.copy(),   \
                        [brushColours[0], brushColours[0]], 0, " "])
                    if point[0] > 0:
                        pointStack.append([point[0] - 1, point[1]])
                    if point[0] < (self.parentCanvas.canvasSize[0] - 1):
                        pointStack.append([point[0] + 1, point[1]])
                    if point[1] > 0:
                        pointStack.append([point[0], point[1] - 1])
                    if point[1] < (self.parentCanvas.canvasSize[1] - 1):
                        pointStack.append([point[0], point[1] + 1])

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
