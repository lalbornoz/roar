#!/usr/bin/env python3
#
# MiRCARTToolRect.py -- XXX
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

class MiRCARTToolRect(MiRCARTTool):
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
        brushSize = brushSize.copy()
        if brushSize[0] > 1:
            brushSize[0] *= 2
        brushPatches = []
        for brushRow in range(brushSize[1]):
            for brushCol in range(brushSize[0]):
                brushPatches.append([[      \
                    atPoint[0] + brushCol,  \
                    atPoint[1] + brushRow], \
                    brushColours, 0, " "])
        if isLeftDown or isRightDown:
            return [[False, brushPatches], [True, brushPatches]]
        else: 
            return [[True, brushPatches]]

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
