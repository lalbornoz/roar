#!/usr/bin/env python3
#
# GuiCanvasWxBackend.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiCanvasColours import Colours
import math, wx

class GuiCanvasWxBackend():
    # {{{ _drawBrushPatch(self, eventDc, patch, point)
    def _drawBrushPatch(self, eventDc, patch, point):
        absPoint = self._xlatePoint(point)
        brushBg, brushFg, pen = self._getBrushPatchColours(patch)
        self._setBrushDc(brushBg, brushFg, eventDc, pen)
        eventDc.DrawRectangle(*absPoint, *self.cellSize)
    # }}}
    # {{{ _drawCharPatch(self, eventDc, patch, point)
    def _drawCharPatch(self, eventDc, patch, point):
        absPoint, fontBitmap = self._xlatePoint(point), wx.Bitmap(*self.cellSize)
        brushBg, brushFg, pen = self._getCharPatchColours(patch)
        fontDc = wx.MemoryDC(); fontDc.SelectObject(fontBitmap);
        fontDc.SetTextForeground(wx.Colour(Colours[patch[0]][:4]))
        fontDc.SetTextBackground(wx.Colour(Colours[patch[1]][:4]))
        fontDc.SetBrush(brushBg); fontDc.SetBackground(brushBg); fontDc.SetPen(pen);
        fontDc.SetFont(self._font)
        fontDc.DrawRectangle(0, 0, *self.cellSize); fontDc.DrawText(patch[3], 0, 0);
        eventDc.Blit(*absPoint, *self.cellSize, fontDc, 0, 0)
    # }}}
    # {{{ _finiBrushesAndPens(self)
    def _finiBrushesAndPens(self):
        [brush.Destroy() for brush in self._brushes or []]
        [pen.Destroy() for pen in self._pens or []]
        self._brushes, self._lastBrushBg, self._lastBrushFg, self._lastPen, self._pens = None, None, None, None, None
    # }}}
    # {{{ _getBrushPatchColours(self, patch)
    def _getBrushPatchColours(self, patch):
        if (patch[0] != -1) and (patch[1] != -1):
            brushBg, brushFg, pen = self._brushes[patch[0]], self._brushes[patch[1]], self._pens[patch[1]]
        elif (patch[0] == -1) and (patch[1] == -1):
            brushBg, brushFg, pen = self._brushes[1], self._brushes[1], self._pens[1]
        elif patch[0] == -1:
            brushBg, brushFg, pen = self._brushes[patch[1]], self._brushes[patch[1]], self._pens[patch[1]]
        elif patch[1] == -1:
            brushBg, brushFg, pen = self._brushes[1], self._brushes[patch[0]], self._pens[1]
        return (brushBg, brushFg, pen)
    # }}}
    # {{{ _getCharPatchColours(self, patch)
    def _getCharPatchColours(self, patch):
        if (patch[0] != -1) and (patch[1] != -1):
            brushBg, brushFg, pen = self._brushes[patch[1]], self._brushes[patch[0]], self._pens[patch[1]]
        elif (patch[0] == -1) and (patch[1] == -1):
            brushBg, brushFg, pen = self._brushes[1], self._brushes[1], self._pens[1]
        elif patch[0] == -1:
            brushBg, brushFg, pen = self._brushes[patch[1]], self._brushes[patch[1]], self._pens[patch[1]]
        elif patch[1] == -1:
            brushBg, brushFg, pen = self._brushes[1], self._brushes[patch[0]], self._pens[1]
        return (brushBg, brushFg, pen)
    # }}}
    # {{{ _initBrushesAndPens(self)
    def _initBrushesAndPens(self):
        self._brushes, self._pens = [None for x in range(len(Colours))], [None for x in range(len(Colours))]
        for mircColour in range(len(Colours)):
            self._brushes[mircColour] = wx.Brush(wx.Colour(Colours[mircColour][:4]), wx.BRUSHSTYLE_SOLID)
            self._pens[mircColour] = wx.Pen(wx.Colour(Colours[mircColour][:4]), 1)
        self._lastBrushBg, self._lastBrushFg, self._lastPen = None, None, None
    # }}}
    # {{{ _setBrushDc(self, brushBg, brushFg, dc, pen)
    def _setBrushDc(self, brushBg, brushFg, dc, pen):
        if self._lastBrushBg != brushBg:
            dc.SetBackground(brushBg); self._lastBrushBg = brushBg;
        if self._lastBrushFg != brushFg:
            dc.SetBrush(brushFg); self._lastBrushFg = brushFg;
        if self._lastPen != pen:
            dc.SetPen(pen); self._lastPen = pen;
    # }}}
    # {{{ _xlatePoint(self, point)
    def _xlatePoint(self, point):
        return [a * b for a, b in zip(point, self.cellSize)]
    # }}}

    # {{{ drawCursorMaskWithJournal(self, canvasJournal, eventDc, viewRect)
    def drawCursorMaskWithJournal(self, canvasJournal, eventDc, viewRect):
        [self.drawPatch(eventDc, patch, viewRect) for patch in canvasJournal.popCursor()]
    # }}}
    # {{{ drawPatch(self, eventDc, patch, viewRect)
    def drawPatch(self, eventDc, patch, viewRect):
        point = [m - n for m, n in zip(patch[:2], viewRect)]
        if [(c >= 0) and (c < s) for c, s in zip(point, self.canvasSize)] == [True, True]:
            if patch[5] == " ":
                self._drawBrushPatch(eventDc, patch[2:], point)
            else:
                self._drawCharPatch(eventDc, patch[2:], point)
            return True
        else:
            return False
    # }}}
    # {{{ getDeviceContext(self, parentWindow, viewRect)
    def getDeviceContext(self, parentWindow, viewRect):
        if viewRect == (0, 0):
            eventDc = wx.BufferedDC(wx.ClientDC(parentWindow), self.canvasBitmap)
        else:
            eventDc = wx.ClientDC(parentWindow)
        self._lastBrushBg, self._lastBrushFg, self._lastPen = None, None, None
        return eventDc
    # }}}
    # {{{ onPanelPaintEvent(self, canvasSize, cellSize, clientSize, panelWindow, viewRect)
    def onPanelPaintEvent(self, canvasSize, cellSize, clientSize, panelWindow, viewRect):
        if self.canvasBitmap != None:
            if viewRect == (0, 0):
                eventDc = wx.BufferedPaintDC(panelWindow, self.canvasBitmap)
            else:
                canvasSize = [a - b for a, b in zip(canvasSize, viewRect)]
                clientSize = [math.ceil(m / n) for m, n in zip(clientSize, cellSize)]
                viewSize = [min(m, n) for m, n in zip(canvasSize, clientSize)]
                viewSize = [m * n for m, n in zip(cellSize, viewSize)]
                canvasDc = wx.MemoryDC(); canvasDc.SelectObject(self.canvasBitmap);
                viewDc = wx.MemoryDC(); viewBitmap = wx.Bitmap(viewSize); viewDc.SelectObject(viewBitmap);
                viewDc.Blit(0, 0, *viewSize, canvasDc, *[m * n for m, n in zip(cellSize, viewRect)])
                canvasDc.SelectObject(wx.NullBitmap); viewDc.SelectObject(wx.NullBitmap);
                eventDc = wx.BufferedPaintDC(panelWindow, viewBitmap)
    # }}}
    # {{{ resize(self, canvasSize, cellSize):
    def resize(self, canvasSize, cellSize):
        winSize = [a * b for a, b in zip(canvasSize, cellSize)]
        if self.canvasBitmap == None:
            self.canvasBitmap = wx.Bitmap(winSize)
        else:
            oldDc = wx.MemoryDC(); oldDc.SelectObject(self.canvasBitmap);
            newDc = wx.MemoryDC(); newBitmap = wx.Bitmap(winSize); newDc.SelectObject(newBitmap);
            newDc.Blit(0, 0, *self.canvasBitmap.GetSize(), oldDc, 0, 0)
            oldDc.SelectObject(wx.NullBitmap)
            self.canvasBitmap.Destroy(); self.canvasBitmap = newBitmap;
        self.canvasSize, self.cellSize = canvasSize, cellSize
        self._font = wx.Font(8, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    # }}}
    # {{{ xlateEventPoint(self, event, eventDc, viewRect)
    def xlateEventPoint(self, event, eventDc, viewRect):
        eventPoint = event.GetLogicalPosition(eventDc)
        rectX, rectY = eventPoint.x - (eventPoint.x % self.cellSize[0]), eventPoint.y - (eventPoint.y % self.cellSize[1])
        mapX, mapY = int(rectX / self.cellSize[0] if rectX else 0), int(rectY / self.cellSize[1] if rectY else 0)
        return [m + n for m, n in zip((mapX, mapY), viewRect)]
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
        self._initBrushesAndPens(); self.resize(canvasSize, cellSize);

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
