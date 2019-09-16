#!/usr/bin/env python3
#
# RoarCanvasWindow.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiWindow import GuiWindow
from ToolObject import ToolObject
from ToolText import ToolText
import json, wx, sys

class RoarCanvasWindowDropTarget(wx.TextDropTarget):
    # {{{ done(self)
    def done(self):
        self.inProgress = False
    # }}}
    # {{{ OnDropText(self, x, y, data)
    def OnDropText(self, x, y, data):
        rc = False
        if  ((self.parent.commands.currentTool.__class__ != ToolObject)                                 \
        or   (self.parent.commands.currentTool.toolState == self.parent.commands.currentTool.TS_NONE))  \
        and (not self.inProgress):
            try:
                dropMap, dropSize = json.loads(data)
                rectX, rectY = x - (x % self.parent.backend.cellSize[0]), y - (y % self.parent.backend.cellSize[1])
                mapX, mapY = int(rectX / self.parent.backend.cellSize[0] if rectX else 0), int(rectY / self.parent.backend.cellSize[1] if rectY else 0)
                viewRect = self.parent.GetViewStart(); mapPoint = [m + n for m, n in zip((mapX, mapY), viewRect)];
                self.parent.commands.lastTool, self.parent.commands.currentTool = self.parent.commands.currentTool, ToolObject()
                self.parent.commands.currentTool.setRegion(self.parent.canvas, mapPoint, dropMap, dropSize, external=True)
                self.parent.commands.update(toolName=self.parent.commands.currentTool.name)
                eventDc = self.parent.backend.getDeviceContext(self.parent.GetClientSize(), self.parent, viewRect)
                eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
                self.parent.applyTool(eventDc, True, None, None, None, self.parent.brushPos, False, False, False, self.parent.commands.currentTool, viewRect)
                eventDc.SetDeviceOrigin(*eventDcOrigin)
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
    # {{{ _drawPatch(self, eventDc, isCursor, patch)
    def _drawPatch(self, eventDc, isCursor, patch):
        if not self.canvas.dirtyCursor:
            self.backend.drawCursorMaskWithJournal(self.canvas, self.canvas.journal, eventDc)
            self.canvas.dirtyCursor = True
        if self.backend.drawPatch(self.canvas, eventDc, patch) and isCursor:
            patchDeltaCell = self.canvas.map[patch[1]][patch[0]]; patchDelta = [*patch[0:2], *patchDeltaCell];
            self.canvas.journal.pushCursor(patchDelta)
    # }}}

    # {{{ applyTool(self, eventDc, eventMouse, keyChar, keyCode, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, tool, viewRect)
    def applyTool(self, eventDc, eventMouse, keyChar, keyCode, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, tool, viewRect):
        eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
        if mapPoint != None:
            mapPoint = [a + b for a, b in zip(mapPoint, viewRect)]
        dirty, self.canvas.dirtyCursor, rc = False, False, False
        self.canvas.journal.begin()
        if eventMouse:
            if  ((mapPoint[0] < self.canvas.size[0])    \
            and  (mapPoint[1] < self.canvas.size[1]))   \
            and ((self.lastCellState == None)           \
            or   (self.lastCellState != [list(mapPoint), mouseDragging, mouseLeftDown, mouseRightDown, list(viewRect)])):
                if tool.__class__ != ToolText:
                    self.brushPos = list(mapPoint)
                if tool != None:
                    rc, dirty = tool.onMouseEvent(mapPoint, self.brushColours, self.brushPos, self.brushSize, self.canvas, self.dispatchPatchSingle, eventDc, keyModifiers, self.brushPos, mouseDragging, mouseLeftDown, mouseRightDown)
                else:
                    self.dispatchPatchSingle(eventDc, True, [*mapPoint, self.brushColours[0], self.brushColours[0], 0, " "])
                self.lastCellState = [list(mapPoint), mouseDragging, mouseLeftDown, mouseRightDown, list(viewRect)]
        else:
            if tool != None:
                rc, dirty = tool.onKeyboardEvent(mapPoint, self.brushColours, self.brushPos, self.brushSize, self.canvas, self.dispatchPatchSingle, eventDc, keyChar, keyCode, keyModifiers, self.brushPos)
            elif mapPoint != None:
                self.dispatchPatchSingle(eventDc, True, [*mapPoint, self.brushColours[0], self.brushColours[0], 0, " "])
        if dirty:
            self.dirty = True
            self.commands.update(dirty=self.dirty, cellPos=self.brushPos, undoLevel=self.canvas.journal.patchesUndoLevel)
        else:
            self.commands.update(cellPos=self.brushPos)
        self.canvas.journal.end()
        if rc and (tool.__class__ == ToolObject):
            if tool.toolState > tool.TS_NONE:
                self.commands.update(undoInhibit=True)
            elif tool.toolState == tool.TS_NONE:
                if tool.external:
                    self.dropTarget.done()
                    self.commands.currentTool, self.commands.lastTool = self.commands.lastTool, self.commands.currentTool
                    if self.commands.currentTool != None:
                        self.commands.update(toolName=self.commands.currentTool.name, undoInhibit=False)
                    else:
                        self.commands.update(toolName="Cursor", undoInhibit=False)
                else:
                    self.commands.update(undoInhibit=False)
        eventDc.SetDeviceOrigin(*eventDcOrigin)
        return rc
    # }}}
    # {{{ dispatchDeltaPatches(self, deltaPatches)
    def dispatchDeltaPatches(self, deltaPatches):
        eventDc = self.backend.getDeviceContext(self.GetClientSize(), self)
        eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
        if self.canvas.dirtyCursor:
            self.backend.drawCursorMaskWithJournal(self.canvas, self.canvas.journal, eventDc)
            self.canvas.dirtyCursor = False
        for patch in deltaPatches:
            if patch == None:
                continue
            elif patch[0] == "resize":
                del eventDc; self.resize(patch[1:], False);
                eventDc = self.backend.getDeviceContext(self.GetClientSize(), self)
                eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
            else:
                self.canvas._commitPatch(patch); self.backend.drawPatch(self.canvas, eventDc, patch)
        eventDc.SetDeviceOrigin(*eventDcOrigin)
    # }}}
    # {{{ dispatchPatch(self, eventDc, isCursor, patch)
    def dispatchPatch(self, eventDc, isCursor, patch):
        if self.canvas.dispatchPatch(isCursor, patch, False if isCursor else True):
            self._drawPatch(eventDc, isCursor, patch)
    # }}}
    # {{{ dispatchPatchSingle(self, eventDc, isCursor, patch)
    def dispatchPatchSingle(self, eventDc, isCursor, patch):
        if self.canvas.dispatchPatchSingle(isCursor, patch, False if isCursor else True):
            self._drawPatch(eventDc, isCursor, patch)
    # }}}
    # {{{ resize(self, newSize, commitUndo=True)
    def resize(self, newSize, commitUndo=True):
        oldSize = [0, 0] if self.canvas.map == None else self.canvas.size
        deltaSize = [b - a for a, b in zip(oldSize, newSize)]
        if self.canvas.resize(newSize, commitUndo):
            super().resize([a * b for a, b in zip(newSize, self.backend.cellSize)])
            self.backend.resize(newSize, self.backend.cellSize)
            eventDc = self.backend.getDeviceContext(self.GetClientSize(), self)
            eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
            if deltaSize[0] > 0:
                for numRow in range(oldSize[1]):
                    for numNewCol in range(oldSize[0], newSize[0]):
                        self._drawPatch(eventDc, False, [numNewCol, numRow, 1, 1, 0, " "])
            if deltaSize[1] > 1:
                for numNewRow in range(oldSize[1], newSize[1]):
                    for numNewCol in range(newSize[0]):
                        self._drawPatch(eventDc, False, [numNewCol, numNewRow, 1, 1, 0, " "])
            eventDc.SetDeviceOrigin(*eventDcOrigin) 
            self.commands.update(size=newSize, undoLevel=self.canvas.journal.patchesUndoLevel)
    # }}}
    # {{{ update(self, newSize, commitUndo=True, newCanvas=None)
    def update(self, newSize, commitUndo=True, newCanvas=None):
        self.resize(newSize, commitUndo)
        self.canvas.update(newSize, newCanvas)
        eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, self.GetViewStart())
        eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
        for numRow in range(newSize[1]):
            for numCol in range(newSize[0]):
                self.backend.drawPatch(self.canvas, eventDc, [numCol, numRow, *self.canvas.map[numRow][numCol]])
        eventDc.SetDeviceOrigin(*eventDcOrigin)
    # }}}

    # {{{ onKeyboardInput(self, event)
    def onKeyboardInput(self, event):
        keyCode, keyModifiers = event.GetKeyCode(), event.GetModifiers()
        viewRect = self.GetViewStart(); eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, viewRect);
        if  (keyCode == wx.WXK_PAUSE)   \
        and (keyModifiers == wx.MOD_SHIFT):
            import pdb; pdb.set_trace()
        elif keyCode in (wx.WXK_DOWN, wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_UP):
            if keyCode == wx.WXK_DOWN:
                if self.brushPos[1] < (self.canvas.size[1] - 1):
                    self.brushPos = [self.brushPos[0], self.brushPos[1] + 1]
                else:
                    self.brushPos = [self.brushPos[0], 0]
            elif keyCode == wx.WXK_LEFT:
                if self.brushPos[0] > 0:
                    self.brushPos = [self.brushPos[0] - 1, self.brushPos[1]]
                else:
                    self.brushPos = [self.canvas.size[0] - 1, self.brushPos[1]]
            elif keyCode == wx.WXK_RIGHT:
                if self.brushPos[0] < (self.canvas.size[0] - 1):
                    self.brushPos = [self.brushPos[0] + 1, self.brushPos[1]]
                else:
                    self.brushPos = [0, self.brushPos[1]]
            elif keyCode == wx.WXK_UP:
                if self.brushPos[1] > 0:
                    self.brushPos = [self.brushPos[0], self.brushPos[1] - 1]
                else:
                    self.brushPos = [self.brushPos[0], self.canvas.size[1] - 1]
            self.commands.update(cellPos=self.brushPos)
            self.applyTool(eventDc, True, None, None, None, self.brushPos, False, False, False, self.commands.currentTool, viewRect)
        else:
            if not self.applyTool(eventDc, False, chr(event.GetUnicodeKey()), keyCode, keyModifiers, None, None, None, None, self.commands.currentTool, viewRect):
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
            eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
            self.backend.drawCursorMaskWithJournal(self.canvas, self.canvas.journal, eventDc)
            eventDc.SetDeviceOrigin(*eventDcOrigin)
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
        elif not self.applyTool(eventDc, True, None, None, event.GetModifiers(), mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, self.commands.currentTool, viewRect):
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
                eventDc = self.backend.getDeviceContext(self.GetClientSize(), self)
                eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
                for numRow in range(self.canvas.size[1]):
                    for numCol in range(len(self.canvas.map[numRow])):
                        self._drawPatch(eventDc, False, [numCol, numRow, *self.canvas.map[numRow][numCol]])
                eventDc.SetDeviceOrigin(*eventDcOrigin)
        else:
            event.Skip()
    # }}}
    # {{{ onPaint(self, event)
    def onPaint(self, event):
        eventDc = self.backend.getDeviceContext(self.GetClientSize(), self)
        eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
        self.backend.drawCursorMaskWithJournal(self.canvas, self.canvas.journal, eventDc)
        eventDc.SetDeviceOrigin(*eventDcOrigin)
        self.backend.onPaint(self.GetClientSize(), self, self.GetViewStart())
    # }}}

    #
    # __init__(self, backend, canvas, cellSize, commands, parent, parentFrame, pos, scrollStep, size): initialisation method
    def __init__(self, backend, canvas, cellSize, commands, parent, parentFrame, pos, scrollStep, size):
        super().__init__(parent, pos, scrollStep)
        self.size = size
        self.backend, self.canvas, self.cellSize, self.commands, self.parentFrame = backend(self.size, cellSize), canvas, cellSize, commands(self, parentFrame), parentFrame
        self.brushColours, self.brushPos, self.brushSize, self.dirty, self.lastCellState = [4, 1], [0, 0], [1, 1], False, None
        self.popupEventDc = None
        self.dropTarget = RoarCanvasWindowDropTarget(self)
        self.SetDropTarget(self.dropTarget)
        self.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
