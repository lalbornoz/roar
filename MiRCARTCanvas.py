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
from MiRCARTCanvasStore import MiRCARTCanvasStore, haveMiRCARTToPngFile, haveUrllib
from MiRCARTColours import MiRCARTColours
import wx

class MiRCARTCanvas(wx.Panel):
    """XXX"""
    parentFrame = None
    canvasPos = canvasSize = canvasWinSize = cellSize = None
    canvasBitmap = canvasMap = canvasTools = None
    brushColours = brushPos = brushSize = None
    mircBrushes = mircPens = None
    canvasJournal = canvasStore = None

    # {{{ _initBrushesAndPens(self): XXX
    def _initBrushesAndPens(self):
        self.mircBrushes = [None for x in range(len(MiRCARTColours))]
        self.mircPens = [None for x in range(len(MiRCARTColours))]
        for mircColour in range(len(MiRCARTColours)):
            self.mircBrushes[mircColour] = wx.Brush(    \
                wx.Colour(MiRCARTColours[mircColour][0:4]), wx.BRUSHSTYLE_SOLID)
            self.mircPens[mircColour] = wx.Pen(         \
                wx.Colour(MiRCARTColours[mircColour][0:4]), 1)
    # }}}
    # {{{ _drawPatch(self, patch, eventDc, tmpDc, atPoint): XXX
    def _drawPatch(self, patch, eventDc, tmpDc, atPoint):
        absPoint = self._relMapPointToAbsPoint(patch[0], atPoint)
        if patch[3] == " ":
            brushFg = self.mircBrushes[patch[1][1]]
            brushBg = self.mircBrushes[patch[1][0]]
            pen = self.mircPens[patch[1][1]]
        else:
            brushFg = self.mircBrushes[patch[1][0]]
            brushBg = self.mircBrushes[patch[1][1]]
            pen = self.mircPens[patch[1][0]]
        for dc in (eventDc, tmpDc):
            dc.SetBrush(brushFg); dc.SetBackground(brushBg); dc.SetPen(pen);
            dc.DrawRectangle(*absPoint, *self.cellSize)
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
        return [(a+b)*c for a,b,c in zip(atPoint, relMapPoint, self.cellSize)]
    # }}}
    # {{{ _setMapCell(self, absMapPoint, colours, charAttrs, char): XXX
    def _setMapCell(self, absMapPoint, colours, charAttrs, char):
        self.canvasMap[absMapPoint[1]][absMapPoint[0]] = [colours, charAttrs, char]
    # }}}

    # {{{ onClose(self, event): XXX
    def onClose(self, event):
        self.Destroy(); self.__del__();
    # }}}
    # {{{ onJournalUpdate(self, isTmp, absMapPoint, patch, eventDc, tmpDc, atPoint):
    def onJournalUpdate(self, isTmp, absMapPoint, patch, eventDc, tmpDc, atPoint, isInherit=False):
        if eventDc == None:
            eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
        if tmpDc == None:
            tmpDc.SelectObject(self.canvasBitmap)
        if isTmp == True:
            if isInherit:
                patch[1:] = self._getMapCell(patch[0])
            self._drawPatch(patch, eventDc, tmpDc, atPoint)
        else:
            if isInherit:
                patchOld = patch.copy()
                patchOld[1:] = self._getMapCell(patchOld[0])
            self._setMapCell(absMapPoint, *patch[1:])
            self._drawPatch(patch, eventDc, tmpDc, atPoint)
            if isInherit:
                return patchOld
    # }}}
    # {{{ onMouseEvent(self, event): XXX
    def onMouseEvent(self, event):
        eventObject = event.GetEventObject()
        eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
        tmpDc.SelectObject(self.canvasBitmap)
        eventPoint = event.GetLogicalPosition(eventDc)
        mapPoint = self._eventPointToMapPoint(eventPoint)
        for tool in self.canvasTools:
            mapPatches = tool.onMouseEvent(                             \
                event, mapPoint, self.brushColours, self.brushSize,     \
                event.Dragging(), event.LeftIsDown(), event.RightIsDown())
            self.canvasJournal.merge(mapPatches, eventDc, tmpDc, mapPoint)
            self.parentFrame.onCanvasUpdate()
        self.parentFrame.onCanvasMotion(event, mapPoint)
    # }}}
    # {{{ onMouseWindowEvent(self, event): XXX
    def onMouseWindowEvent(self, event):
        eventObject = event.GetEventObject()
        eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
        tmpDc.SelectObject(self.canvasBitmap)
        self.canvasJournal.resetCursor(eventDc, tmpDc)
        self.parentFrame.onCanvasMotion(event)
    # }}}
    # {{{ onPaint(self, event): XXX
    def onPaint(self, event):
        eventDc = wx.BufferedPaintDC(self, self.canvasBitmap)
    # }}}
    # {{{ onStoreUpdate(self, newCanvasSize, newCanvas=None):
    def onStoreUpdate(self, newCanvasSize, newCanvas=None):
        if newCanvasSize != None:
            self.resize(newCanvasSize)
        self.canvasJournal.reset()
        if newCanvas != None:
            self.canvasMap = newCanvas.copy()
            for numRow in range(self.canvasSize[1]):
                numRowCols = len(self.canvasMap[numRow])
                if numRowCols < self.canvasSize[0]:
                    colsDelta = self.canvasSize[0] - numRowCols
                    self.canvasMap[numRow][self.canvasSize[0]:] =   \
                            [[(1, 1), 0, " "] for y in range(colsDelta)]
                else:
                    del self.canvasMap[numRow][self.canvasSize[0]:]
        else:
            self.canvasMap = [[[(1, 1), 0, " "]                     \
                    for x in range(self.canvasSize[0])]             \
                for y in range(self.canvasSize[1])]
        canvasWinSize = [a*b for a,b in zip(self.canvasSize, self.cellSize)]
        if self.canvasBitmap != None:
            self.canvasBitmap.Destroy()
        self.canvasBitmap = wx.Bitmap(canvasWinSize)
        eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
        tmpDc.SelectObject(self.canvasBitmap)
        for numRow in range(self.canvasSize[1]):
            for numCol in range(self.canvasSize[0]):
                self.onJournalUpdate(False,                         \
                    (numCol, numRow),                               \
                    [(numCol, numRow),                              \
                     *self.canvasMap[numRow][numCol]],              \
                    eventDc, tmpDc, (0, 0))
        wx.SafeYield()
    # }}}
    # {{{ redo(self): XXX
    def redo(self):
        result = self.canvasJournal.redo()
        self.parentFrame.onCanvasUpdate()
        return result
    # }}}
    # {{{ resize(self, newCanvasSize): XXX
    def resize(self, newCanvasSize):
        if newCanvasSize != self.canvasSize:
            self.SetSize(*self.canvasPos,                   \
                newCanvasSize[0] * self.cellSize[0],        \
                newCanvasSize[1] * self.cellSize[1])
            for numRow in range(self.canvasSize[1]):
                for numNewCol in range(self.canvasSize[0], newCanvasSize[0]):
                    self.canvasMap[numRow].append([1, 1, " "])
            for numNewRow in range(self.canvasSize[1], newCanvasSize[1]):
                self.canvasMap.append([])
                for numNewCol in range(newCanvasSize[0]):
                    self.canvasMap[numNewRow].append([1, 1, " "])
            self.canvasSize = newCanvasSize
            canvasWinSize = (                               \
                self.cellSize[0] * self.canvasSize[0],      \
                self.cellSize[1] * self.canvasSize[1])
            self.canvasBitmap = wx.Bitmap(canvasWinSize)
    # }}}
    # {{{ undo(self): XXX
    def undo(self):
        result = self.canvasJournal.undo()
        self.parentFrame.onCanvasUpdate()
        return result
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
    def __init__(self, parent, parentFrame, canvasPos, canvasSize, canvasTools, cellSize):
        self.parentFrame = parentFrame
        self.canvasPos = canvasPos; self.canvasSize = canvasSize;
        self.canvasTools = [canvasTool(self) for canvasTool in canvasTools]
        self.cellSize = cellSize

        self.brushColours = [4, 1]; self._initBrushesAndPens();
        self.brushPos = [0, 0]; self.brushSize = [1, 1];
        self.canvasJournal = MiRCARTCanvasJournal(parentCanvas=self)
        self.canvasStore = MiRCARTCanvasStore(parentCanvas=self)

        super().__init__(parent, pos=canvasPos, \
            size=[w*h for w,h in zip(canvasSize, cellSize)])
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_ENTER_WINDOW, self.onMouseWindowEvent)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseWindowEvent)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseEvent)
        self.Bind(wx.EVT_MOTION, self.onMouseEvent)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onMouseEvent)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
