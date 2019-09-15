#!/usr/bin/env python3
#
# RoarCanvasWindow.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiWindow import GuiWindow
from ToolObject import ToolObject
import json, wx, sys
import time

class RoarCanvasWindowDropTarget(wx.TextDropTarget):
    # {{{ done(self)
    def done(self):
        self.inProgress = False
    # }}}
    # {{{ OnDropText(self, x, y, data)
    def OnDropText(self, x, y, data):
        rc = False
        if not self.inProgress:
            try:
                dropMap, dropSize = json.loads(data)
                viewRect = self.parent.GetViewStart()
                rectX, rectY = x - (x % self.parent.backend.cellSize[0]), y - (y % self.parent.backend.cellSize[1])
                mapX, mapY = int(rectX / self.parent.backend.cellSize[0] if rectX else 0), int(rectY / self.parent.backend.cellSize[1] if rectY else 0)
                mapPoint = [m + n for m, n in zip((mapX, mapY), viewRect)]
                self.parent.commands.lastTool, self.parent.commands.currentTool = self.parent.commands.currentTool, ToolObject()
                self.parent.commands.currentTool.setRegion(self.parent.canvas, mapPoint, dropMap, dropSize, external=True)
                self.parent.commands.update(toolName=self.parent.commands.currentTool.name)
                eventDc = self.parent.backend.getDeviceContext(self.parent.GetClientSize(), self.parent, viewRect)
                self.parent.applyTool(eventDc, True, None, None, self.parent.brushPos, False, False, False, self.parent.commands.currentTool, viewRect)
                rc = True; self.inProgress = True;
            except:
                with wx.MessageDialog(self.parent, "Error: {}".format(sys.exc_info()[1]), "", wx.OK | wx.OK_DEFAULT) as dialog:
                    dialogChoice = dialog.ShowModal()
        return rc
    # }}}
    # {{{ __init__(self, parent)
    def __init__(self, parent):
        super().__init__(); self.inProgress, self.parent = False, parent;
    # }}}

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
        if mapPoint != None:
            mapPoint = [a + b for a, b in zip(mapPoint, viewRect)]
        dirty, self.canvas.dirtyCursor, rc = False, False, False
        self.canvas.journal.begin()
        if eventMouse:
            if  ((mapPoint[0] < self.canvas.size[0])    \
            and  (mapPoint[1] < self.canvas.size[1]))   \
            and ((self.lastCellState == None)           \
            or   (self.lastCellState != [list(mapPoint), mouseDragging, mouseLeftDown, mouseRightDown, list(viewRect)])):
                self.brushPos = list(mapPoint)
                self.lastCellState = [list(mapPoint), mouseDragging, mouseLeftDown, mouseRightDown, list(viewRect)]
                rc, dirty = tool.onMouseEvent(self.brushColours, self.brushSize, self.canvas, self.dispatchPatchSingle, eventDc, keyModifiers, self.brushPos, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
        else:
            rc, dirty = tool.onKeyboardEvent(self.brushColours, self.brushSize, self.canvas, self.dispatchPatchSingle, eventDc, keyChar, keyModifiers, self.brushPos, viewRect)
        if dirty:
            self.dirty = True
            self.commands.update(dirty=self.dirty, cellPos=self.brushPos, undoLevel=self.canvas.journal.patchesUndoLevel)
        else:
            self.commands.update(cellPos=mapPoint if mapPoint else self.brushPos)
        self.canvas.journal.end()
        if  rc and (tool.__class__ == ToolObject)       \
        and (tool.toolState == tool.TS_NONE)            \
        and tool.external:
            self.commands.currentTool, self.commands.lastTool = self.commands.lastTool, self.commands.currentTool
            self.commands.update(toolName=self.commands.currentTool.name)
            self.dropTarget.done()
        return rc
    # }}}
    # {{{ dispatchDeltaPatches(self, deltaPatches)
    def dispatchDeltaPatches(self, deltaPatches):
        viewRect = self.GetViewStart()
        eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, viewRect)
        if self.canvas.dirtyCursor:
            self.backend.drawCursorMaskWithJournal(self.canvas.journal, eventDc, viewRect)
            self.canvas.dirtyCursor = False
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
        if  (event.GetKeyCode() == wx.WXK_PAUSE)    \
        and (event.GetModifiers() == wx.MOD_SHIFT):
            import pdb; pdb.set_trace()
        else:
            viewRect = self.GetViewStart(); eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, viewRect);
            keyChar, keyModifiers = chr(event.GetUnicodeKey()), event.GetModifiers()
            if not self.applyTool(eventDc, False, keyChar, keyModifiers, None, None, None, None, self.commands.currentTool, viewRect):
                event.Skip()
    # }}}
    # {{{ onEnterWindow(self, event)
    def onEnterWindow(self, event):
        self.lastCellState = None
    # }}}
    # {{{ onLeaveWindow(self, event)
    def onLeaveWindow(self, event):
        if False:
            eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, self.GetViewStart())
            self.backend.drawCursorMaskWithJournal(self.canvas.journal, eventDc, self.GetViewStart())
        self.lastCellState = None
    # }}}
    # {{{ onMouseInput(self, event)
    def onMouseInput(self, event):
        viewRect = self.GetViewStart(); eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, viewRect);
        mouseDragging, mouseLeftDown, mouseRightDown = event.Dragging(), event.LeftIsDown(), event.RightIsDown()
        mapPoint = self.backend.xlateEventPoint(event, eventDc, viewRect)
        if  mouseRightDown                                      \
        and (self.commands.currentTool.__class__ == ToolObject) \
        and (self.commands.currentTool.toolState >= self.commands.currentTool.TS_SELECT):
            self.popupEventDc = eventDc; self.PopupMenu(self.operatorsMenu); self.popupEventDc = None;
        elif not self.applyTool(eventDc, True, None, event.GetModifiers(), mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, self.commands.currentTool, viewRect):
            event.Skip()
    # }}}
    # {{{ onMouseWheel(self, event)
    def onMouseWheel(self, event):
        if event.GetModifiers() == wx.MOD_CONTROL:
            cd = +1 if event.GetWheelRotation() >= event.GetWheelDelta() else -1
            newCellSize = [cs + cd for cs in self.backend.cellSize]
            if (newCellSize[0] > 0) and (newCellSize[1] > 0):
                self.backend.cellSize = newCellSize
                super().resize([a * b for a, b in zip(self.canvas.size, self.backend.cellSize)])
                self.backend.resize(self.canvas.size, self.backend.cellSize)
                viewRect = self.GetViewStart(); eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, viewRect);
                for numRow in range(self.canvas.size[1]):
                    for numCol in range(len(self.canvas.map[numRow])):
                        self._drawPatch(eventDc, False, [numCol, numRow, *self.canvas.map[numRow][numCol]], viewRect)
        else:
            event.Skip()
    # }}}
    # {{{ onPaint(self, event)
    def onPaint(self, event):
        viewRect = self.GetViewStart()
        eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, viewRect)
        self.backend.drawCursorMaskWithJournal(self.canvas.journal, eventDc, viewRect)
        self.backend.onPaint(self.GetClientSize(), self, self.GetViewStart())
    # }}}

    #
    # __init__(self, backend, canvas, cellSize, commands, parent, parentFrame, pos, scrollStep, size): initialisation method
    def __init__(self, backend, canvas, cellSize, commands, parent, parentFrame, pos, scrollStep, size):
        super().__init__(parent, pos, scrollStep, [w * h for w, h in zip(cellSize, size)])
        self.backend, self.canvas, self.cellSize, self.commands, self.parentFrame = backend(self.size, cellSize), canvas, cellSize, commands(self, parentFrame), parentFrame
        self.brushColours, self.brushPos, self.brushSize, self.dirty, self.lastCellState = [4, 1], [0, 0], [1, 1], False, None
        self.popupEventDc = None
        self.dropTarget = RoarCanvasWindowDropTarget(self)
        self.SetDropTarget(self.dropTarget)
        self.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
