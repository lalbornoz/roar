#!/usr/bin/env python3
#
# MiRCART.py -- XXX
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

import wx
import os, sys

# {{{ mircColours: mIRC colour number to RGBA map given none of ^[BFV_] (bold, italic, reverse, underline)
mircColours = [
    (255, 255, 255, 255),   # White
    (0,   0,   0,   255),   # Black
    (0,   0,   187, 255),   # Blue
    (0,   187, 0,   255),   # Green
    (255, 85,  85,  255),   # Light Red
    (187, 0,   0,   255),   # Red
    (187, 0,   187, 255),   # Purple
    (187, 187, 0,   255),   # Yellow
    (255, 255, 85,  255),   # Light Yellow
    (85,  255, 85,  255),   # Light Green
    (0,   187, 187, 255),   # Cyan
    (85,  255, 255, 255),   # Light Cyan
    (85,  85,  255, 255),   # Light Blue
    (255, 85,  255, 255),   # Pink
    (85,  85,  85,  255),   # Grey
    (187, 187, 187, 255),   # Light Grey
]
# }}}

class MiRCARTCanvas(wx.Panel):
    """XXX"""
    canvasPos = canvasSize = canvasWinSize = cellPos = cellSize = None
    canvasBitmap = canvasMap = canvasTools = None
    mircBg = mircFg = mircBrushes = mircPens = None
    patchesTmp = patchesUndo = None

    # {{{ _drawPatch(): XXX
    def _drawPatch(self, patch, eventDc, tmpDc, atX, atY):
        patchXabs = (atX + patch[0]) * self.getCellWidth()
        patchYabs = (atY + patch[1]) * self.getCellHeight()
        brushFg = self.mircBrushes[patch[2]]
        brushBg = self.mircBrushes[patch[3]]
        pen = self.mircPens[patch[2]]
        for dc in (eventDc, tmpDc):
            dc.SetBrush(brushFg); dc.SetBackground(brushBg); dc.SetPen(pen);
            dc.DrawRectangle(patchXabs, patchYabs,                  \
                self.getCellWidth(), self.getCellHeight())
    # }}}
    # {{{ _eventPointToMapX(): XXX
    def _eventPointToMapX(self, eventPoint):
        rectX = eventPoint.x - (eventPoint.x % self.getCellWidth())
        return int(rectX / self.getCellWidth() if rectX else 0)
    # }}}
    # {{{ _eventPointToMapY(): XXX
    def _eventPointToMapY(self, eventPoint):
        rectY = eventPoint.y - (eventPoint.y % self.getCellHeight())
        return int(rectY / self.getCellHeight() if rectY else 0)
    # }}}
    # {{{ _onMouseEvent(): XXX
    def _onMouseEvent(self, event):
        eventObject = event.GetEventObject()
        eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
        tmpDc.SelectObject(self.canvasBitmap)
        eventPoint = event.GetLogicalPosition(eventDc)
        mapX = self._eventPointToMapX(eventPoint)
        mapY = self._eventPointToMapY(eventPoint)
        for tool in self.canvasTools:
            if event.Dragging():
                mapPatches = tool.onMouseMotion(event, mapX, mapY, event.LeftIsDown(), event.RightIsDown())
            else:
                mapPatches = tool.onMouseDown(event, mapX, mapY, event.LeftIsDown(), event.RightIsDown())
            self._processMapPatches(mapPatches, eventDc, tmpDc, mapX, mapY)
    # }}}
    # {{{ _processMapPatches(): XXX
    def _processMapPatches(self, mapPatches, eventDc, tmpDc, atX, atY):
        for mapPatch in mapPatches:
            mapPatchTmp = mapPatch[0]; mapPatchW = mapPatch[1]; mapPatchH = mapPatch[2];
            if mapPatchTmp and self.patchesTmp:
                for patch in self.patchesTmp:
                    self._drawPatch(patch, eventDc, tmpDc, 0, 0)
                self.patchesTmp = []
            for patch in mapPatch[3]:
                if mapPatchTmp:
                    mapItem = self.canvasMap[atY + patch[1]][atX + patch[0]]
                    self.patchesTmp.append((atX + patch[0],         \
                        atY + patch[1], mapItem[0], mapItem[1], mapItem[2]))
                    self._drawPatch(patch, eventDc, tmpDc, atX, atY)
                else:
                    self._drawPatch(patch, eventDc, tmpDc, atX, atY)
                    self.canvasMap[atY + patch[1]][atX + patch[0]] =\
                        [patch[2], patch[3], " "];
    # }}}
    # {{{ getBackgroundColour(): XXX
    def getBackgroundColour(self):
        return self.mircBg
    # }}}
    # {{{ getCellHeight(): XXX
    def getCellHeight(self):
        return self.cellSize[1]
    # }}}
    # {{{ getCellWidth(): XXX
    def getCellWidth(self):
        return self.cellSize[0]
    # }}}
    # {{{ getForegroundColour(): XXX
    def getForegroundColour(self):
        return self.mircFg
    # }}}
    # {{{ getHeight(): XXX
    def getHeight(self):
        return self.canvasSize[1]
    # }}}
    # {{{ getMap(): XXX
    def getMap(self):
        return self.canvasMap
    # }}}
    # {{{ getWidth(): XXX
    def getWidth(self):
        return self.canvasSize[0]
    # }}}
    # {{{ onLeftDown(): XXX
    def onLeftDown(self, event):
        self._onMouseEvent(event)
    # }}}
    # {{{ onMotion(): XXX
    def onMotion(self, event):
            self._onMouseEvent(event)
    # }}}
    # {{{ onPaint(): XXX
    def onPaint(self, event):
        eventDc = wx.BufferedPaintDC(self, self.canvasBitmap)
    # }}}
    # {{{ onPaletteEvent(): XXX
    def onPaletteEvent(self, leftDown, rightDown, numColour):
        if leftDown:
            self.mircFg = numColour
        elif rightDown:
            self.mircBg = numColour
    # }}}
    # {{{ onRightDown(): XXX
    def onRightDown(self, event):
        self._onMouseEvent(event)
    # }}}
    # {{{ Initialisation method
    def __init__(self, parent, canvasPos, cellSize, canvasSize, canvasTools):
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
        self.mircBrushes = [None for x in range(len(mircColours))]
        self.mircPens = [None for x in range(len(mircColours))]
        for mircColour in range(0, len(mircColours)):
            self.mircBrushes[mircColour] = wx.Brush(                \
                wx.Colour(mircColours[mircColour]), wx.BRUSHSTYLE_SOLID)
            self.mircPens[mircColour] = wx.Pen(                     \
                wx.Colour(mircColours[mircColour]), 1)

        self.patchesTmp = []; self.patchesUndo = [];

        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
    # }}}

class MiRCARTTool():
    """XXX"""
    parentCanvas = None

    # {{{ onMouseDown(): XXX
    def onMouseDown(self, event, mapX, mapY, isLeftDown, isRightDown):
        pass
    # }}}
    # {{{ onMouseMotion(): XXX
    def onMouseMotion(self, event, mapX, mapY, isLeftDown, isRightDown):
        pass
    # }}}
    # {{{ Initialisation method
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas
    # }}}

class MiRCARTToolRect(MiRCARTTool):
    """XXX"""

    # {{{ _draw(): XXX
    def _draw(self, event, mapX, mapY, isLeftDown, isRightDown):
        if isLeftDown:
            return [[False, 1, 1, [[0, 0,                           \
                self.parentCanvas.getForegroundColour(),            \
                self.parentCanvas.getForegroundColour(), " "]]],
                    [True, 1, 1, [[0, 0,                            \
                self.parentCanvas.getForegroundColour(),            \
                self.parentCanvas.getForegroundColour(), " "]]]]
        elif isRightDown:
            return [[False, 1, 1, [[0, 0,                           \
                self.parentCanvas.getBackgroundColour(),            \
                self.parentCanvas.getBackgroundColour(), " "]]],    \
                    [True, 1, 1, [[0, 0,                            \
                self.parentCanvas.getForegroundColour(),            \
                self.parentCanvas.getForegroundColour(), " "]]]]
        else:
            return [[True, 1, 1, [[0, 0,                            \
                self.parentCanvas.getForegroundColour(),            \
                self.parentCanvas.getForegroundColour(), " "]]]]
    # }}}
    # {{{ onMouseDown(): XXX
    def onMouseDown(self, event, mapX, mapY, isLeftDown, isRightDown):
        return self._draw(event, mapX, mapY, isLeftDown, isRightDown)
    # }}}
    # {{{ onMouseMotion(): XXX
    def onMouseMotion(self, event, mapX, mapY, isLeftDown, isRightDown):
        return self._draw(event, mapX, mapY, isLeftDown, isRightDown)
    # }}}
    # {{{ Initialisation method
    def __init__(self, parentCanvas):
        super().__init__(parentCanvas)
    # }}}

class MiRCARTPalette(wx.Panel):
    """XXX"""
    panelsByColour = onPaletteEvent = None

    # {{{ onLeftDown(): XXX
    def onLeftDown(self, event):
        numColour = int(event.GetEventObject().GetName())
        self.onPaletteEvent(True, False, numColour)
    # }}}
    # {{{ onRightDown(): XXX
    def onRightDown(self, event):
        numColour = int(event.GetEventObject().GetName())
        self.onPaletteEvent(False, True, numColour)
    # }}}
    # {{{ Initialisation method
    def __init__(self, parent, parentPos, cellSize, onPaletteEvent):
        panelSizeW = 6 * cellSize[0]; panelSizeH = 2 * cellSize[1];
        paletteSize = (panelSizeW * 16, panelSizeH)
        super().__init__(parent, pos=parentPos, size=paletteSize)
        self.panelsByColour = [None] * len(mircColours)
        for numColour in range(0, len(mircColours)):
            posX = (numColour * (cellSize[0] * 6))
            self.panelsByColour[numColour] = wx.Panel(self,         \
                pos=(posX, 0), size=(panelSizeW, panelSizeH))
            self.panelsByColour[numColour].SetBackgroundColour(     \
                wx.Colour(mircColours[numColour]))
            self.panelsByColour[numColour].Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
            self.panelsByColour[numColour].Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
            self.panelsByColour[numColour].SetName(str(numColour))
        self.onPaletteEvent = onPaletteEvent
    # }}}

class MiRCARTFrame(wx.Frame):
    """XXX"""
    menuFile = menuFileSaveAs = menuFileExit = menuBar = None
    panelSkin = panelCanvas = panelPalette = None
    statusBar = None

    # {{{ _updateStatusBar(): XXX
    def _updateStatusBar(self):
        text = "Foreground colour:"
        text += " " + str(self.panelCanvas.getForegroundColour())
        text += " | "
        text += "Background colour:"
        text += " " + str(self.panelCanvas.getBackgroundColour())
        self.statusBar.SetStatusText(text)
    # }}}
    # {{{ onFileSaveAs(): XXX
    def onFileSaveAs(self, event):
        with wx.FileDialog(self, "Save As...", os.getcwd(), "",     \
                "*.txt", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            else:
                try:
                    with open(dialog.GetPath(), "w") as file:
                        canvasMap = self.panelCanvas.getMap()
                        canvasHeight = self.panelCanvas.getHeight()
                        canvasWidth = self.panelCanvas.getWidth()
                        for canvasRow in range(0, canvasHeight):
                            colourLastBg = colourLastFg = None;
                            for canvasCol in range(0, canvasWidth):
                                canvasColBg = canvasMap[canvasRow][canvasCol][0]
                                canvasColFg = canvasMap[canvasRow][canvasCol][1]
                                canvasColText = canvasMap[canvasRow][canvasCol][2]
                                if colourLastBg != canvasColBg      \
                                or colourLastFg != canvasColFg:
                                    colourLastBg = canvasColBg; colourLastFg = canvasColFg;
                                    file.write("" + str(canvasColFg) + "," + str(canvasColBg))
                                file.write(canvasColText)
                            file.write("\n")
                except IOError as error:
                    wx.LogError("IOError {}".format(error))
    # }}}
    # {{{ onFileExit(): XXX
    def onFileExit(self, event):
        self.Close(True)
    # }}}
    # {{{ onPaletteEvent(): XXX
    def onPaletteEvent(self, leftDown, rightDown, numColour):
        self.panelCanvas.onPaletteEvent(leftDown, rightDown, numColour)
        self._updateStatusBar()
    # }}}
    # {{{ Initialisation method
    def __init__(self, parent, appSize=(1024, 768), canvasPos=(25, 25), cellSize=(7, 14), canvasSize=(80, 25)):
        super().__init__(parent, wx.ID_ANY, "MiRCART", size=appSize)

        self.menuFile = wx.Menu()
        self.menuFileSaveAs = self.menuFile.Append(wx.ID_SAVE, "Save &As...", "Save As...")
        self.menuFileExit = self.menuFile.Append(wx.ID_EXIT, "E&xit", "Exit")
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.menuFile, "&File")

        self.panelSkin = wx.Panel(self, wx.ID_ANY)
        self.panelCanvas = MiRCARTCanvas(self.panelSkin,            \
            canvasPos=canvasPos, cellSize=cellSize,                 \
            canvasSize=canvasSize, canvasTools=[MiRCARTToolRect])
        self.panelPalette = MiRCARTPalette(self.panelSkin,          \
            (25, (canvasSize[1] + 3) * cellSize[1]), cellSize, self.onPaletteEvent)

        self.statusBar = self.CreateStatusBar()
        self._updateStatusBar()

        self.Bind(wx.EVT_MENU, self.onFileExit, self.menuFileExit)
        self.Bind(wx.EVT_MENU, self.onFileSaveAs, self.menuFileSaveAs)
        self.SetMenuBar(self.menuBar)
        self.Show(True)
    # }}}

#
# Entry point
def main(*argv):
    wxApp = wx.App(False)
    MiRCARTFrame(None)
    wxApp.MainLoop()
if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
