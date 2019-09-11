#!/usr/bin/env python3
#
# RoarCanvasWindow.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiWindow import GuiWindow

class RoarCanvasWindow(GuiWindow):
    # {{{ _drawPatch(self, eventDc, isCursor, patch, viewRect)
    def _drawPatch(self, eventDc, isCursor, patch, viewRect):
        if not self.canvas.dirtyCursor:
            self.backend.drawCursorMaskWithJournal(self.canvas.journal, eventDc, viewRect)
            self.canvas.dirtyCursor = True
        if self.backend.drawPatch(eventDc, patch, viewRect) and isCursor:
            patchDeltaCell = self.canvas.map[patch[1]][patch[0]]; patchDelta = [*patch[0:2], *patchDeltaCell];
            self.canvas.journal.pushCursor(patchDelta)
    # }}}

    # {{{ applyTool(self, eventDc, eventMouse, keyChar, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, tool, viewRect)
    def applyTool(self, eventDc, eventMouse, keyChar, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, tool, viewRect):
        dirty, self.canvas.dirtyCursor, rc = False, False, False
        self.canvas.journal.begin()
        if eventMouse:
            if  (mapPoint[0] < self.canvas.size[0]) \
            and (mapPoint[1] < self.canvas.size[1]):
                self.brushPos = mapPoint
                rc, dirty = tool.onMouseEvent(self.brushColours, self.brushSize, self.canvas, self.dispatchPatchSingle, eventDc, self.brushPos, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
        else:
            rc, dirty = tool.onKeyboardEvent(self.brushColours, self.brushSize, self.canvas, self.dispatchPatchSingle, eventDc, keyChar, keyModifiers, self.brushPos, viewRect)
        if dirty:
            self.dirty = True
            self.commands.update(dirty=self.dirty, cellPos=self.brushPos, undoLevel=self.canvas.journal.patchesUndoLevel)
        else:
            self.commands.update(cellPos=mapPoint if mapPoint else self.brushPos)
        self.canvas.journal.end()
        return rc
    # }}}
    # {{{ dispatchDeltaPatches(self, deltaPatches)
    def dispatchDeltaPatches(self, deltaPatches):
        eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, self.GetViewStart())
        for patch in deltaPatches:
            if patch == None:
                continue
            elif patch[0] == "resize":
                del eventDc; self.resize(patch[1:], False); eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, self.GetViewStart());
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
            super().resize([a * b for a, b in zip(newSize, self.backend.cellSize)])
            self.backend.resize(newSize, self.backend.cellSize)
            viewRect = self.GetViewStart(); eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, viewRect);
            if deltaSize[0] > 0:
                for numRow in range(oldSize[1]):
                    for numNewCol in range(oldSize[0], newSize[0]):
                        self._drawPatch(eventDc, False, [numNewCol, numRow, 1, 1, 0, " "], viewRect)
            if deltaSize[1] > 1:
                for numNewRow in range(oldSize[1], newSize[1]):
                    for numNewCol in range(newSize[0]):
                        self._drawPatch(eventDc, False, [numNewCol, numNewRow, 1, 1, 0, " "], viewRect)
            self.commands.update(size=newSize, undoLevel=self.canvas.journal.patchesUndoLevel)
    # }}}
    # {{{ update(self, newSize, commitUndo=True, newCanvas=None)
    def update(self, newSize, commitUndo=True, newCanvas=None):
        self.resize(newSize, commitUndo)
        self.canvas.update(newSize, newCanvas)
        eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, self.GetViewStart())
        for numRow in range(newSize[1]):
            for numCol in range(newSize[0]):
                self.backend.drawPatch(eventDc, [numCol, numRow, *self.canvas.map[numRow][numCol]], self.GetViewStart())
    # }}}

    # {{{ onKeyboardInput(self, event)
    def onKeyboardInput(self, event):
        viewRect = self.GetViewStart(); eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, viewRect);
        keyChar, keyModifiers = chr(event.GetUnicodeKey()), event.GetModifiers()
        if not self.applyTool(eventDc, False, keyChar, keyModifiers, None, None, None, None, self.commands.currentTool, viewRect):
            event.Skip()
    # }}}
    # {{{ onLeaveWindow(self, event)
    def onLeaveWindow(self, event):
        eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, self.GetViewStart())
        self.backend.drawCursorMaskWithJournal(self.canvas.journal, eventDc, self.GetViewStart())
    # }}}
    # {{{ onMouseInput(self, event)
    def onMouseInput(self, event):
        viewRect = self.GetViewStart(); eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, viewRect);
        mouseDragging, mouseLeftDown, mouseRightDown = event.Dragging(), event.LeftIsDown(), event.RightIsDown()
        mapPoint = self.backend.xlateEventPoint(event, eventDc, viewRect)
        if not self.applyTool(eventDc, True, None, None, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, self.commands.currentTool, viewRect):
            event.Skip()
    # }}}
    # {{{ onPaint(self, event)
    def onPaint(self, event):
        self.backend.onPaint(self.GetClientSize(), self, self.GetViewStart())
    # }}}
    # {{{ onScroll(self, event)
    def onScroll(self, event):
        if self.canvas.dirtyCursor:
            viewRect = self.GetViewStart()
            eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, viewRect)
            self.backend.drawCursorMaskWithJournal(self.canvas.journal, eventDc, viewRect)
            self.canvas.dirtyCursor = False
        event.Skip()
    # }}}

    #
    # __init__(self, backend, canvas, cellSize, commands, parent, parentFrame, pos, scrollStep, size): initialisation method
    def __init__(self, backend, canvas, cellSize, commands, parent, parentFrame, pos, scrollStep, size):
        super().__init__(parent, pos, scrollStep, [w * h for w, h in zip(cellSize, size)])
        self.backend, self.canvas, self.cellSize, self.commands, self.parentFrame = backend(self.size, cellSize), canvas, cellSize, commands(self, parentFrame), parentFrame
        self.brushColours, self.brushPos, self.brushSize, self.dirty = [4, 1], [0, 0], [1, 1], False

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
