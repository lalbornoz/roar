#!/usr/bin/env python3
#
# RoarCanvasWindow.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiWindow import GuiWindow
from ToolObject import ToolObject
from ToolText import ToolText
import copy, json, wx, sys

class RoarCanvasWindowDropTarget(wx.TextDropTarget):
    def done(self):
        self.inProgress = False

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

    def __init__(self, parent):
        super().__init__(); self.inProgress, self.parent = False, parent;

class RoarCanvasWindow(GuiWindow):
    def _applyPatches(self, eventDc, patches, patchesCursor, rc):
        if rc:
            eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
            if ((patches != None) and (len(patches) > 0))   \
            or ((patchesCursor != None) and (len(patchesCursor) > 0)):
                self.backend.drawCursorMaskWithJournal(self.canvas, self.canvas.journal, eventDc)
            if (patches != None) and (len(patches) > 0):
                self.backend.drawPatches(self.canvas, eventDc, patches, isCursor=False)
                self.dirty = True if not self.dirty else self.dirty;
                self.canvas.journal.begin()
                for patch in patches if patches != None else []:
                    self.canvas.applyPatch(patch, commitUndo=True)
                self.canvas.journal.end()
            if patchesCursor != None:
                patchesCursorCells = self.backend.drawPatches(self.canvas, eventDc, patchesCursor, isCursor=True)
                if len(patchesCursorCells) > 0:
                    self.canvas.journal.pushCursor(patchesCursorCells)
            eventDc.SetDeviceOrigin(*eventDcOrigin)
            self.commands.update(dirty=self.dirty, cellPos=self.brushPos, undoLevel=self.canvas.journal.patchesUndoLevel)

    def applyOperator(self, currentTool, mapPoint, mouseLeftDown, mousePoint, operator, viewRect):
        eventDc, patches, patchesCursor, rc = self.backend.getDeviceContext(self.GetClientSize(), self), None, None, True
        if (currentTool.__class__ == ToolObject) and (currentTool.toolState >= currentTool.TS_SELECT):
            region = currentTool.getRegion(self.canvas)
        else:
            region = self.canvas.map
        if hasattr(operator, "apply2"):
            if mouseLeftDown:
                self.commands.operatorState = True if self.commands.operatorState == None else self.commands.operatorState
                region = operator.apply2(mapPoint, mousePoint, region, copy.deepcopy(region))
                self.commands.update(operator=self.commands.currentOperator.name)
            elif self.commands.operatorState != None:
                self.commands.currentOperator = None; self.commands.update(operator=None); rc = False;
        else:
            region = operator.apply(copy.deepcopy(region)); self.commands.currentOperator = None;
        if rc:
            if (currentTool.__class__ == ToolObject) and (currentTool.toolState >= currentTool.TS_SELECT):
                currentTool.setRegion(self.canvas, None, region, [len(region[0]), len(region)], currentTool.external)
                rc, patches, patchesCursor = currentTool.onSelectEvent(self.canvas, (0, 0), True, wx.MOD_NONE, None, currentTool.targetRect)
                patchesCursor = [] if patchesCursor == None else patchesCursor
                patchesCursor += currentTool._drawSelectRect(currentTool.targetRect)
            else:
                patches = []
                for numRow in range(len(region)):
                    for numCol in range(len(region[numRow])):
                        patches += [[numCol, numRow, *region[numRow][numCol]]]
            self._applyPatches(eventDc, patches, patchesCursor, rc)
        return rc

    def applyTool(self, eventDc, eventMouse, keyChar, keyCode, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, tool, viewRect, force=False):
        dirty, patches, patchesCursor, rc = False, None, None, False
        if eventMouse:
            self.lastCellState = None if force else self.lastCellState
            if  ((mapPoint[0] < self.canvas.size[0]) and (mapPoint[1] < self.canvas.size[1]))   \
            and ((self.lastCellState == None) or (self.lastCellState != [list(mapPoint), mouseDragging, mouseLeftDown, mouseRightDown, list(viewRect)])):
                self.brushPos = list(mapPoint) if tool.__class__ != ToolText else self.brushPos
                if tool != None:
                    rc, patches, patchesCursor = tool.onMouseEvent(mapPoint, self.brushColours, self.brushPos, self.brushSize, self.canvas, keyModifiers, self.brushPos, mouseDragging, mouseLeftDown, mouseRightDown)
                else:
                    rc, patches, patchesCursor = True, None, [[*mapPoint, self.brushColours[0], self.brushColours[0], 0, " "]]
                self.lastCellState = [list(mapPoint), mouseDragging, mouseLeftDown, mouseRightDown, list(viewRect)]
        else:
            if tool != None:
                rc, patches, patchesCursor = tool.onKeyboardEvent(mapPoint, self.brushColours, self.brushPos, self.brushSize, self.canvas, keyChar, keyCode, keyModifiers, self.brushPos)
            elif mapPoint != None:
                rc, patches, patchesCursor = True, None, [[*mapPoint, self.brushColours[0], self.brushColours[0], 0, " "]]
        if rc:
            self._applyPatches(eventDc, patches, patchesCursor, rc)
            if tool.__class__ == ToolObject:
                if tool.toolState > tool.TS_NONE:
                    self.commands.update(undoInhibit=True)
                elif tool.toolState == tool.TS_NONE:
                    if tool.external:
                        self.dropTarget.done(); self.commands.currentTool, self.commands.lastTool = self.commands.lastTool, self.commands.currentTool;
                        newToolName = "Cursor" if self.commands.currentTool == None else self.commands.currentTool.name
                        self.commands.update(toolName=newToolName, undoInhibit=False)
                    else:
                        self.commands.update(undoInhibit=False)
        return rc

    def onKeyboardInput(self, event):
        keyCode, keyModifiers = event.GetKeyCode(), event.GetModifiers()
        viewRect = self.GetViewStart(); eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, viewRect);
        if  (keyCode == wx.WXK_PAUSE)               \
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
        elif (chr(event.GetUnicodeKey()) == " ")    \
        and  (self.commands.currentTool.__class__ != ToolText):
            if not self.applyTool(eventDc, True, None, None, event.GetModifiers(), self.brushPos, False, True, False, self.commands.currentTool, viewRect):
                event.Skip()
            else:
                if self.brushPos[0] < (self.canvas.size[0] - 1):
                    self.brushPos = [self.brushPos[0] + 1, self.brushPos[1]]
                else:
                    self.brushPos = [0, self.brushPos[1]]
            self.commands.update(cellPos=self.brushPos)
            self.applyTool(eventDc, True, None, None, None, self.brushPos, False, False, False, self.commands.currentTool, viewRect)
        else:
            if not self.applyTool(eventDc, False, chr(event.GetUnicodeKey()), keyCode, keyModifiers, None, None, None, None, self.commands.currentTool, viewRect):
                event.Skip()

    def onEnterWindow(self, event):
        self.lastCellState = None

    def onLeaveWindow(self, event):
        if False:
            eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, self.GetViewStart())
            self.backend.drawCursorMaskWithJournal(self.canvas, self.canvas.journal, eventDc)
        self.lastCellState = None

    def onMouseInput(self, event):
        viewRect = self.GetViewStart(); eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, viewRect);
        mouseDragging, mouseLeftDown, mouseRightDown = event.Dragging(), event.LeftIsDown(), event.RightIsDown()
        mapPoint = self.backend.xlateEventPoint(event, eventDc, viewRect)
        if viewRect != (0, 0):
            mapPoint = [a + b for a, b in zip(mapPoint, viewRect)]
        if self.commands.currentOperator != None:
            self.applyOperator(self.commands.currentTool, mapPoint, mouseLeftDown, event.GetLogicalPosition(eventDc), self.commands.currentOperator, viewRect)
        elif  mouseRightDown                                    \
        and (self.commands.currentTool.__class__ == ToolObject) \
        and (self.commands.currentTool.toolState >= self.commands.currentTool.TS_SELECT):
            self.popupEventDc = eventDc; self.PopupMenu(self.operatorsMenu); self.popupEventDc = None;
        elif not self.applyTool(eventDc, True, None, None, event.GetModifiers(), mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, self.commands.currentTool, viewRect):
            event.Skip()

    def onMouseWheel(self, event):
        delta, modifiers = +1 if event.GetWheelRotation() >= event.GetWheelDelta() else -1, event.GetModifiers()
        if modifiers == (wx.MOD_CONTROL | wx.MOD_ALT):
            newFontSize = self.backend.fontSize + delta
            if newFontSize > 0:
                self.backend.fontSize = newFontSize
                self.backend.resize(self.canvas.size); self.scrollStep = self.backend.cellSize;
                super().resize([a * b for a, b in zip(self.canvas.size, self.backend.cellSize)])
                eventDc = self.backend.getDeviceContext(self.GetClientSize(), self)
                eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
                patches = []
                for numRow in range(self.canvas.size[1]):
                    for numCol in range(len(self.canvas.map[numRow])):
                        patches += [[numCol, numRow, *self.canvas.map[numRow][numCol]]]
                self.backend.drawPatches(self.canvas, eventDc, patches, isCursor=False)
                eventDc.SetDeviceOrigin(*eventDcOrigin)
        elif modifiers == (wx.MOD_CONTROL | wx.MOD_SHIFT):
            self.commands.canvasCanvasSize(self.commands.canvasCanvasSize, 2, 1 if delta > 0 else 0)(None)
        elif modifiers == wx.MOD_CONTROL:
            self.commands.canvasBrushSize(self.commands.canvasBrushSize, 2, 1 if delta > 0 else 0)(None)
        else:
            event.Skip()

    def onPaint(self, event):
        eventDc = self.backend.getDeviceContext(self.GetClientSize(), self)
        self.backend.onPaint(self.GetClientSize(), self, self.GetViewStart())

    def resize(self, newSize, commitUndo=True, dirty=True):
        viewRect = self.GetViewStart()
        oldSize = [0, 0] if self.canvas.map == None else self.canvas.size
        deltaSize = [b - a for a, b in zip(oldSize, newSize)]
        if self.canvas.resize(newSize, commitUndo):
            self.backend.resize(newSize); self.scrollStep = self.backend.cellSize;
            super().resize([a * b for a, b in zip(newSize, self.backend.cellSize)])
            eventDc = self.backend.getDeviceContext(self.GetClientSize(), self)
            eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
            patches = []
            if deltaSize[0] > 0:
                for numRow in range(oldSize[1]):
                    for numNewCol in range(oldSize[0], newSize[0]):
                        patches += [[numNewCol, numRow, 1, 1, 0, " "]]
            if deltaSize[1] > 1:
                for numNewRow in range(oldSize[1], newSize[1]):
                    for numNewCol in range(newSize[0]):
                        patches += [[numNewCol, numNewRow, 1, 1, 0, " "]]
            self.backend.drawPatches(self.canvas, eventDc, patches, isCursor=False)
            eventDc.SetDeviceOrigin(*eventDcOrigin)
            self.Scroll(*viewRect); self.dirty = dirty;
            self.commands.update(dirty=self.dirty, size=newSize, undoLevel=self.canvas.journal.patchesUndoLevel)

    def undo(self, redo=False):
        deltaPatches = self.canvas.journal.popUndo() if not redo else self.canvas.journal.popRedo()
        eventDc = self.backend.getDeviceContext(self.GetClientSize(), self)
        eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
        self.backend.drawCursorMaskWithJournal(self.canvas, self.canvas.journal, eventDc)
        patches = []
        for patch in deltaPatches:
            if patch == None:
                continue
            elif patch[0] == "resize":
                del eventDc; self.resize(patch[1:], False);
                eventDc = self.backend.getDeviceContext(self.GetClientSize(), self)
                eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
            else:
               self.canvas._commitPatch(patch); patches += [patch];
        self.backend.drawPatches(self.canvas, eventDc, patches, isCursor=False)
        eventDc.SetDeviceOrigin(*eventDcOrigin)

    def update(self, newSize, commitUndo=True, newCanvas=None, dirty=True):
        self.resize(newSize, commitUndo, dirty)
        self.canvas.update(newSize, newCanvas)
        eventDc = self.backend.getDeviceContext(self.GetClientSize(), self, self.GetViewStart())
        eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0); patches = [];
        for numRow in range(newSize[1]):
            for numCol in range(newSize[0]):
                patches += [[numCol, numRow, *self.canvas.map[numRow][numCol]]]
        self.backend.drawPatches(self.canvas, eventDc, patches, isCursor=False)
        eventDc.SetDeviceOrigin(*eventDcOrigin)

    def __init__(self, backend, canvas, commands, parent, pos, size):
        super().__init__(parent, pos)
        self.size = size
        self.backend, self.canvas, self.commands, self.parentFrame = backend(self.size), canvas, commands(self, parent), parent
        self.brushColours, self.brushPos, self.brushSize, self.dirty, self.lastCellState = [4, 1], [0, 0], [1, 1], False, None
        self.popupEventDc = None
        self.dropTarget = RoarCanvasWindowDropTarget(self)
        self.SetDropTarget(self.dropTarget)
        self.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
