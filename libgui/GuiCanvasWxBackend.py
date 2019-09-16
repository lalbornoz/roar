#!/usr/bin/env python3
#
# GuiCanvasWxBackend.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from ctypes import *
from GuiCanvasColours import Colours
import math, os, platform, wx

class GuiBufferedDC(wx.MemoryDC):
    # {{{ __del__(self)
    def __del__(self):
        self.dc.Blit(0, 0, *self.viewSize, self, 0, 0)
        self.SelectObject(wx.NullBitmap)
    # }}}
    # {{{ __init__(self, backend, buffer, clientSize, dc, viewRect)
    def __init__(self, backend, buffer, clientSize, dc, viewRect):
        super().__init__()
        canvasSize = [a - b for a, b in zip(backend.canvasSize, viewRect)]
        clientSize = [math.ceil(m / n) for m, n in zip(clientSize, backend.cellSize)]
        viewRect = [m * n for m, n in zip(backend.cellSize, viewRect)]
        viewSize = [min(m, n) for m, n in zip(canvasSize, clientSize)]
        viewSize = [m * n for m, n in zip(backend.cellSize, viewSize)]
        self.SelectObject(buffer); self.SetDeviceOrigin(*viewRect);
        self.dc, self.viewRect, self.viewSize = dc, viewRect, viewSize
    # }}}

class GuiCanvasWxBackend():
    # {{{ arabicShapes{}
    arabicShapes = {
        u'\u0621': (u'\uFE80'),
        u'\u0622': (u'\uFE81', None, None, u'\uFE82'),
        u'\u0623': (u'\uFE83', None, None, u'\uFE84'),
        u'\u0624': (u'\uFE85', None, None, u'\uFE86'),
        u'\u0625': (u'\uFE87', None, None, u'\uFE88'),
        u'\u0626': (u'\uFE89', u'\uFE8B', u'\uFE8C', u'\uFE8A'),
        u'\u0627': (u'\uFE8D', None, None, u'\uFE8E'),
        u'\u0628': (u'\uFE8F', u'\uFE91', u'\uFE92', u'\uFE90'),
        u'\u0629': (u'\uFE93', None, None, u'\uFE94'),
        u'\u062A': (u'\uFE95', u'\uFE97', u'\uFE98', u'\uFE96'),
        u'\u062B': (u'\uFE99', u'\uFE9B', u'\uFE9C', u'\uFE9A'),
        u'\u062C': (u'\uFE9D', u'\uFE9F', u'\uFEA0', u'\uFE9E'),
        u'\u062D': (u'\uFEA1', u'\uFEA3', u'\uFEA4', u'\uFEA2'),
        u'\u062E': (u'\uFEA5', u'\uFEA7', u'\uFEA8', u'\uFEA6'),
        u'\u062F': (u'\uFEA9', None, None, u'\uFEAA'),
        u'\u0630': (u'\uFEAB', None, None, u'\uFEAC'),
        u'\u0631': (u'\uFEAD', None, None, u'\uFEAE'),
        u'\u0632': (u'\uFEAF', None, None, u'\uFEB0'),
        u'\u0633': (u'\uFEB1', u'\uFEB3', u'\uFEB4', u'\uFEB2'),
        u'\u0634': (u'\uFEB5', u'\uFEB7', u'\uFEB8', u'\uFEB6'),
        u'\u0635': (u'\uFEB9', u'\uFEBB', u'\uFEBC', u'\uFEBA'),
        u'\u0636': (u'\uFEBD', u'\uFEBF', u'\uFEC0', u'\uFEBE'),
        u'\u0637': (u'\uFEC1', u'\uFEC3', u'\uFEC4', u'\uFEC2'),
        u'\u0638': (u'\uFEC5', u'\uFEC7', u'\uFEC8', u'\uFEC6'),
        u'\u0639': (u'\uFEC9', u'\uFECB', u'\uFECC', u'\uFECA'),
        u'\u063A': (u'\uFECD', u'\uFECF', u'\uFED0', u'\uFECE'),
        u'\u0640': (u'\u0640', None, None, None),
        u'\u0641': (u'\uFED1', u'\uFED3', u'\uFED4', u'\uFED2'),
        u'\u0642': (u'\uFED5', u'\uFED7', u'\uFED8', u'\uFED6'),
        u'\u0643': (u'\uFED9', u'\uFEDB', u'\uFEDC', u'\uFEDA'),
        u'\u0644': (u'\uFEDD', u'\uFEDF', u'\uFEE0', u'\uFEDE'),
        u'\u0645': (u'\uFEE1', u'\uFEE3', u'\uFEE4', u'\uFEE2'),
        u'\u0646': (u'\uFEE5', u'\uFEE7', u'\uFEE8', u'\uFEE6'),
        u'\u0647': (u'\uFEE9', u'\uFEEB', u'\uFEEC', u'\uFEEA'),
        u'\u0648': (u'\uFEED', None, None, u'\uFEEE'),
        u'\u0649': (u'\uFEEF', None, None, u'\uFEF0'),
        u'\u064A': (u'\uFEF1', u'\uFEF3', u'\uFEF4', u'\uFEF2'),
    }
    # }}}
    # {{{ _CellState(): Cell state
    class _CellState():
        CS_NONE             = 0x00
        CS_BOLD             = 0x01
        CS_ITALIC           = 0x02
        CS_UNDERLINE        = 0x04
    # }}}

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
        fontDc = wx.MemoryDC(); fontDc.SelectObject(fontBitmap); fontDc.SetFont(self._font);
        fontDc.SetBackground(brushBg); fontDc.SetBrush(brushFg); fontDc.SetPen(pen);
        fontDc.SetTextForeground(wx.Colour(Colours[patch[0]][:4]))
        fontDc.SetTextBackground(wx.Colour(Colours[patch[1]][:4]))
        fontDc.DrawRectangle(0, 0, *self.cellSize)
        fontDc.SetPen(self._pens[patch[0]])
        if (patch[2] & self._CellState.CS_UNDERLINE)    \
        or (patch[3] == "_"):
            fontDc.DrawLine(0, self.cellSize[1] - 1, self.cellSize[0], self.cellSize[1] - 1)
        if patch[3] != "_":
            fontDc.DrawText(patch[3], 0, 0)
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
            brushBg, brushFg, pen = self._brushes[patch[1]], self._brushes[patch[1]], self._pens[patch[1]]
        elif (patch[0] == -1) and (patch[1] == -1):
            brushBg, brushFg, pen = self._brushAlpha, self._brushAlpha, self._penAlpha
        elif patch[0] == -1:
            brushBg, brushFg, pen = self._brushes[patch[1]], self._brushes[patch[1]], self._pens[patch[1]]
        elif patch[1] == -1:
            brushBg, brushFg, pen = self._brushAlpha, self._brushAlpha, self._penAlpha
        return (brushBg, brushFg, pen)
    # }}}
    # {{{ _getCharPatchColours(self, patch)
    def _getCharPatchColours(self, patch):
        if (patch[0] != -1) and (patch[1] != -1):
            brushBg, brushFg, pen = self._brushes[patch[1]], self._brushes[patch[1]], self._pens[patch[1]]
        elif (patch[0] == -1) and (patch[1] == -1):
            brushBg, brushFg, pen = self._brushAlpha, self._brushAlpha, self._penAlpha
        elif patch[0] == -1:
            brushBg, brushFg, pen = self._brushes[patch[1]], self._brushes[patch[1]], self._pens[patch[1]]
        elif patch[1] == -1:
            brushBg, brushFg, pen = self._brushAlpha, self._brushAlpha, self._penAlpha
        return (brushBg, brushFg, pen)
    # }}}
    # {{{ _initBrushesAndPens(self)
    def _initBrushesAndPens(self):
        self._brushes, self._pens = [None for x in range(len(Colours))], [None for x in range(len(Colours))]
        for mircColour in range(len(Colours)):
            self._brushes[mircColour] = wx.Brush(wx.Colour(Colours[mircColour][:4]), wx.BRUSHSTYLE_SOLID)
            self._pens[mircColour] = wx.Pen(wx.Colour(Colours[mircColour][:4]), 1)
        self._brushAlpha = wx.Brush(wx.Colour(Colours[14][:4]), wx.BRUSHSTYLE_SOLID)
        self._penAlpha = wx.Pen(wx.Colour(Colours[14][:4]), 1)
        self._lastBrushBg, self._lastBrushFg, self._lastPen = None, None, None
    # }}}
    # {{{ _reshapeArabic(self, canvas, eventDc, patch, point)
    def _reshapeArabic(self, canvas, eventDc, patch, point):
        lastCell = point[0]
        while True:
            if  ((lastCell + 1) >= (canvas.size[0] - 1))    \
            or  (not canvas.map[point[1]][lastCell + 1][3] in self.arabicShapes):
                break
            else:
                lastCell += 1
        connect = False
        for runX in range(lastCell, point[0], -1):
            runCell = list(canvas.map[point[1]][runX])
            if runX == lastCell:
                if self.arabicShapes[runCell[3]][1] != None:
                    runCell[3] = self.arabicShapes[runCell[3]][1]; connect = True;
                else:
                    runCell[3] = self.arabicShapes[runCell[3]][0]; connect = False;
            else:
                if connect and (self.arabicShapes[runCell[3]][2] != None):
                    runCell[3] = self.arabicShapes[runCell[3]][2]; connect = True;
                elif connect and (self.arabicShapes[runCell[3]][3] != None):
                    runCell[3] = self.arabicShapes[runCell[3]][3]; connect = False;
                elif not connect and (self.arabicShapes[runCell[3]][1] != None):
                    runCell[3] = self.arabicShapes[runCell[3]][1]; connect = True;
                else:
                    runCell[3] = self.arabicShapes[runCell[3]][0]; connect = False;
            self._drawCharPatch(eventDc, runCell, [runX, point[1]])
        runCell = list(patch[2:])
        if connect and (self.arabicShapes[patch[5]][3] != None):
            runCell[3] = self.arabicShapes[patch[5]][3]
        else:
            runCell[3] = self.arabicShapes[patch[5]][0]
        self._drawCharPatch(eventDc, runCell, [point[0], point[1]])
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

    # {{{ drawCursorMaskWithJournal(self, canvas, canvasJournal, eventDc)
    def drawCursorMaskWithJournal(self, canvas, canvasJournal, eventDc):
        [self.drawPatch(canvas, eventDc, patch) for patch in canvasJournal.popCursor()]
    # }}}
    # {{{ drawPatch(self, canvas, eventDc, patch)
    def drawPatch(self, canvas, eventDc, patch):
        point = patch[:2]
        if [(c >= 0) and (c < s) for c, s in zip(point, self.canvasSize)] == [True, True]:
            if patch[5] == " ":
                if patch[3] == -1:
                    self._drawCharPatch(eventDc, [*patch[2:-1], "░"], point)
                elif patch[4] & self._CellState.CS_UNDERLINE:
                    self._drawCharPatch(eventDc, patch[2:], point)
                else:
                    self._drawBrushPatch(eventDc, patch[2:], point)
            elif patch[5] in self.arabicShapes:
                self._reshapeArabic(canvas, eventDc, patch, point)
            else:
                self._drawCharPatch(eventDc, patch[2:], point)
            return True
        else:
            return False
    # }}}
    # {{{ getDeviceContext(self, clientSize, parentWindow, viewRect=None)
    def getDeviceContext(self, clientSize, parentWindow, viewRect=None):
        if viewRect == None:
            viewRect = parentWindow.GetViewStart()
        if viewRect == (0, 0):
            eventDc = wx.BufferedDC(wx.ClientDC(parentWindow), self.canvasBitmap)
        else:
            eventDc = GuiBufferedDC(self, self.canvasBitmap, clientSize, wx.ClientDC(parentWindow), viewRect)
        self._lastBrushBg, self._lastBrushFg, self._lastPen = None, None, None
        return eventDc
    # }}}
    # {{{ onPaint(self, clientSize, panelWindow, viewRect)
    def onPaint(self, clientSize, panelWindow, viewRect):
        if self.canvasBitmap != None:
            if viewRect == (0, 0):
                eventDc = wx.BufferedPaintDC(panelWindow, self.canvasBitmap)
            else:
                eventDc = GuiBufferedDC(self, self.canvasBitmap, clientSize, wx.PaintDC(panelWindow), viewRect)
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
        if platform.system() == "Windows":
            self._font = wx.TheFontList.FindOrCreateFont(cellSize[0] + 1, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, self.fontName)
        else:
            self._font = wx.Font(cellSize[0] + 1, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
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
    # __init__(self, canvasSize, cellSize, fontName="Dejavu Sans Mono", fontPathName=os.path.join("assets", "fonts", "DejaVuSansMono.ttf")): initialisation method
    def __init__(self, canvasSize, cellSize, fontName="Dejavu Sans Mono", fontPathName=os.path.join("assets", "fonts", "DejaVuSansMono.ttf")):
        self._brushes, self._font, self._lastBrush, self._lastPen, self._pens = None, None, None, None, None
        self.canvasBitmap, self.cellSize, self.fontName, self.fontPathName = None, None, fontName, fontPathName
        if platform.system() == "Windows":
            WinDLL("gdi32.dll").AddFontResourceW(self.fontPathName.encode("utf16"))
        self._initBrushesAndPens(); self.resize(canvasSize, cellSize);

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
