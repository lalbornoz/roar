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

from MiRCARTCanvasBackend import MiRCARTCanvasBackend
from MiRCARTCanvasJournal import MiRCARTCanvasJournal
from MiRCARTCanvasExportStore import MiRCARTCanvasExportStore, haveMiRCARTToPngFile, haveUrllib
from MiRCARTCanvasImportStore import MiRCARTCanvasImportStore
from MiRCARTCanvasInterface import MiRCARTCanvasInterface
import wx

class MiRCARTCanvas(wx.Panel):
    """XXX"""
    parentFrame = None
    canvasMap = canvasPos = canvasSize = None
    brushColours = brushPos = brushSize = None
    canvasBackend = canvasJournal = None
    canvasExportStore = canvasImportStore = None
    canvasInterface = None

    # {{{ _commitPatch(self, patch): XXX
    def _commitPatch(self, patch):
        self.canvasMap[patch[0][1]][patch[0][0]] = patch[1:]
    # }}}
    # {{{ _dispatchDeltaPatches(self, deltaPatches): XXX
    def _dispatchDeltaPatches(self, deltaPatches):
        eventDc = self.canvasBackend.getDeviceContext(self)
        for patch in deltaPatches:
            if self.canvasBackend.drawPatch(eventDc, patch):
                self._commitPatch(patch)
        self.parentFrame.onCanvasUpdate(newUndoLevel=self.canvasJournal.patchesUndoLevel)
    # }}}
    # {{{ _dispatchPatch(self, eventDc, isCursor, patch): XXX
    def _dispatchPatch(self, eventDc, isCursor, patch):
        if not self._canvasDirtyCursor:
            self.canvasBackend.drawCursorMaskWithJournal(   \
                self.canvasJournal, eventDc)
            self._canvasDirtyCursor = True
        if self.canvasBackend.drawPatch(eventDc, patch):
            patchDeltaCell = self.canvasMap[patch[0][1]][patch[0][0]]
            patchDelta = [list(patch[0]), *patchDeltaCell.copy()]
            if isCursor:
                self.canvasJournal.pushCursor(patchDelta)
            else:
                if not self._canvasDirty:
                    self.canvasJournal.pushDeltas([], [])
                    self._canvasDirty = True
                self.canvasJournal.updateCurrentDeltas(patchDelta, patch)
                self._commitPatch(patch)
    # }}}

    # {{{ onPanelClose(self, event): XXX
    def onPanelClose(self, event):
        self.Destroy()
    # }}}
    # {{{ onPanelEnterWindow(self, event): XXX
    def onPanelEnterWindow(self, event):
        self.parentFrame.SetFocus()
    # }}}
    # {{{ onPanelInput(self, event): XXX
    def onPanelInput(self, event):
        eventDc = self.canvasBackend.getDeviceContext(self)
        eventType = event.GetEventType()
        self._canvasDirty = self._canvasDirtyCursor = False
        tool = self.canvasInterface.canvasTool
        if eventType == wx.wxEVT_CHAR:
            mapPoint = self.brushPos
            doSkip = tool.onKeyboardEvent(                                  \
                event, mapPoint, self.brushColours, self.brushSize,         \
                chr(event.GetUnicodeKey()), self._dispatchPatch, eventDc)
            if doSkip:
                event.Skip(); return;
        else:
            mapPoint = self.canvasBackend.xlateEventPoint(event, eventDc)
            self.brushPos = mapPoint
            tool.onMouseEvent(                                              \
                event, mapPoint, self.brushColours, self.brushSize,         \
                event.Dragging(), event.LeftIsDown(), event.RightIsDown(),  \
                self._dispatchPatch, eventDc)
        if self._canvasDirty:
            self.parentFrame.onCanvasUpdate(newCellPos=self.brushPos,       \
                newUndoLevel=self.canvasJournal.patchesUndoLevel)
        if eventType == wx.wxEVT_MOTION:
            self.parentFrame.onCanvasUpdate(newCellPos=mapPoint)
    # }}}
    # {{{ onPanelLeaveWindow(self, event): XXX
    def onPanelLeaveWindow(self, event):
        eventDc = self.canvasBackend.getDeviceContext(self)
        self.canvasBackend.drawCursorMaskWithJournal(  \
            self.canvasJournal, eventDc)
    # }}}
    # {{{ onPanelPaint(self, event): XXX
    def onPanelPaint(self, event):
        self.canvasBackend.onPanelPaintEvent(self, event)
    # }}}
    # {{{ onStoreUpdate(self, newCanvasSize, newCanvas=None): XXX
    def onStoreUpdate(self, newCanvasSize, newCanvas=None):
        self.resize(newCanvasSize=newCanvasSize)
        eventDc = self.canvasBackend.getDeviceContext(self)
        for numRow in range(self.canvasSize[1]):
            for numCol in range(self.canvasSize[0]):
                if  newCanvas != None                   \
                and numRow < len(newCanvas)             \
                and numCol < len(newCanvas[numRow]):
                    self._commitPatch([                 \
                        [numCol, numRow], *newCanvas[numRow][numCol]])
                self.canvasBackend.drawPatch(eventDc,   \
                    ([numCol, numRow],                  \
                    *self.canvasMap[numRow][numCol]))
        wx.SafeYield()
    # }}}
    # {{{ resize(self, newCanvasSize): XXX
    def resize(self, newCanvasSize):
        if newCanvasSize != self.canvasSize:
            if self.canvasMap == None:
                self.canvasMap = [[[(1, 1), 0, " "]         \
                        for x in range(self.canvasSize[0])] \
                            for y in range(self.canvasSize[1])]
            else:
                for numRow in range(self.canvasSize[1]):
                    for numNewCol in range(self.canvasSize[0], newCanvasSize[0]):
                        self.canvasMap[numRow].append([[1, 1], 0, " "])
                for numNewRow in range(self.canvasSize[1], newCanvasSize[1]):
                    self.canvasMap.append([])
                    for numNewCol in range(newCanvasSize[0]):
                        self.canvasMap[numNewRow].append([[1, 1], 0, " "])
            self.canvasSize = newCanvasSize
            self.SetSize(*self.canvasPos,                   \
                *[a*b for a,b in zip(self.canvasSize,       \
                    self.canvasBackend.cellSize)])
            self.canvasBackend.reset(self.canvasSize, self.canvasBackend.cellSize)
            self.canvasJournal.resetCursor(); self.canvasJournal.resetUndo();
            self.parentFrame.onCanvasUpdate(                \
                newSize=self.canvasSize, newUndoLevel=-1)
    # }}}

    #
    # _init__(self, parent, parentFrame, canvasPos, canvasSize, cellSize): initialisation method
    def __init__(self, parent, parentFrame, canvasPos, canvasSize, cellSize):
        super().__init__(parent, pos=canvasPos,             \
            size=[w*h for w,h in zip(canvasSize, cellSize)])

        self.parentFrame = parentFrame
        self.canvasMap = None; self.canvasPos = canvasPos; self.canvasSize = canvasSize;
        self.brushColours = [4, 1]; self.brushPos = [0, 0]; self.brushSize = [1, 1];
        self.parentFrame.onCanvasUpdate(newColours=self.brushColours)
        self.canvasBackend = MiRCARTCanvasBackend(canvasSize, cellSize)
        self.canvasJournal = MiRCARTCanvasJournal()
        self.canvasExportStore = MiRCARTCanvasExportStore(parentCanvas=self)
        self.canvasImportStore = MiRCARTCanvasImportStore(parentCanvas=self)
        self.canvasInterface = MiRCARTCanvasInterface(self, parentFrame)

        # Bind event handlers
        self.Bind(wx.EVT_CLOSE, self.onPanelClose)
        self.Bind(wx.EVT_ENTER_WINDOW, self.onPanelEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onPanelLeaveWindow)
        self.parentFrame.Bind(wx.EVT_CHAR, self.onPanelInput)
        for eventType in(                                   \
                wx.EVT_LEFT_DOWN, wx.EVT_MOTION, wx.EVT_RIGHT_DOWN):
            self.Bind(eventType, self.onPanelInput)
        self.Bind(wx.EVT_PAINT, self.onPanelPaint)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
