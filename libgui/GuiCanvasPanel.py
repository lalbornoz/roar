#!/usr/bin/env python3
#
# GuiCanvasPanel.py 
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import wx

class GuiCanvasPanel(wx.Panel):
    # {{{ _drawPatch(self, eventDc, isCursor, patch)
    def _drawPatch(self, eventDc, isCursor, patch):
        if not self.canvas.dirtyCursor:
            self.backend.drawCursorMaskWithJournal(self.canvas.journal, eventDc)
            self.canvas.dirtyCursor = True
        if  self.backend.drawPatch(eventDc, patch)  \
        and isCursor:
            patchDeltaCell = self.canvas.map[patch[1]][patch[0]]; patchDelta = [*patch[0:2], *patchDeltaCell];
            self.canvas.journal.pushCursor(patchDelta)
    # }}}

    # {{{ dispatchDeltaPatches(self, deltaPatches)
    def dispatchDeltaPatches(self, deltaPatches):
        eventDc = self.backend.getDeviceContext(self)
        for patch in deltaPatches:
            if patch == None:
                continue
            elif patch[0] == "resize":
                del eventDc; self.resize(patch[1:], False); eventDc = self.backend.getDeviceContext(self);
            else:
                self.canvas._commitPatch(patch); self.backend.drawPatch(eventDc, patch);
    # }}}
    # {{{ dispatchPatch(self, eventDc, isCursor, patch)
    def dispatchPatch(self, eventDc, isCursor, patch):
        self.canvas.dispatchPatch(isCursor, patch, False if isCursor else True)
        self._drawPatch(eventDc, isCursor, patch)
    # }}}
    # {{{ resize(self, newSize, commitUndo=True)
    def resize(self, newSize, commitUndo=True):
        oldSize = [0, 0] if self.canvas.map == None else self.canvas.size
        deltaSize = [b - a for a, b in zip(oldSize, newSize)]
        if self.canvas.resize(newSize, commitUndo):
            newWinSize = [a * b for a, b in zip(newSize, self.backend.cellSize)]
            self.SetMinSize(newWinSize); self.SetSize(wx.DefaultCoord, wx.DefaultCoord, *newWinSize);
            curWindow = self
            while curWindow != None:
                curWindow.Layout(); curWindow = curWindow.GetParent();
            self.backend.resize(newSize, self.backend.cellSize)
            eventDc = self.backend.getDeviceContext(self)
            if deltaSize[0] > 0:
                for numRow in range(oldSize[1]):
                    for numNewCol in range(oldSize[0], newSize[0]):
                        self._drawPatch(eventDc, False, [numNewCol, numRow, 1, 1, 0, " "])
            if deltaSize[1] > 1:
                for numNewRow in range(oldSize[1], newSize[1]):
                    for numNewCol in range(newSize[0]):
                        self._drawPatch(eventDc, False, [numNewCol, numNewRow, 1, 1, 0, " "])
            del eventDc; wx.SafeYield();
            self.interface.update(size=newSize, undoLevel=self.canvas.journal.patchesUndoLevel)
    # }}}
    # {{{ update(self, newSize, commitUndo=True, newCanvas=None)
    def update(self, newSize, commitUndo=True, newCanvas=None):
        self.resize(newSize, commitUndo)
        self.canvas.update(newSize, newCanvas)
        eventDc = self.backend.getDeviceContext(self)
        for numRow in range(newSize[1]):
            for numCol in range(newSize[0]):
                self.backend.drawPatch(eventDc, [numCol, numRow, *self.canvas.map[numRow][numCol]])
        wx.SafeYield()
    # }}}

    # {{{ onPanelClose(self, event)
    def onPanelClose(self, event):
        self.Destroy()
    # }}}
    # {{{ onPanelEnterWindow(self, event)
    def onPanelEnterWindow(self, event):
        self.parentFrame.SetFocus()
    # }}}
    # {{{ onPanelInput(self, event)
    def onPanelInput(self, event):
        self.canvas.dirtyJournal, self.canvas.dirtyCursor = False, False
        eventDc, eventType, tool = self.backend.getDeviceContext(self), event.GetEventType(), self.interface.currentTool
        if eventType == wx.wxEVT_CHAR:
            mapPoint = self.brushPos
            doSkip = tool.onKeyboardEvent(event, mapPoint, self.brushColours, self.brushSize, chr(event.GetUnicodeKey()), self.dispatchPatch, eventDc)
            if doSkip:
                event.Skip(); return;
        else:
            mapPoint = self.backend.xlateEventPoint(event, eventDc)
            if mapPoint[0] >= self.canvas.size[0]                           \
            or mapPoint[1] >= self.canvas.size[1]:
                return
            self.brushPos = mapPoint
            tool.onMouseEvent(                                              \
                event, mapPoint, self.brushColours, self.brushSize,         \
                event.Dragging(), event.LeftIsDown(), event.RightIsDown(),  \
                self.dispatchPatch, eventDc)
        if self.canvas.dirtyJournal:
            self.dirty = True
            self.interface.update(dirty=self.dirty, cellPos=self.brushPos, undoLevel=self.canvas.journal.patchesUndoLevel)
        if eventType == wx.wxEVT_MOTION:
            self.interface.update(cellPos=mapPoint)
    # }}}
    # {{{ onPanelLeaveWindow(self, event)
    def onPanelLeaveWindow(self, event):
        eventDc = self.backend.getDeviceContext(self)
        self.backend.drawCursorMaskWithJournal(self.canvas.journal, eventDc)
    # }}}
    # {{{ onPanelPaint(self, event)
    def onPanelPaint(self, event):
        self.backend.onPanelPaintEvent(event, self)
    # }}}

    #
    # __init__(self, parent, parentFrame, backend, canvas, defaultCanvasPos, defaultCanvasSize, defaultCellSize, interface): initialisation method
    def __init__(self, parent, parentFrame, backend, canvas, defaultCanvasPos, defaultCanvasSize, defaultCellSize, interface):
        super().__init__(parent, pos=defaultCanvasPos, size=[w * h for w, h in zip(defaultCanvasSize, defaultCellSize)])
        self.backend, self.interface = backend(defaultCanvasSize, defaultCellSize), interface(self, parentFrame)
        self.brushColours, self.brushPos, self.brushSize = [4, 1], [0, 0], [1, 1]
        self.canvas, self.canvasPos, self.defaultCanvasPos, self.defaultCanvasSize, self.defaultCellSize = canvas, defaultCanvasPos, defaultCanvasPos, defaultCanvasSize, defaultCellSize
        self.dirty, self.parentFrame = False, parentFrame

        self.Bind(wx.EVT_CLOSE, self.onPanelClose)
        self.Bind(wx.EVT_ENTER_WINDOW, self.onPanelEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onPanelLeaveWindow)
        self.parentFrame.Bind(wx.EVT_CHAR, self.onPanelInput)
        for eventType in (wx.EVT_LEFT_DOWN, wx.EVT_MOTION, wx.EVT_RIGHT_DOWN):
            self.Bind(eventType, self.onPanelInput)
        self.Bind(wx.EVT_PAINT, self.onPanelPaint)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
