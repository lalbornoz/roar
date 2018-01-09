#!/usr/bin/env python3
#
# MiRCARTCanvasBackend.py -- XXX
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

from MiRCARTColours import MiRCARTColours
import wx

class MiRCARTCanvasBackend():
    """XXX"""
    _font = _brushes = _pens = None
    _lastBrush = _lastPen = None
    canvasBitmap = cellSize = None

    # {{{ _drawBrushPatch(self, eventDc, patch, tmpDc): XXX
    def _drawBrushPatch(self, eventDc, patch, tmpDc):
        absPoint = self._xlatePoint(patch[0])
        brushFg = self._brushes[patch[1][1]]
        brushBg = self._brushes[patch[1][0]]
        pen = self._pens[patch[1][1]]
        self._setBrushDc(brushBg, brushFg, (eventDc, tmpDc), pen)
        eventDc.DrawRectangle(*absPoint, *self.cellSize)
        tmpDc.DrawRectangle(*absPoint, *self.cellSize)
    # }}}
    # {{{ _drawCharPatch(self, eventDc, patch, tmpDc): XXX
    def _drawCharPatch(self, eventDc, patch, tmpDc):
        absPoint = self._xlatePoint(patch[0])
        brushFg = self._brushes[patch[1][0]]
        brushBg = self._brushes[patch[1][1]]
        pen = self._pens[patch[1][1]]
        for dc in (eventDc, tmpDc):
            fontBitmap = wx.Bitmap(*self.cellSize)
            fontDc = wx.MemoryDC(); fontDc.SelectObject(fontBitmap);
            fontDc.SetTextForeground(wx.Colour(MiRCARTColours[patch[1][0]][0:4]))
            fontDc.SetTextBackground(wx.Colour(MiRCARTColours[patch[1][1]][0:4]))
            fontDc.SetBrush(brushBg); fontDc.SetBackground(brushBg); fontDc.SetPen(pen);
            fontDc.SetFont(self._font)
            fontDc.DrawRectangle(0, 0, *self.cellSize)
            fontDc.DrawText(patch[3], 0, 0)
            dc.Blit(*absPoint, *self.cellSize, fontDc, 0, 0)
    # }}}
    # {{{ _finiBrushesAndPens(self): XXX
    def _finiBrushesAndPens(self):
        for brush in self._brushes or []:
            brush.Destroy()
        self._brushes = None
        for pen in self._pens or []:
            pen.Destroy()
        self._pens = None
        self._lastBrushBg = self._lastBrushFg = self._lastPen = None;
    # }}}
    # {{{ _initBrushesAndPens(self): XXX
    def _initBrushesAndPens(self):
        self._brushes = [None for x in range(len(MiRCARTColours))]
        self._pens = [None for x in range(len(MiRCARTColours))]
        for mircColour in range(len(MiRCARTColours)):
            self._brushes[mircColour] = wx.Brush(    \
                wx.Colour(MiRCARTColours[mircColour][0:4]), wx.BRUSHSTYLE_SOLID)
            self._pens[mircColour] = wx.Pen(         \
                wx.Colour(MiRCARTColours[mircColour][0:4]), 1)
        self._lastBrushBg = self._lastBrushFg = self._lastPen = None;
    # }}}
    # {{{ _setBrushDc(self, brushBg, brushFg, dcList, pen): XXX
    def _setBrushDc(self, brushBg, brushFg, dcList, pen):
        if self._lastBrushBg != brushBg:
            for dc in dcList:
                dc.SetBackground(brushBg)
            self._lastBrushBg = brushBg
        if self._lastBrushFg != brushFg:
            for dc in dcList:
                dc.SetBrush(brushFg)
            self._lastBrushFg = brushFg
        if self._lastPen != pen:
            for dc in dcList:
                dc.SetPen(pen)
            self._lastPen = pen
    # }}}
    # {{{ _xlatePoint(self, relMapPoint): XXX
    def _xlatePoint(self, relMapPoint):
        return [a*b for a,b in zip(relMapPoint, self.cellSize)]
    # }}}

    # {{{ drawPatch(self, eventDc, patch, tmpDc): XXX
    def drawPatch(self, eventDc, patch, tmpDc):
        if  patch[0][0] < self.canvasSize[0]    \
        and patch[0][1] < self.canvasSize[1]:
            if patch[3] == " ":
                self._drawBrushPatch(eventDc, patch, tmpDc)
            else:
                self._drawCharPatch(eventDc, patch, tmpDc)
            return True
        else:
            return False
    # }}}
    # {{{ drawCursorMaskWithJournal(self, canvasJournal, eventDc, tmpDc): XXX
    def drawCursorMaskWithJournal(self, canvasJournal, eventDc, tmpDc):
        for patch in canvasJournal.popCursor():
            self.drawPatch(eventDc, patch, tmpDc)
    # }}}
    # {{{ getDeviceContexts(self, parentWindow): XXX
    def getDeviceContexts(self, parentWindow):
        eventDc = wx.ClientDC(parentWindow); tmpDc = wx.MemoryDC();
        tmpDc.SelectObject(self.canvasBitmap)
        self._lastBrushBg = self._lastBrushFg = self._lastPen = None;
        return (eventDc, tmpDc)
    # }}}
    # {{{ reset(self, canvasSize, cellSize):
    def reset(self, canvasSize, cellSize):
        self.resize(canvasSize, cellSize)
    # }}}
    # {{{ resize(self, canvasSize, cellSize):
    def resize(self, canvasSize, cellSize):
        winSize = [a*b for a,b in zip(canvasSize, cellSize)]
        if self.canvasBitmap == None:
            self.canvasBitmap = wx.Bitmap(winSize)
        else:
            oldDc = wx.MemoryDC()
            oldDc.SelectObject(self.canvasBitmap)
            newDc = wx.MemoryDC()
            newBitmap = wx.Bitmap(winSize)
            newDc.SelectObject(newBitmap)
            newDc.Blit(0, 0, *self.canvasBitmap.GetSize(), oldDc, 0, 0)
            self.canvasBitmap = newBitmap
        self.canvasSize = canvasSize; self.cellSize = cellSize;
        self._font = wx.Font(       \
            8,                      \
            wx.FONTFAMILY_TELETYPE, \
            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    # }}}
    # {{{ xlateEventPoint(self, event, eventDc): XXX
    def xlateEventPoint(self, event, eventDc):
        eventPoint = event.GetLogicalPosition(eventDc)
        rectX = eventPoint.x - (eventPoint.x % self.cellSize[0])
        rectY = eventPoint.y - (eventPoint.y % self.cellSize[1])
        mapX = int(rectX / self.cellSize[0] if rectX else 0)
        mapY = int(rectY / self.cellSize[1] if rectY else 0)
        return (mapX, mapY)
    # }}}

    # {{{ __del__(self): destructor method
    def __del__(self):
        if self.canvasBitmap != None:
            self.canvasBitmap.Destroy(); self.canvasBitmap = None;
        self._finiBrushesAndPens()
    # }}}

    #
    # _init__(self, canvasSize, cellSize): initialisation method
    def __init__(self, canvasSize, cellSize):
        self._initBrushesAndPens()
        self.reset(canvasSize, cellSize)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
