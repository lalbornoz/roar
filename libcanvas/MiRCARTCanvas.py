#!/usr/bin/env python3
#
# MiRCARTCanvas.py -- XXX
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from MiRCARTCanvasBackend import MiRCARTCanvasBackend
from MiRCARTCanvasJournal import MiRCARTCanvasJournal
from MiRCARTCanvasExportStore import MiRCARTCanvasExportStore, haveMiRCARTToPngFile, haveUrllib
from MiRCARTCanvasImportStore import MiRCARTCanvasImportStore
from MiRCARTCanvasInterface import MiRCARTCanvasInterface
from MiRCARTImgurApiKey import MiRCARTImgurApiKey
import wx

class MiRCARTCanvas(wx.Panel):
    """XXX"""
    parentFrame = None
    defaultCanvasPos = defaultCanvasSize = defaultCellSize = None
    canvasMap = canvasPos = canvasSize = None
    brushColours = brushPos = brushSize = None
    canvasBackend = canvasJournal = None
    canvasExportStore = canvasImportStore = None
    canvasInterface = None
    imgurApiKey = MiRCARTImgurApiKey.imgurApiKey

    # {{{ _commitPatch(self, patch): XXX
    def _commitPatch(self, patch):
        self.canvasMap[patch[1]][patch[0]] = patch[2:]
    # }}}
    # {{{ _dispatchDeltaPatches(self, deltaPatches): XXX
    def _dispatchDeltaPatches(self, deltaPatches):
        eventDc = self.canvasBackend.getDeviceContext(self)
        for patch in deltaPatches:
            if self.canvasBackend.drawPatch(eventDc, patch):
                self._commitPatch(patch)
        self.parentFrame.onCanvasUpdate(undoLevel=self.canvasJournal.patchesUndoLevel)
    # }}}
    # {{{ _dispatchPatch(self, eventDc, isCursor, patch): XXX
    def _dispatchPatch(self, eventDc, isCursor, patch):
        if not self._canvasDirtyCursor:
            self.canvasBackend.drawCursorMaskWithJournal(   \
                self.canvasJournal, eventDc)
            self._canvasDirtyCursor = True
        if self.canvasBackend.drawPatch(eventDc, patch):
            patchDeltaCell = self.canvasMap[patch[1]][patch[0]]
            patchDelta = [*patch[0:2], *patchDeltaCell]
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
            if mapPoint[0] >= self.canvasSize[0]                            \
            or mapPoint[1] >= self.canvasSize[1]:
                return
            self.brushPos = mapPoint
            tool.onMouseEvent(                                              \
                event, mapPoint, self.brushColours, self.brushSize,         \
                event.Dragging(), event.LeftIsDown(), event.RightIsDown(),  \
                self._dispatchPatch, eventDc)
        if self._canvasDirty:
            self.parentFrame.onCanvasUpdate(cellPos=self.brushPos,          \
                undoLevel=self.canvasJournal.patchesUndoLevel)
        if eventType == wx.wxEVT_MOTION:
            self.parentFrame.onCanvasUpdate(cellPos=mapPoint)
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
                        numCol, numRow, *newCanvas[numRow][numCol]])
                self.canvasBackend.drawPatch(eventDc,   \
                    [numCol, numRow,                    \
                    *self.canvasMap[numRow][numCol]])
        wx.SafeYield()
    # }}}
    # {{{ resize(self, newCanvasSize): XXX
    def resize(self, newCanvasSize):
        if newCanvasSize != self.canvasSize:
            if self.canvasMap == None:
                self.canvasMap = []; oldCanvasSize = [0, 0];
            else:
                oldCanvasSize = self.canvasSize
            deltaCanvasSize = [b-a for a,b in zip(oldCanvasSize, newCanvasSize)]

            newWinSize = [a*b for a,b in zip(newCanvasSize, self.canvasBackend.cellSize)]
            self.SetMinSize(newWinSize)
            self.SetSize(wx.DefaultCoord, wx.DefaultCoord, *newWinSize)
            curWindow = self
            while curWindow != None:
                curWindow.Layout()
                curWindow = curWindow.GetParent()

            self.canvasBackend.resize(newCanvasSize, self.canvasBackend.cellSize)
            eventDc = self.canvasBackend.getDeviceContext(self)
            self.canvasJournal.resetCursor(); self.canvasJournal.resetUndo();

            if deltaCanvasSize[0] < 0:
                for numRow in range(oldCanvasSize[1]):
                    del self.canvasMap[numRow][-1:(deltaCanvasSize[0]-1):-1]
            else:
                for numRow in range(oldCanvasSize[1]):
                    self.canvasMap[numRow].extend(              \
                            [[1, 1, 0, " "]] * deltaCanvasSize[0])
                    for numNewCol in range(oldCanvasSize[0], newCanvasSize[0]):
                        self.canvasBackend.drawPatch(           \
                            eventDc, [numNewCol, numRow,        \
                            *self.canvasMap[numRow][-1]])
            if deltaCanvasSize[1] < 0:
                del self.canvasMap[-1:(deltaCanvasSize[1]-1):-1]
            else:
                for numNewRow in range(oldCanvasSize[1], newCanvasSize[1]):
                    self.canvasMap.extend(                      \
                                [[[1, 1, 0, " "]] * newCanvasSize[0]])
                    for numNewCol in range(newCanvasSize[0]):
                        self.canvasBackend.drawPatch(           \
                            eventDc, [numNewCol, numNewRow,     \
                            *self.canvasMap[-1][-1]])

            self.canvasSize = newCanvasSize
            wx.SafeYield()
            self.parentFrame.onCanvasUpdate(size=newCanvasSize, undoLevel=-1)
    # }}}

    # {{{ __del__(self): destructor method
    def __del__(self):
        if self.canvasMap != None:
            self.canvasMap.clear(); self.canvasMap = None;
    # }}}

    #
    # __init__(self, parent, parentFrame, defaultCanvasPos, defaultCanvasSize, defaultCellSize): initialisation method
    def __init__(self, parent, parentFrame, defaultCanvasPos, defaultCanvasSize, defaultCellSize):
        super().__init__(parent, pos=defaultCanvasPos,      \
            size=[w*h for w,h in zip(defaultCanvasSize, defaultCellSize)])

        self.parentFrame = parentFrame
        self.canvasMap = None
        self.canvasPos = defaultCanvasPos; self.canvasSize = defaultCanvasSize;
        self.defaultCanvasPos = defaultCanvasPos; self.defaultCanvasSize = defaultCanvasSize;
        self.brushColours = [4, 1]; self.brushPos = [0, 0]; self.brushSize = [1, 1];
        self.parentFrame.onCanvasUpdate(                    \
            brushSize=self.brushSize, colours=self.brushColours)
        self.canvasBackend = MiRCARTCanvasBackend(defaultCanvasSize, defaultCellSize)
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
