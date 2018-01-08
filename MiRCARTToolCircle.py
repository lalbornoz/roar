#!/usr/bin/env python3
#
# MiRCARTToolCircle.py -- XXX
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

class MiRCARTToolCircle(MiRCARTTool):
    """XXX"""

    #
    # onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown): XXX
    def onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown):
        brushColours = brushColours.copy()
        if isLeftDown:
            brushColours[1] = brushColours[0]
        elif isRightDown:
            brushColours[0] = brushColours[1]
        else:
            brushColours[1] = brushColours[0]
        brushPatches = []
        _brushSize = brushSize[0]*2
        originPoint = (_brushSize/2, _brushSize/2)
        radius = _brushSize
        for brushY in range(-radius, radius + 1):
            for brushX in range(-radius, radius + 1):
                if ((brushX**2)+(brushY**2) < (((radius**2)+radius)*0.8)):
                    brushPatches.append([                           \
                        [atPoint[0] + int(originPoint[0]+brushX),   \
                         atPoint[1] + int(originPoint[1]+brushY)],  \
                        brushColours, 0, " "])
        if isLeftDown or isRightDown:
            return [[False, brushPatches], [True, brushPatches]]
        else: 
            return [[True, brushPatches]]

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
