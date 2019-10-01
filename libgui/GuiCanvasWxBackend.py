#!/usr/bin/env python3
#
# GuiCanvasWxBackend.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from ctypes import *
from GuiCanvasColours import Colours
import GuiCanvasWxBackendFast
import math, os, platform, wx

class GuiBufferedDC(wx.MemoryDC):
    def __del__(self):
        self.dc.Blit(0, 0, *self.viewSize, self, 0, 0)
        self.SelectObject(wx.NullBitmap)

    def __init__(self, backend, buffer, clientSize, dc, viewRect):
        super().__init__()
        canvasSize = [a - b for a, b in zip(backend.canvasSize, viewRect)]
        clientSize = [math.ceil(m / n) for m, n in zip(clientSize, backend.cellSize)]
        viewRect = [m * n for m, n in zip(backend.cellSize, viewRect)]
        viewSize = [min(m, n) for m, n in zip(canvasSize, clientSize)]
        viewSize = [m * n for m, n in zip(backend.cellSize, viewSize)]
        self.SelectObject(buffer); self.SetDeviceOrigin(*viewRect);
        self.dc, self.viewRect, self.viewSize = dc, viewRect, viewSize

class GuiCanvasWxBackend():
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

    class _CellState():
        CS_NONE         = 0x00
        CS_BOLD         = 0x01
        CS_UNDERLINE    = 0x02

    def _blendColours(self, bg, fg):
        return [int((fg * 0.8) + (bg * (1.0 - 0.8))) for bg, fg in zip(Colours[bg][:3], Colours[fg][:3])]

    def _finiBrushesAndPens(self):
        for wxObject in Rtl.flatten([
                (self._brushAlpha,), (*(self._brushes or ()),), (self._penAlpha,), (*(self._pens or ()),),
                *[[self._brushesBlend[bg][fg] for fg in self._brushesBlend[bg].keys()] for bg in self._brushesBlend.keys()],
                *[[self._pensBlend[bg][fg] for fg in self._pensBlend[bg].keys()] for bg in self._pensBlend.keys()]]):
            if wxObject != None:
                wxObject.Destroy()
        self._brushAlpha, self._brushes, self._brushesBlend, self._lastBrush, self._lastPen, self._penAlpha, self._pens, self._pensBlend = None, [], {}, None, None, None, [], {}

    def _initBrushesAndPens(self):
        self._brushes, self._brushesBlend, self._lastBrush, self._lastPen, self._pens, self._pensBlend = [], {}, None, None, [], {}
        self._brushAlpha, self._penAlpha = wx.Brush(wx.Colour(48, 48, 48, 255), wx.BRUSHSTYLE_SOLID), wx.Pen(wx.Colour(48, 48, 48, 255), 1)
        for mircColour in range(len(Colours)):
            self._brushes += [wx.Brush(wx.Colour(Colours[mircColour][:4]), wx.BRUSHSTYLE_SOLID)]; self._brushesBlend[mircColour] = {};
            self._pens += [wx.Pen(wx.Colour(Colours[mircColour][:4]), 1)]; self._pensBlend[mircColour] = {};
            for mircColourFg in range(len(Colours)):
                colourBlend = self._blendColours(mircColour, mircColourFg)
                self._brushesBlend[mircColour][mircColourFg] = wx.Brush(wx.Colour(colourBlend), wx.BRUSHSTYLE_SOLID)
                self._pensBlend[mircColour][mircColourFg] = wx.Pen(wx.Colour(colourBlend), 1)

    def _reshapeArabic(self, canvas, eventDc, isCursor, patch, point):
        lastCell, patches = point[0], []
        while True:
            if ((lastCell + 1) >= (canvas.size[0] - 1)) \
            or (not canvas.map[point[1]][lastCell + 1][3] in self.arabicShapes):
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
            patches += [[runX, point[1], *runCell]]
        runCell = list(patch[2:])
        if connect and (self.arabicShapes[patch[5]][3] != None):
            runCell[3] = self.arabicShapes[patch[5]][3]
        else:
            runCell[3] = self.arabicShapes[patch[5]][0]
        patches += [[*point, *runCell]]
        return patches

    def _setBrushColours(self, dc, isCursor, patch, patchBg):
        if  ((patch[0] != -1) and (patch[1] != -1)) \
        or  ((patch[0] == -1) and (patch[1] != -1)):
            if not isCursor:
                brush, pen = self._brushes[patch[1]], self._pens[patch[1]]
            else:
                bg = patchBg[1] if patchBg[1] != -1 else 14
                brush, pen = self._brushesBlend[bg][patch[1]], self._pensBlend[bg][patch[1]]
        else:
            if not isCursor:
                brush, pen = self._brushAlpha, self._penAlpha
            else:
                bg = patchBg[1] if patchBg[1] != -1 else 14
                brush, pen = self._brushesBlend[bg][14], self._pensBlend[bg][14]
        return brush, pen

    def drawCursorMaskWithJournal(self, canvas, canvasJournal, eventDc, reset=True):
        eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
        cursorPatches = canvasJournal.popCursor(reset=reset); patches = [];
        for cursorCell in [p[:2] for p in cursorPatches]:
            if  (cursorCell[0] < canvas.size[0])    \
            and (cursorCell[1] < canvas.size[1]):
                patches += [[*cursorCell, *canvas.map[cursorCell[1]][cursorCell[0]]]]
        if len(patches) > 0:
            self.drawPatches(canvas, eventDc, patches, False)
        eventDc.SetDeviceOrigin(*eventDcOrigin)
        return cursorPatches

    def drawPatches(self, canvas, eventDc, patches, isCursor=False):
        GuiCanvasWxBackendFast.drawPatches()
        patchesRender = []
        for patch in patches:
            point = patch[:2]
            if [(c >= 0) and (c < s) for c, s in zip(point, self.canvasSize)] == [True, True]:
                if patch[5] in self.arabicShapes:
                    for patchReshaped in self._reshapeArabic(canvas, eventDc, isCursor, patch, point):
                        patchesRender += [patchReshaped]
                else:
                    patchesRender += [patch]
        numPatch, textBg = 0, wx.Colour(0, 0, 0, 0)
        rectangles, pens, brushes = [None] * len(patchesRender), [None] * len(patchesRender), [None] * len(patchesRender)
        textList, coords, foregrounds, backgrounds = [], [], [], []
        eventDc.SetFont(self._font)
        for patchRender in patchesRender:
            if (patchRender[5] == " ") and (patchRender[3] == -1):
                text, textFg = "░", wx.Colour(0, 0, 0, 255)
            elif isCursor and (patchRender[5] == " ") and (canvas.map[patchRender[1]][patchRender[0]][3] != " "):
                patchRender = [*patchRender[:-2], *canvas.map[patchRender[1]][patchRender[0]][2:]]
                text, textFg = canvas.map[patchRender[1]][patchRender[0]][3], wx.Colour(self._blendColours(canvas.map[patchRender[1]][patchRender[0]][0], patchRender[3]))
            elif isCursor and (patchRender[5] == " ") and (canvas.map[patchRender[1]][patchRender[0]][2] & self._CellState.CS_UNDERLINE):
                patchRender = [*patchRender[:-2], *canvas.map[patchRender[1]][patchRender[0]][2:]]
                text, textFg = "_", wx.Colour(self._blendColours(canvas.map[patchRender[1]][patchRender[0]][0], patchRender[3]))
            elif patchRender[5] != " ":
                text, textFg = patchRender[5], wx.Colour(Colours[patchRender[2]][:4])
            elif patchRender[4] & self._CellState.CS_UNDERLINE:
                text, textFg = "_", wx.Colour(Colours[patchRender[2]][:4])
            else:
                text = None
            brush, pen = self._setBrushColours(eventDc, isCursor, patchRender[2:], canvas.map[patchRender[1]][patchRender[0]])
            rectangles[numPatch] = [patchRender[:2][0] * self.cellSize[0], patchRender[:2][1] * self.cellSize[1], self.cellSize[0], self.cellSize[1]];
            pens[numPatch] = pen; brushes[numPatch] = brush;
            if text != None:
                textList += [text]; coords += [[patchRender[:2][0] * self.cellSize[0], patchRender[:2][1] * self.cellSize[1]]]; foregrounds += [textFg]; backgrounds += [textBg];
            numPatch += 1
        eventDc.DrawRectangleList(rectangles, pens, brushes)
        eventDc.DrawTextList(textList, coords, foregrounds, backgrounds)

    def getDeviceContext(self, clientSize, parentWindow, viewRect=None):
        if viewRect == None:
            viewRect = parentWindow.GetViewStart()
        if viewRect == (0, 0):
            eventDc = wx.BufferedDC(wx.ClientDC(parentWindow), self.canvasBitmap)
        else:
            eventDc = GuiBufferedDC(self, self.canvasBitmap, clientSize, wx.ClientDC(parentWindow), viewRect)
        self._lastBrush, self._lastPen = None, None
        return eventDc

    def onPaint(self, clientSize, panelWindow, viewRect):
        if self.canvasBitmap != None:
            if viewRect == (0, 0):
                eventDc = wx.BufferedPaintDC(panelWindow, self.canvasBitmap)
            else:
                eventDc = GuiBufferedDC(self, self.canvasBitmap, clientSize, wx.PaintDC(panelWindow), viewRect)

    def resize(self, canvasSize):
        if platform.system() == "Windows":
            self._font = wx.TheFontList.FindOrCreateFont(self.fontSize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, self.fontName)
            fontInfoDesc = self._font.GetNativeFontInfoDesc().split(";"); fontInfoDesc[12] = "3";
            self._font.SetNativeFontInfo(";".join(fontInfoDesc))
            dc = wx.MemoryDC()
            dc.SetFont(self._font); self.cellSize = dc.GetTextExtent("_");
            dc.Destroy()
        else:
            self._font = wx.Font(self.cellSize[0] + 1, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        winSize = [a * b for a, b in zip(canvasSize, self.cellSize)]
        if self.canvasBitmap == None:
            self.canvasBitmap = wx.Bitmap(winSize)
        else:
            oldDc = wx.MemoryDC(); oldDc.SelectObject(self.canvasBitmap);
            newDc = wx.MemoryDC(); newBitmap = wx.Bitmap(winSize); newDc.SelectObject(newBitmap);
            newDc.Blit(0, 0, *self.canvasBitmap.GetSize(), oldDc, 0, 0)
            oldDc.SelectObject(wx.NullBitmap)
            self.canvasBitmap.Destroy(); self.canvasBitmap = newBitmap;
        self.canvasSize = canvasSize

    def xlateEventPoint(self, event, eventDc, viewRect):
        eventPoint = event.GetLogicalPosition(eventDc)
        rectX, rectY = eventPoint.x - (eventPoint.x % self.cellSize[0]), eventPoint.y - (eventPoint.y % self.cellSize[1])
        mapX, mapY = int(rectX / self.cellSize[0] if rectX else 0), int(rectY / self.cellSize[1] if rectY else 0)
        return [m + n for m, n in zip((mapX, mapY), viewRect)]

    def __del__(self):
        if self.canvasBitmap != None:
            self.canvasBitmap.Destroy(); self.canvasBitmap = None;
        self._finiBrushesAndPens()

    def __init__(self, canvasSize, fontName="Dejavu Sans Mono", fontPathName=os.path.join("assets", "fonts", "DejaVuSansMono.ttf"), fontSize=8):
        self._brushes, self._font, self._lastBrush, self._lastPen, self._pens = None, None, None, None, None
        self.canvasBitmap, self.cellSize, self.fontName, self.fontPathName, self.fontSize = None, None, fontName, fontPathName, fontSize
        if platform.system() == "Windows":
            WinDLL("gdi32.dll").AddFontResourceW(self.fontPathName.encode("utf16"))
        self._initBrushesAndPens(); self.resize(canvasSize);

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
