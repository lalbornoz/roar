#!/usr/bin/env python3
#
# MiRCARTCanvas.py -- XXX
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

from MiRCARTCanvasJournal import MiRCARTCanvasJournal
from MiRCARTColours import MiRCARTColours
import wx

class MiRCARTCanvas(wx.Panel):
    """XXX"""
    parentFrame = None
    canvasPos = canvasSize = canvasWinSize = cellPos = cellSize = None
    canvasBitmap = canvasMap = canvasTools = None
    mircBg = mircFg = mircBrushes = mircPens = None
    canvasJournal = None

    # {{{ _drawPatch(self, patch, eventDc, tmpDc, atPoint): XXX
    def _drawPatch(self, patch, eventDc, tmpDc, atPoint):
        absPoint = self._relMapPointToAbsPoint((patch[0], patch[1]), atPoint)
        if patch[4] == " ":
            brushFg = self.mircBrushes[patch[3]]; brushBg = self.mircBrushes[patch[3]];
            pen = self.mircPens[patch[3]]
        else:
            brushFg = self.mircBrushes[patch[2]]; brushBg = self.mircBrushes[patch[3]];
            pen = self.mircPens[patch[2]]
        for dc in (eventDc, tmpDc):
            dc.SetBrush(brushFg); dc.SetBackground(brushBg); dc.SetPen(pen);
            dc.DrawRectangle(absPoint[0], absPoint[1], self.cellSize[0], self.cellSize[1])
    # }}}
    # {{{ _eventPointToMapPoint(self, eventPoint): XXX
    def _eventPointToMapPoint(self, eventPoint):
        rectX = eventPoint.x - (eventPoint.x % self.cellSize[0])
        rectY = eventPoint.y - (eventPoint.y % self.cellSize[1])
        mapX = int(rectX / self.cellSize[0] if rectX else 0)
        mapY = int(rectY / self.cellSize[1] if rectY else 0)
        return (mapX, mapY)
    # }}}
    # {{{ _getMapCell(self, absMapPoint): XXX
    def _getMapCell(self, absMapPoint):
        return self.canvasMap[absMapPoint[1]][absMapPoint[0]]
    # }}}
    # {{{ _relMapPointToAbsPoint(self, relMapPoint, atPoint): XXX
    def _relMapPointToAbsPoint(self, relMapPoint, atPoint):
        absX = (atPoint[0] + relMapPoint[0]) * self.cellSize[0]
        absY = (atPoint[1] + relMapPoint[1]) * self.cellSize[1]
        return (absX, absY)
    # }}}
    # {{{ _setMapCell(self, absMapPoint, colourFg, colourBg, char): XXX
    def _setMapCell(self, absMapPoint, colourFg, colourBg, char):
        self.canvasMap[absMapPoint[1]][absMapPoint[0]] = [colourFg, colourBg, char]
    # }}}
    # {{{ onClose(self, event): XXX
    def onClose(self, event):
        self.Destroy(); self.__del__();
    # }}}
    # {{{ onJournalUpdate(self, isTmp, absMapPoint, patch, eventDc, tmpDc, atPoint):
    def onJournalUpdate(self, isTmp, absMapPoint, patch, eventDc, tmpDc, atPoint):
        if eventDc == None:
            eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
        if tmpDc == None:
            tmpDc.SelectObject(self.canvasBitmap)
        if isTmp == True:
            self._drawPatch(patch, eventDc, tmpDc, atPoint)
        else:
            self._setMapCell(absMapPoint, *patch[2:5])
            self._drawPatch(patch, eventDc, tmpDc, atPoint)
            self.parentFrame.onCanvasUpdate()
    # }}}
    # {{{ onMouseEvent(self, event): XXX
    def onMouseEvent(self, event):
        eventObject = event.GetEventObject()
        eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
        tmpDc.SelectObject(self.canvasBitmap)
        eventPoint = event.GetLogicalPosition(eventDc)
        mapPoint = self._eventPointToMapPoint(eventPoint)
        for tool in self.canvasTools:
            mapPatches = tool.onMouseEvent(event, mapPoint, event.Dragging(),   \
                event.LeftIsDown(), event.RightIsDown())
            self.canvasJournal.merge(mapPatches, eventDc, tmpDc, mapPoint)
    # }}}
    # {{{ onPaint(self, event): XXX
    def onPaint(self, event):
        eventDc = wx.BufferedPaintDC(self, self.canvasBitmap)
    # }}}
    # {{{ redo(self): XXX
    def redo(self):
        return self.canvasJournal.redo()
    # }}}
    # {{{ undo(self): XXX
    def undo(self):
        return self.canvasJournal.undo()
    # }}}
    # {{{ __del__(self): destructor method
    def __del__(self):
        if self.canvasBitmap != None:
            self.canvasBitmap.Destroy(); self.canvasBitmap = None;
        for brush in self.mircBrushes or []:
            brush.Destroy()
        self.mircBrushes = None
        for pen in self.mircPens or []:
            pen.Destroy()
        self.mircPens = None
    # }}}

    #
    # _init__(self, parent, parentFrame, canvasPos, cellSize, canvasSize, canvasTools): initialisation method
    def __init__(self, parent, parentFrame, canvasPos, cellSize, canvasSize, canvasTools):
        self.parentFrame = parentFrame
        canvasWinSize = (cellSize[0] * canvasSize[0], cellSize[1] * canvasSize[1])
        super().__init__(parent, pos=canvasPos, size=canvasWinSize)
        self.canvasPos = canvasPos; self.canvasSize = canvasSize; self.canvasWinSize = canvasWinSize;
        self.cellPos = (0, 0); self.cellSize = cellSize;

        self.canvasBitmap = wx.Bitmap(canvasWinSize)
        self.canvasMap = [[[1, 1, " "] for x in range(canvasSize[0])] for y in range(canvasSize[1])]
        self.canvasTools = []
        for canvasTool in canvasTools:
            self.canvasTools.append(canvasTool(self))

        self.mircBg = 1; self.mircFg = 4;
        self.mircBrushes = [None for x in range(len(MiRCARTColours))]
        self.mircPens = [None for x in range(len(MiRCARTColours))]
        for mircColour in range(0, len(MiRCARTColours)):
            self.mircBrushes[mircColour] = wx.Brush(    \
                wx.Colour(MiRCARTColours[mircColour]), wx.BRUSHSTYLE_SOLID)
            self.mircPens[mircColour] = wx.Pen(         \
                wx.Colour(MiRCARTColours[mircColour]), 1)

        self.canvasJournal = MiRCARTCanvasJournal(self)

        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseEvent)
        self.Bind(wx.EVT_MOTION, self.onMouseEvent)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onMouseEvent)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
