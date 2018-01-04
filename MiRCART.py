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
import sys

class MiRCARTCanvas(wx.Panel):
    """XXX"""
    canvasPos = canvasSize = None
    canvasMap = None
    cellPos = cellSize = None
    brushBg = brushFg = penBg = penFg = None
    mircBg = mircFg = None
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

    # {{{ _onMouseEvent(): XXX
    def _onMouseEvent(self, event):
        eventObject = event.GetEventObject()
        if event.Dragging():
            eventDc = wx.ClientDC(self)
            eventPoint = event.GetLogicalPosition(eventDc)
            rectX = eventPoint.x - (eventPoint.x % self.cellSize[0])
            rectY = eventPoint.y - (eventPoint.y % self.cellSize[1])
            mapX = int(rectX / 7 if rectX else 0)
            mapY = int(rectY / 14 if rectY else 0)
            eventDc.SetBackground(self.brushBg);
            if event.LeftIsDown():
                eventDc.SetBrush(self.brushFg);
                eventDc.SetPen(self.penFg)
                self.canvasMap[mapX][mapY] = [self.mircFg, self.mircFg, " "]
            elif event.RightIsDown():
                eventDc.SetBrush(self.brushBg);
                eventDc.SetPen(self.penBg)
                self.canvasMap[mapX][mapY] = [self.mircBg, self.mircBg, " "]
            eventDc.DrawRectangle(rectX, rectY,             \
                self.cellSize[0], self.cellSize[1])
    # }}}
    # {{{ onCharHook(): XXX
    def onCharHook(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_UP:
            self.mircFg = self.mircFg + 1 if self.mircFg < 15 else 15
        elif keyCode == wx.WXK_DOWN:
            self.mircFg = self.mircFg - 1 if self.mircFg > 0 else 0
        self.brushBg = wx.Brush(wx.Colour(self.mircColours[self.mircBg]), wx.BRUSHSTYLE_SOLID)
        self.brushFg = wx.Brush(wx.Colour(self.mircColours[self.mircFg]), wx.BRUSHSTYLE_SOLID)
        self.penBg = wx.Pen(wx.Colour(self.mircColours[self.mircBg]), 1)
        self.penFg = wx.Pen(wx.Colour(self.mircColours[self.mircFg]), 1)
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
        eventDc = wx.BufferedPaintDC(self)
        eventDc.SetBackground(wx.Brush(wx.BLACK))
        eventDc.Clear()
        for cellX in range(0, self.canvasSize[0]):
            for cellY in range(0, self.canvasSize[1]):
                eventDc.SetBackground(wx.Brush(wx.Colour(self.mircColours[self.canvasMap[cellX][cellY][0]]), wx.BRUSHSTYLE_SOLID))
                eventDc.SetBrush(wx.Brush(wx.Colour(self.mircColours[self.canvasMap[cellX][cellY][1]]), wx.BRUSHSTYLE_SOLID))
                eventDc.SetPen(wx.Pen(wx.Colour(self.mircColours[self.canvasMap[cellX][cellY][1]]), 1))
                rectX = cellX * self.cellSize[0]; rectY = cellY * self.cellSize[1];
                eventDc.DrawRectangle(rectX, rectY,         \
                    self.cellSize[0], self.cellSize[1])
    # }}}
    # {{{ onRightDown(): XXX
    def onRightDown(self, event):
        self._onMouseEvent(event)
    # }}}

    #
    # Initialisation method
    def __init__(self, parent, canvasPos, cellSize, canvasSize):
        super().__init__(parent, pos=canvasPos, size=(      \
            cellSize[0] * canvasSize[0],
            cellSize[1] * canvasSize[1]))

        self.canvasPos = canvasPos; self.canvasSize = canvasSize;
        self.canvasMap = [[[1, 1, " "] for y in range(canvasSize[1])] for x in range(canvasSize[0])]
        self.cellPos = (0, 0); self.cellSize = cellSize;
        self.brushBg = wx.Brush(wx.Colour(self.mircColours[1]), wx.BRUSHSTYLE_SOLID)
        self.brushFg = wx.Brush(wx.Colour(self.mircColours[4]), wx.BRUSHSTYLE_SOLID)
        self.penBg = wx.Pen(wx.Colour(self.mircColours[1]), 1)
        self.penFg = wx.Pen(wx.Colour(self.mircColours[4]), 1)
        self.mircBg = 1; self.mircFg = 4;
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.Bind(wx.EVT_CHAR_HOOK, self.onCharHook)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)

class MiRCARTFrame(wx.Frame):
    """XXX"""
    menuFile = menuFileSaveAs = menuFileExit = menuBar = None
    panelSkin = panelCanvas = None

    # {{{ onFileSaveAs(): XXX
    def onFileSaveAs(self, event):
        pass
    # }}}
    # {{{ onFileExit(): XXX
    def onFileExit(self, event):
        self.Close(True)
    # }}}

    #
    # Initialisation method
    def __init__(self, parent, appSize=(1024, 768), canvasPos=(25, 25), cellSize=(7, 14), canvasSize=(80, 25)):
        super().__init__(parent, wx.ID_ANY, "MiRCART", size=appSize)

        self.menuFile = wx.Menu()
        self.menuFileExit = self.menuFile.Append(wx.ID_EXIT, "E&xit", "Exit")
        self.menuFileSaveAs = self.menuFile.Append(wx.ID_SAVE, "Save &As...", "Save As...")
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.menuFile, "&File")

        self.panelSkin = wx.Panel(self, wx.ID_ANY)
        self.panelCanvas = MiRCARTCanvas(self.panelSkin,    \
            canvasPos=canvasPos, cellSize=cellSize, canvasSize=canvasSize)

        self.Bind(wx.EVT_MENU, self.onFileExit, self.menuFileExit)
        self.Bind(wx.EVT_MENU, self.onFileSaveAs, self.menuFileSaveAs)
        self.CreateStatusBar()
        self.SetMenuBar(self.menuBar)
        self.Show(True)

#
# Entry point
def main(*argv):
    wxApp = wx.App(False)
    MiRCARTFrame(None)
    wxApp.MainLoop()
if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
