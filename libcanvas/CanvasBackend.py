#!/usr/bin/env python3
#
# CanvasBackend.py -- XXX
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Colours import Colours
import wx

class CanvasBackend():
    """XXX"""

    # {{{ _drawBrushPatch(self, eventDc, patch): XXX
    def _drawBrushPatch(self, eventDc, patch):
        absPoint = self._xlatePoint(patch)
        brushFg = self._brushes[patch[3]]
        brushBg = self._brushes[patch[2]]
        pen = self._pens[patch[3]]
        self._setBrushDc(brushBg, brushFg, eventDc, pen)
        eventDc.DrawRectangle(*absPoint, *self.cellSize)
    # }}}
    # {{{ _drawCharPatch(self, eventDc, patch): XXX
    def _drawCharPatch(self, eventDc, patch):
        absPoint = self._xlatePoint(patch)
        brushFg = self._brushes[patch[2]]
        brushBg = self._brushes[patch[3]]
        pen = self._pens[patch[3]]
        fontBitmap = wx.Bitmap(*self.cellSize)
        fontDc = wx.MemoryDC(); fontDc.SelectObject(fontBitmap);
        fontDc.SetTextForeground(wx.Colour(Colours[patch[2]][0:4]))
        fontDc.SetTextBackground(wx.Colour(Colours[patch[3]][0:4]))
        fontDc.SetBrush(brushBg); fontDc.SetBackground(brushBg); fontDc.SetPen(pen);
        fontDc.SetFont(self._font)
        fontDc.DrawRectangle(0, 0, *self.cellSize)
        fontDc.DrawText(patch[5], 0, 0)
        eventDc.Blit(*absPoint, *self.cellSize, fontDc, 0, 0)
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
        self._brushes = [None for x in range(len(Colours))]
        self._pens = [None for x in range(len(Colours))]
        for mircColour in range(len(Colours)):
            self._brushes[mircColour] = wx.Brush(    \
                wx.Colour(Colours[mircColour][0:4]), wx.BRUSHSTYLE_SOLID)
            self._pens[mircColour] = wx.Pen(         \
                wx.Colour(Colours[mircColour][0:4]), 1)
        self._lastBrushBg = self._lastBrushFg = self._lastPen = None;
    # }}}
    # {{{ _setBrushDc(self, brushBg, brushFg, dc, pen): XXX
    def _setBrushDc(self, brushBg, brushFg, dc, pen):
        if self._lastBrushBg != brushBg:
            dc.SetBackground(brushBg)
            self._lastBrushBg = brushBg
        if self._lastBrushFg != brushFg:
            dc.SetBrush(brushFg)
            self._lastBrushFg = brushFg
        if self._lastPen != pen:
            dc.SetPen(pen)
            self._lastPen = pen
    # }}}
    # {{{ _xlatePoint(self, patch): XXX
    def _xlatePoint(self, patch):
        return [a * b for a, b in zip(patch[0:2], self.cellSize)]
    # }}}

    # {{{ drawCursorMaskWithJournal(self, canvasJournal, eventDc): XXX
    def drawCursorMaskWithJournal(self, canvasJournal, eventDc):
        for patch in canvasJournal.popCursor():
            self.drawPatch(eventDc, patch)
    # }}}
    # {{{ drawPatch(self, eventDc, patch): XXX
    def drawPatch(self, eventDc, patch):
        if  patch[0] < self.canvasSize[0]    \
        and patch[0] >= 0                    \
        and patch[1] < self.canvasSize[1]    \
        and patch[1] >= 0:
            if patch[5] == " ":
                self._drawBrushPatch(eventDc, patch)
            else:
                self._drawCharPatch(eventDc, patch)
            return True
        else:
            return False
    # }}}
    # {{{ getDeviceContext(self, parentWindow): XXX
    def getDeviceContext(self, parentWindow):
        eventDc = wx.BufferedDC(wx.ClientDC(parentWindow), self.canvasBitmap)
        self._lastBrushBg = self._lastBrushFg = self._lastPen = None;
        return eventDc
    # }}}
    # {{{ onPanelPaintEvent(self, panelWindow, panelEvent): XXX
    def onPanelPaintEvent(self, panelWindow, panelEvent):
        if self.canvasBitmap != None:
            eventDc = wx.BufferedPaintDC(panelWindow, self.canvasBitmap)
    # }}}
    # {{{ reset(self, canvasSize, cellSize):
    def reset(self, canvasSize, cellSize):
        self.resize(canvasSize, cellSize)
    # }}}
    # {{{ resize(self, canvasSize, cellSize):
    def resize(self, canvasSize, cellSize):
        winSize = [a * b for a, b in zip(canvasSize, cellSize)]
        if self.canvasBitmap == None:
            self.canvasBitmap = wx.Bitmap(winSize)
        else:
            oldDc = wx.MemoryDC()
            oldDc.SelectObject(self.canvasBitmap)
            newDc = wx.MemoryDC()
            newBitmap = wx.Bitmap(winSize)
            newDc.SelectObject(newBitmap)
            newDc.Blit(0, 0, *self.canvasBitmap.GetSize(), oldDc, 0, 0)
            oldDc.SelectObject(wx.NullBitmap)
            self.canvasBitmap.Destroy(); self.canvasBitmap = newBitmap;
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
    # __init__(self, canvasSize, cellSize): initialisation method
    def __init__(self, canvasSize, cellSize):
        self._brushes, self._font, self._lastBrush, self._lastPen, self._pens = None, None, None, None, None
        self.canvasBitmap, self.cellSize = None, None
        self._initBrushesAndPens()
        self.reset(canvasSize, cellSize)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
