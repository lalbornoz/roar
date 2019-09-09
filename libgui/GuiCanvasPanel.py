#!/usr/bin/env python3
#
# GuiCanvasPanel.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import wx

class GuiCanvasPanel(wx.ScrolledWindow):
    # {{{ _drawPatch(self, eventDc, isCursor, patch, viewRect)
    def _drawPatch(self, eventDc, isCursor, patch, viewRect):
        if not self.canvas.dirtyCursor:
            self.backend.drawCursorMaskWithJournal(self.canvas.journal, eventDc, viewRect)
            self.canvas.dirtyCursor = True
        if self.backend.drawPatch(eventDc, patch, viewRect) and isCursor:
            patchDeltaCell = self.canvas.map[patch[1]][patch[0]]; patchDelta = [*patch[0:2], *patchDeltaCell];
            self.canvas.journal.pushCursor(patchDelta)
    # }}}
    # {{{ _updateScrollBars(self)
    def _updateScrollBars(self):
        clientSize = self.GetClientSize()
        if   (self.winSize[0] > clientSize[0])      \
        or   (self.winSize[1] > clientSize[1]):
            self.scrollFlag = True; super().SetVirtualSize(self.winSize);
        elif self.scrollFlag                        \
        and  ((self.winSize[0] <= clientSize[0])    \
        or    (self.winSize[1] <= clientSize[1])):
            self.scrollFlag = False; super().SetVirtualSize((0, 0));
    # }}}

    # {{{ applyTool(self, eventDc, eventType, keyChar, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, tool, viewRect)
    def applyTool(self, eventDc, eventType, keyChar, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, tool, viewRect):
        dirty, self.canvas.dirtyCursor, rc = False, False, False
        self.canvas.journal.begin()
        if eventType == wx.wxEVT_CHAR:
            rc, dirty = tool.onKeyboardEvent(self.brushColours, self.brushSize, self.dispatchPatchSingle, eventDc, keyChar, keyModifiers, self.brushPos, viewRect)
        else:
            if  (mapPoint[0] < self.canvas.size[0]) \
            and (mapPoint[1] < self.canvas.size[1]):
                self.brushPos = mapPoint
                rc, dirty = tool.onMouseEvent(self.brushColours, self.brushSize, self.dispatchPatchSingle, eventDc, self.brushPos, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
        if dirty:
            self.dirty = True
            self.interface.update(dirty=self.dirty, cellPos=self.brushPos, undoLevel=self.canvas.journal.patchesUndoLevel)
        self.canvas.journal.end()
        if eventType == wx.wxEVT_MOTION:
            self.interface.update(cellPos=mapPoint)
        return rc
    # }}}
    # {{{ dispatchDeltaPatches(self, deltaPatches)
    def dispatchDeltaPatches(self, deltaPatches):
        eventDc = self.backend.getDeviceContext(self, self.GetViewStart())
        for patch in deltaPatches:
            if patch == None:
                continue
            elif patch[0] == "resize":
                del eventDc; self.resize(patch[1:], False); eventDc = self.backend.getDeviceContext(self, self.GetViewStart());
            else:
                self.canvas._commitPatch(patch); self.backend.drawPatch(eventDc, patch, self.GetViewStart());
    # }}}
    # {{{ dispatchPatch(self, eventDc, isCursor, patch, viewRect)
    def dispatchPatch(self, eventDc, isCursor, patch, viewRect):
        if self.canvas.dispatchPatch(isCursor, patch, False if isCursor else True):
            self._drawPatch(eventDc, isCursor, patch, viewRect)
    # }}}
    # {{{ dispatchPatchSingle(self, eventDc, isCursor, patch, viewRect)
    def dispatchPatchSingle(self, eventDc, isCursor, patch, viewRect):
        if self.canvas.dispatchPatchSingle(isCursor, patch, False if isCursor else True):
            self._drawPatch(eventDc, isCursor, patch, viewRect)
    # }}}
    # {{{ resize(self, newSize, commitUndo=True)
    def resize(self, newSize, commitUndo=True):
        oldSize = [0, 0] if self.canvas.map == None else self.canvas.size
        deltaSize = [b - a for a, b in zip(oldSize, newSize)]
        if self.canvas.resize(newSize, commitUndo):
            self.winSize = [a * b for a, b in zip(newSize, self.backend.cellSize)]; self._updateScrollBars();
            self.SetMinSize(self.winSize); self.SetSize(wx.DefaultCoord, wx.DefaultCoord, *self.winSize);
            curWindow = self
            while curWindow != None:
                curWindow.Layout(); curWindow = curWindow.GetParent();
            self.backend.resize(newSize, self.backend.cellSize)
            viewRect = self.GetViewStart(); eventDc = self.backend.getDeviceContext(self, viewRect);
            if deltaSize[0] > 0:
                for numRow in range(oldSize[1]):
                    for numNewCol in range(oldSize[0], newSize[0]):
                        self._drawPatch(eventDc, False, [numNewCol, numRow, 1, 1, 0, " "], viewRect)
            if deltaSize[1] > 1:
                for numNewRow in range(oldSize[1], newSize[1]):
                    for numNewCol in range(newSize[0]):
                        self._drawPatch(eventDc, False, [numNewCol, numNewRow, 1, 1, 0, " "], viewRect)
            self.interface.update(size=newSize, undoLevel=self.canvas.journal.patchesUndoLevel)
    # }}}
    # {{{ update(self, newSize, commitUndo=True, newCanvas=None)
    def update(self, newSize, commitUndo=True, newCanvas=None):
        self.resize(newSize, commitUndo)
        self.canvas.update(newSize, newCanvas)
        eventDc = self.backend.getDeviceContext(self, self.GetViewStart())
        for numRow in range(newSize[1]):
            for numCol in range(newSize[0]):
                self.backend.drawPatch(eventDc, [numCol, numRow, *self.canvas.map[numRow][numCol]], self.GetViewStart())
    # }}}

    # {{{ onPanelClose(self, event)
    def onPanelClose(self, event):
        self.Destroy()
    # }}}
    # {{{ onPanelInput(self, event)
    def onPanelInput(self, event):
        eventType, viewRect = event.GetEventType(), self.GetViewStart()
        eventDc = self.backend.getDeviceContext(self, viewRect)
        if eventType == wx.wxEVT_CHAR:
            keyChar, keyModifiers = chr(event.GetUnicodeKey()), event.GetModifiers()
            mapPoint, mouseDragging, mouseLeftDown, mouseRightDown = None, None, None, None
        else:
            keyChar, keyModifiers = None, None
            mouseDragging, mouseLeftDown, mouseRightDown = event.Dragging(), event.LeftIsDown(), event.RightIsDown()
            mapPoint = self.backend.xlateEventPoint(event, eventDc, viewRect)
        if not self.applyTool(eventDc, eventType, keyChar, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, self.interface.currentTool, self.GetViewStart()):
            event.Skip()
    # }}}
    # {{{ onPanelLeaveWindow(self, event)
    def onPanelLeaveWindow(self, event):
        eventDc = self.backend.getDeviceContext(self, self.GetViewStart())
        self.backend.drawCursorMaskWithJournal(self.canvas.journal, eventDc, self.GetViewStart())
    # }}}
    # {{{ onPanelPaint(self, event)
    def onPanelPaint(self, event):
        self.backend.onPanelPaintEvent(self.canvas.size, self.defaultCellSize, self.GetClientSize(), self, self.GetViewStart())
    # }}}
    # {{{ onPanelSize(self, event)
    def onPanelSize(self, event):
        self._updateScrollBars(); event.Skip();
    # }}}

    #
    # __init__(self, parent, parentFrame, backend, canvas, defaultCanvasPos, defaultCanvasSize, defaultCellSize, interface): initialisation method
    def __init__(self, parent, parentFrame, backend, canvas, defaultCanvasPos, defaultCanvasSize, defaultCellSize, interface):
        self.winSize = [w * h for w, h in zip(defaultCanvasSize, defaultCellSize)]
        super().__init__(parent, pos=defaultCanvasPos, size=self.winSize)
        self.backend, self.interface = backend(defaultCanvasSize, defaultCellSize), interface(self, parentFrame)
        self.brushColours, self.brushPos, self.brushSize = [4, 1], [0, 0], [1, 1]
        self.canvas, self.canvasPos, self.defaultCanvasPos, self.defaultCanvasSize, self.defaultCellSize = canvas, defaultCanvasPos, defaultCanvasPos, defaultCanvasSize, defaultCellSize
        self.dirty, self.parentFrame, self.scrollFlag = False, parentFrame, False
        self.SetScrollRate(*defaultCellSize); self._updateScrollBars();

        self.Bind(wx.EVT_CLOSE, self.onPanelClose)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onPanelLeaveWindow)
        self.Bind(wx.EVT_CHAR, self.onPanelInput)
        for eventType in (wx.EVT_LEFT_DOWN, wx.EVT_MOTION, wx.EVT_RIGHT_DOWN):
            self.Bind(eventType, self.onPanelInput)
        self.Bind(wx.EVT_PAINT, self.onPanelPaint)
        self.Bind(wx.EVT_SIZE, self.onPanelSize)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
