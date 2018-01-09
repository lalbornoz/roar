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
from MiRCARTCanvasStore import MiRCARTCanvasStore, haveMiRCARTToPngFile, haveUrllib
from MiRCARTColours import MiRCARTColours
import wx

class MiRCARTCanvas(wx.Panel):
    """XXX"""
    parentFrame = None
    canvasMap = canvasPos = canvasSize = None
    brushColours = brushPos = brushSize = None
    canvasBackend = canvasCurTool = canvasJournal = canvasStore = None

    # {{{ _commitPatch(self, patch):
    def _commitPatch(self, patch):
        self.canvasMap[patch[0][1]][patch[0][0]] = patch[1:]
    # }}}
    # {{{ _dispatchInput(self, eventDc, patches): XXX
    def _dispatchInput(self, eventDc, patches):
        self.canvasBackend.drawCursorMaskWithJournal(   \
            self.canvasJournal, eventDc)
        cursorPatches = []; undoPatches = []; newPatches = [];
        for patchDescr in patches:
            patchIsCursor = patchDescr[0]
            for patch in patchDescr[1]:
                if self.canvasBackend.drawPatch(eventDc, patch) == False:
                    continue
                else:
                    patchDeltaCell = self.canvasMap[patch[0][1]][patch[0][0]]
                if patchIsCursor == True:
                    cursorPatches.append([list(patch[0]), *patchDeltaCell.copy()])
                else:
                    undoPatches.append([list(patch[0]), *patchDeltaCell.copy()])
                    newPatches.append(patch)
                    self._commitPatch(patch)
        if len(cursorPatches):
            self.canvasJournal.pushCursor(cursorPatches)
        if len(undoPatches):
            self.canvasJournal.pushDeltas(undoPatches, newPatches)
    # }}}

    # {{{ onPanelClose(self, event): XXX
    def onPanelClose(self, event):
        self.Destroy()
    # }}}
    # {{{ onPanelKeyboardInput(self, event): XXX
    def onPanelKeyboardInput(self, event):
        eventDc = self.canvasBackend.getDeviceContext(self)
        tool = self.canvasCurTool; mapPoint = self.brushPos;
        keyModifiers = event.GetModifiers()
        if  keyModifiers != wx.MOD_NONE                             \
        and keyModifiers != wx.MOD_SHIFT:
            event.Skip()
        else:
            patches = tool.onKeyboardEvent(                         \
                event, mapPoint, self.brushColours, self.brushSize, \
                chr(event.GetUnicodeKey()))
            if len(patches):
                self._dispatchInput(eventDc, patches)
                self.parentFrame.onCanvasUpdate()
    # }}}
    # {{{ onPanelMouseInput(self, event): XXX
    def onPanelMouseInput(self, event):
        eventDc = self.canvasBackend.getDeviceContext(self)
        tool = self.canvasCurTool
        self.brushPos = mapPoint =                              \
            self.canvasBackend.xlateEventPoint(event, eventDc)
        patches = tool.onMouseEvent(                            \
            event, mapPoint, self.brushColours, self.brushSize, \
            event.Dragging(), event.LeftIsDown(), event.RightIsDown())
        if len(patches):
            self._dispatchInput(eventDc, patches)
            self.parentFrame.onCanvasUpdate()
        self.parentFrame.onCanvasMotion(event, mapPoint)
    # }}}
    # {{{ onPanelFocus(self, event): XXX
    def onPanelFocus(self, event):
        if event.GetEventType() == wx.wxEVT_LEAVE_WINDOW:
            eventDc = self.canvasBackend.getDeviceContext(self)
            self.canvasBackend.drawCursorMaskWithJournal(  \
                self.canvasJournal, eventDc)
        self.parentFrame.onCanvasMotion(event)
    # }}}
    # {{{ onPanelPaint(self, event): XXX
    def onPanelPaint(self, event):
        self.canvasBackend.onPanelPaintEvent(self, event)
    # }}}
    # {{{ onStoreUpdate(self, newCanvasSize, newCanvas=None):
    def onStoreUpdate(self, newCanvasSize, newCanvas=None):
        self.resize(newCanvasSize=newCanvasSize)
        self.canvasBackend.reset(self.canvasSize, self.canvasBackend.cellSize)
        self.canvasJournal.resetCursor(); self.canvasJournal.resetUndo();
        self.canvasMap = [[[(1, 1), 0, " "]             \
                for x in range(self.canvasSize[0])]     \
                    for y in range(self.canvasSize[1])]
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
    # {{{ popRedo(self):
    def popRedo(self):
        eventDc = self.canvasBackend.getDeviceContext(self)
        patches = self.canvasJournal.popRedo()
        for patch in patches:
            if self.canvasBackend.drawPatch(eventDc, patch) == False:
                continue
            else:
                self._commitPatch(patch)
        self.parentFrame.onCanvasUpdate()
    # }}}
    # {{{ popUndo(self):
    def popUndo(self):
        eventDc = self.canvasBackend.getDeviceContext(self)
        patches = self.canvasJournal.popUndo()
        for patch in patches:
            if self.canvasBackend.drawPatch(eventDc, patch) == False:
                continue
            else:
                self._commitPatch(patch)
        self.parentFrame.onCanvasUpdate()
    # }}}
    # {{{ resize(self, newCanvasSize):
    def resize(self, newCanvasSize):
        if newCanvasSize != self.canvasSize:
            winSize = [a*b for a,b in                   \
                zip(newCanvasSize, self.canvasBackend.cellSize)]
            self.SetSize(*self.canvasPos, *winSize)
            for numRow in range(self.canvasSize[1]):
                for numNewCol in range(self.canvasSize[0], newCanvasSize[0]):
                    self.canvasMap[numRow].append([[1, 1], 0, " "])
            for numNewRow in range(self.canvasSize[1], newCanvasSize[1]):
                self.canvasMap.append([])
                for numNewCol in range(newCanvasSize[0]):
                    self.canvasMap[numNewRow].append([[1, 1], 0, " "])
            self.canvasSize = newCanvasSize
            self.canvasBackend.reset(self.canvasSize,   \
                self.canvasBackend.cellSize)
        self.parentFrame.onCanvasUpdate()
    # }}}

    #
    # _init__(self, parent, parentFrame, canvasPos, canvasSize, cellSize): initialisation method
    def __init__(self, parent, parentFrame, canvasPos, canvasSize, cellSize):
        super().__init__(parent, pos=canvasPos,             \
            size=[w*h for w,h in zip(canvasSize, cellSize)])

        self.parentFrame = parentFrame
        self.canvasMap = None; self.canvasPos = canvasPos; self.canvasSize = canvasSize;
        self.brushColours = [4, 1]; self.brushPos = [0, 0]; self.brushSize = [1, 1];
        self.canvasBackend = MiRCARTCanvasBackend(canvasSize, cellSize)
        self.canvasCurTool = None
        self.canvasJournal = MiRCARTCanvasJournal()
        self.canvasStore = MiRCARTCanvasStore(parentCanvas=self)

        # Bind event handlers
        self.Bind(wx.EVT_CLOSE, self.onPanelClose)
        self.Bind(wx.EVT_ENTER_WINDOW, self.onPanelFocus)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onPanelFocus)
        self.parentFrame.Bind(wx.EVT_CHAR, self.onPanelKeyboardInput)
        for eventType in(                                   \
                wx.EVT_LEFT_DOWN, wx.EVT_MOTION, wx.EVT_RIGHT_DOWN):
            self.Bind(eventType, self.onPanelMouseInput)
        self.Bind(wx.EVT_PAINT, self.onPanelPaint)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
