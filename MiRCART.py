#!/usr/bin/env python3
#
# MiRCART.py -- mIRC art editor for Windows & Linux
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

import wx
import os, sys

# {{{ mircColours: mIRC colour number to RGBA map given none of ^[BFV_] (bold, italic, reverse, underline)
mircColours = [
    (255, 255, 255, 255),   # White
    (0,   0,   0,   255),   # Black
    (0,   0,   187, 255),   # Blue
    (0,   187, 0,   255),   # Green
    (255, 85,  85,  255),   # Light Red
    (187, 0,   0,   255),   # Red
    (187, 0,   187, 255),   # Purple
    (187, 187, 0,   255),   # Yellow
    (255, 255, 85,  255),   # Light Yellow
    (85,  255, 85,  255),   # Light Green
    (0,   187, 187, 255),   # Cyan
    (85,  255, 255, 255),   # Light Cyan
    (85,  85,  255, 255),   # Light Blue
    (255, 85,  255, 255),   # Pink
    (85,  85,  85,  255),   # Grey
    (187, 187, 187, 255),   # Light Grey
]
# }}}

class MiRCARTCanvas(wx.Panel):
    """XXX"""
    canvasPos = canvasSize = canvasWinSize = cellPos = cellSize = None
    canvasBitmap = canvasMap = canvasTools = None
    mircBg = mircFg = mircBrushes = mircPens = None
    patchesTmp = patchesUndo = patchesUndoLevel = None

    # {{{ _drawPatch(): XXX
    def _drawPatch(self, patch, eventDc, tmpDc, atX, atY):
        patchXabs = (atX + patch[0]) * self.getCellWidth()
        patchYabs = (atY + patch[1]) * self.getCellHeight()
        brushFg = self.mircBrushes[patch[2]]
        brushBg = self.mircBrushes[patch[3]]
        pen = self.mircPens[patch[2]]
        for dc in (eventDc, tmpDc):
            dc.SetBrush(brushFg); dc.SetBackground(brushBg); dc.SetPen(pen);
            dc.DrawRectangle(patchXabs, patchYabs,                  \
                self.getCellWidth(), self.getCellHeight())
    # }}}
    # {{{ _eventPointToMapX(): XXX
    def _eventPointToMapX(self, eventPoint):
        rectX = eventPoint.x - (eventPoint.x % self.getCellWidth())
        return int(rectX / self.getCellWidth() if rectX else 0)
    # }}}
    # {{{ _eventPointToMapY(): XXX
    def _eventPointToMapY(self, eventPoint):
        rectY = eventPoint.y - (eventPoint.y % self.getCellHeight())
        return int(rectY / self.getCellHeight() if rectY else 0)
    # }}}
    # {{{ _onMouseEvent(): XXX
    def _onMouseEvent(self, event):
        eventObject = event.GetEventObject()
        eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
        tmpDc.SelectObject(self.canvasBitmap)
        eventPoint = event.GetLogicalPosition(eventDc)
        mapX = self._eventPointToMapX(eventPoint)
        mapY = self._eventPointToMapY(eventPoint)
        for tool in self.canvasTools:
            if event.Dragging():
                mapPatches = tool.onMouseMotion(event, mapX, mapY, event.LeftIsDown(), event.RightIsDown())
            else:
                mapPatches = tool.onMouseDown(event, mapX, mapY, event.LeftIsDown(), event.RightIsDown())
            self._processMapPatches(mapPatches, eventDc, tmpDc, mapX, mapY)
    # }}}
    # {{{ _processMapPatches(): XXX
    def _processMapPatches(self, mapPatches, eventDc, tmpDc, atX, atY):
        for mapPatch in mapPatches:
            mapPatchTmp = mapPatch[0]; mapPatchW = mapPatch[1]; mapPatchH = mapPatch[2];
            if mapPatchTmp and self.patchesTmp:
                for patch in self.patchesTmp:
                    patch[2] = self.canvasMap[patch[1]][patch[0]][0]
                    patch[3] = self.canvasMap[patch[1]][patch[0]][1]
                    patch[4] = self.canvasMap[patch[1]][patch[0]][2]
                    self._drawPatch(patch, eventDc, tmpDc, 0, 0)
                self.patchesTmp = []
            for patch in mapPatch[3]:
                if mapPatchTmp:
                    mapItem = self.canvasMap[atY + patch[1]][atX + patch[0]]
                    self.patchesTmp.append([atX + patch[0], atY + patch[1], None, None, None])
                    self._drawPatch(patch, eventDc, tmpDc, atX, atY)
                else:
                    mapItem = self.canvasMap[atY + patch[1]][atX + patch[0]]
                    if mapItem != [patch[2], patch[3], patch[4]]:
                        if self.patchesUndoLevel > 0:
                            del self.patchesUndo[0:self.patchesUndoLevel]
                            self.patchesUndoLevel = 0
                        self.patchesUndo.insert(0, (                                                \
                            (atX + patch[0], atY + patch[1], mapItem[0], mapItem[1], mapItem[2]),   \
                            (atX + patch[0], atY + patch[1], patch[2], patch[3], " ")))
                        self.canvasMap[atY + patch[1]][atX + patch[0]] = [patch[2], patch[3], " "];
                        self._drawPatch(patch, eventDc, tmpDc, atX, atY)
    # }}}
    # {{{ getBackgroundColour(): XXX
    def getBackgroundColour(self):
        return self.mircBg
    # }}}
    # {{{ getCellHeight(): XXX
    def getCellHeight(self):
        return self.cellSize[1]
    # }}}
    # {{{ getCellWidth(): XXX
    def getCellWidth(self):
        return self.cellSize[0]
    # }}}
    # {{{ getForegroundColour(): XXX
    def getForegroundColour(self):
        return self.mircFg
    # }}}
    # {{{ getHeight(): XXX
    def getHeight(self):
        return self.canvasSize[1]
    # }}}
    # {{{ getMap(): XXX
    def getMap(self):
        return self.canvasMap
    # }}}
    # {{{ getWidth(): XXX
    def getWidth(self):
        return self.canvasSize[0]
    # }}}
    # {{{ onLeftDown(): XXX
    def onLeftDown(self, event):
        self._onMouseEvent(event)
    # }}}
    # {{{ onMotion(): XXX
    def onMotion(self, event):
            self._onMouseEvent(event)
    # }}}
    # {{{ onPaint(): XXX
    def onPaint(self, event):
        eventDc = wx.BufferedPaintDC(self, self.canvasBitmap)
    # }}}
    # {{{ onPaletteEvent(): XXX
    def onPaletteEvent(self, leftDown, rightDown, numColour):
        if leftDown:
            self.mircFg = numColour
        elif rightDown:
            self.mircBg = numColour
    # }}}
    # {{{ onRightDown(): XXX
    def onRightDown(self, event):
        self._onMouseEvent(event)
    # }}}
    # {{{ redo(): XXX
    def redo(self):
        if self.patchesUndoLevel > 0:
            self.patchesUndoLevel -= 1
            redoPatch = self.patchesUndo[self.patchesUndoLevel][1]
            self.canvasMap[redoPatch[1]][redoPatch[0]] =    \
                [redoPatch[2], redoPatch[3], redoPatch[4]]
            eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
            tmpDc.SelectObject(self.canvasBitmap)
            self._drawPatch(redoPatch, eventDc, tmpDc, 0, 0)
            return True
        else:
            return False
    # }}}
    # {{{ undo(): XXX
    def undo(self):
        if self.patchesUndo[self.patchesUndoLevel] != None:
            undoPatch = self.patchesUndo[self.patchesUndoLevel][0]
            self.canvasMap[undoPatch[1]][undoPatch[0]] =    \
                [undoPatch[2], undoPatch[3], undoPatch[4]]
            eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
            tmpDc.SelectObject(self.canvasBitmap)
            self._drawPatch(undoPatch, eventDc, tmpDc, 0, 0)
            self.patchesUndoLevel += 1
            return True
        else:
            return False
    # }}}
    # {{{ Initialisation method
    def __init__(self, parent, canvasPos, cellSize, canvasSize, canvasTools):
        canvasWinSize = (cellSize[0] * canvasSize[0], cellSize[1] * canvasSize[1])
        super().__init__(parent, pos=canvasPos, size=canvasWinSize)
        self.canvasPos = canvasPos; self.canvasSize = canvasSize; self.canvasWinSize = canvasWinSize;
        self.cellPos = (0, 0); self.cellSize = cellSize;

        self.canvasBitmap = wx.Bitmap(canvasWinSize)
        self.canvasMap = [[[1, 1, " "] for x in range(canvasSize[0])] for y in range(canvasSize[1])]
        self.canvasTools = []
        for canvasTool in canvasTools:
            self.canvasTools.append(canvasTool(self))

        self.mircBg = 1; self.mircFg = 4;
        self.mircBrushes = [None for x in range(len(mircColours))]
        self.mircPens = [None for x in range(len(mircColours))]
        for mircColour in range(0, len(mircColours)):
            self.mircBrushes[mircColour] = wx.Brush(                \
                wx.Colour(mircColours[mircColour]), wx.BRUSHSTYLE_SOLID)
            self.mircPens[mircColour] = wx.Pen(                     \
                wx.Colour(mircColours[mircColour]), 1)

        self.patchesTmp = []
        self.patchesUndo = [None]; self.patchesUndoLevel = 0;

        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
    # }}}

class MiRCARTTool():
    """XXX"""
    parentCanvas = None

    # {{{ onMouseDown(): XXX
    def onMouseDown(self, event, mapX, mapY, isLeftDown, isRightDown):
        pass
    # }}}
    # {{{ onMouseMotion(): XXX
    def onMouseMotion(self, event, mapX, mapY, isLeftDown, isRightDown):
        pass
    # }}}
    # {{{ Initialisation method
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas
    # }}}

class MiRCARTToolRect(MiRCARTTool):
    """XXX"""

    # {{{ _draw(): XXX
    def _draw(self, event, mapX, mapY, isLeftDown, isRightDown):
        if isLeftDown:
            return [[False, 1, 1, [[0, 0,                           \
                self.parentCanvas.getForegroundColour(),            \
                self.parentCanvas.getForegroundColour(), " "]]],
                    [True, 1, 1, [[0, 0,                            \
                self.parentCanvas.getForegroundColour(),            \
                self.parentCanvas.getForegroundColour(), " "]]]]
        elif isRightDown:
            return [[False, 1, 1, [[0, 0,                           \
                self.parentCanvas.getBackgroundColour(),            \
                self.parentCanvas.getBackgroundColour(), " "]]],    \
                    [True, 1, 1, [[0, 0,                            \
                self.parentCanvas.getBackgroundColour(),            \
                self.parentCanvas.getBackgroundColour(), " "]]]]
        else:
            return [[True, 1, 1, [[0, 0,                            \
                self.parentCanvas.getForegroundColour(),            \
                self.parentCanvas.getForegroundColour(), " "]]]]
    # }}}
    # {{{ onMouseDown(): XXX
    def onMouseDown(self, event, mapX, mapY, isLeftDown, isRightDown):
        return self._draw(event, mapX, mapY, isLeftDown, isRightDown)
    # }}}
    # {{{ onMouseMotion(): XXX
    def onMouseMotion(self, event, mapX, mapY, isLeftDown, isRightDown):
        return self._draw(event, mapX, mapY, isLeftDown, isRightDown)
    # }}}
    # {{{ Initialisation method
    def __init__(self, parentCanvas):
        super().__init__(parentCanvas)
    # }}}

class MiRCARTPalette(wx.Panel):
    """XXX"""
    panelsByColour = onPaletteEvent = None

    # {{{ onLeftDown(): XXX
    def onLeftDown(self, event):
        numColour = int(event.GetEventObject().GetName())
        self.onPaletteEvent(True, False, numColour)
    # }}}
    # {{{ onRightDown(): XXX
    def onRightDown(self, event):
        numColour = int(event.GetEventObject().GetName())
        self.onPaletteEvent(False, True, numColour)
    # }}}
    # {{{ Initialisation method
    def __init__(self, parent, parentPos, cellSize, onPaletteEvent):
        panelSizeW = 6 * cellSize[0]; panelSizeH = 2 * cellSize[1];
        paletteSize = (panelSizeW * 16, panelSizeH)
        super().__init__(parent, pos=parentPos, size=paletteSize)
        self.panelsByColour = [None] * len(mircColours)
        for numColour in range(0, len(mircColours)):
            posX = (numColour * (cellSize[0] * 6))
            self.panelsByColour[numColour] = wx.Panel(self,         \
                pos=(posX, 0), size=(panelSizeW, panelSizeH))
            self.panelsByColour[numColour].SetBackgroundColour(     \
                wx.Colour(mircColours[numColour]))
            self.panelsByColour[numColour].Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
            self.panelsByColour[numColour].Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
            self.panelsByColour[numColour].SetName(str(numColour))
        self.onPaletteEvent = onPaletteEvent
    # }}}

class MiRCARTFrame(wx.Frame):
    """XXX"""
    menuFile = None
    menuFileNew = menuFileOpen = menuFileSave = menuFileSaveAs = None
    menuFileExportPastebin = menuFileExportPng = None
    menuFileExit = None
    menuEdit = None
    menuEditRedo = menuEditUndo = None
    menuEditCopy = menuEditCut = menuEditDelete = menuEditPaste = None
    menuEditDecrBrush = menuEditIncrBrush = menuEditSolidBrush = None
    menuTools = menuToolsCircle = menuToolsLine = menuToolsRect = None
    menuBar = None
    panelSkin = panelCanvas = panelPalette = None
    accelRedoId = accelUndoId = accelTable = statusBar = None

    # {{{ _updateStatusBar(): XXX
    def _updateStatusBar(self):
        text = "Foreground colour:"
        text += " " + str(self.panelCanvas.getForegroundColour())
        text += " | "
        text += "Background colour:"
        text += " " + str(self.panelCanvas.getBackgroundColour())
        self.statusBar.SetStatusText(text)
    # }}}
    # {{{ onAccelRedo(): XXX
    def onAccelRedo(self, event):
        self.panelCanvas.redo()
    # }}}
    # {{{ onAccelUndo(): XXX
    def onAccelUndo(self, event):
        self.panelCanvas.undo()
    # }}}
    # {{{ onEditCopy(): XXX
    def onEditCopy(self, event):
        pass
    # }}}
    # {{{ onEditCut(): XXX
    def onEditCut(self, event):
        pass
    # }}}
    # {{{ onEditDecrBrush(): XXX
    def onEditDecrBrush(self, event):
        pass
    # }}}
    # {{{ onEditDelete(): XXX
    def onEditDelete(self, event):
        pass
    # }}}
    # {{{ onEditIncrBrush(): XXX
    def onEditIncrBrush(self, event):
        pass
    # }}}
    # {{{ onEditPaste(): XXX
    def onEditPaste(self, event):
        pass
    # }}}
    # {{{ onEditRedo(): XXX
    def onEditRedo(self, event):
        self.panelCanvas.redo()
    # }}}
    # {{{ onEditSolidBrush(): XXX
    def onEditSolidBrush(self, event):
        pass
    # }}}
    # {{{ onEditUndo(): XXX
    def onEditUndo(self, event):
        self.panelCanvas.undo()
    # }}}
    # {{{ onFileExit(): XXX
    def onFileExit(self, event):
        self.Close(True)
    # }}}
    # {{{ onFileExportPastebin(): XXX
    def onFileExportPastebin(self, event):
        pass
    # }}}
    # {{{ onFileExportPng(): XXX
    def onFileExportPng(self, event):
        pass
    # }}}
    # {{{ onFileNew(): XXX
    def onFileNew(self, event):
        pass
    # }}}
    # {{{ onFileOpen(): XXX
    def onFileOpen(self, event):
        pass
    # }}}
    # {{{ onFileSave(): XXX
    def onFileSave(self, event):
        pass
    # }}}
    # {{{ onFileSaveAs(): XXX
    def onFileSaveAs(self, event):
        with wx.FileDialog(self, "Save As...", os.getcwd(), "",     \
                "*.txt", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            else:
                try:
                    with open(dialog.GetPath(), "w") as file:
                        canvasMap = self.panelCanvas.getMap()
                        canvasHeight = self.panelCanvas.getHeight()
                        canvasWidth = self.panelCanvas.getWidth()
                        for canvasRow in range(0, canvasHeight):
                            colourLastBg = colourLastFg = None;
                            for canvasCol in range(0, canvasWidth):
                                canvasColBg = canvasMap[canvasRow][canvasCol][0]
                                canvasColFg = canvasMap[canvasRow][canvasCol][1]
                                canvasColText = canvasMap[canvasRow][canvasCol][2]
                                if colourLastBg != canvasColBg      \
                                or colourLastFg != canvasColFg:
                                    colourLastBg = canvasColBg; colourLastFg = canvasColFg;
                                    file.write("" + str(canvasColFg) + "," + str(canvasColBg))
                                file.write(canvasColText)
                            file.write("\n")
                except IOError as error:
                    wx.LogError("IOError {}".format(error))
    # }}}
    # {{{ onToolsRect(): XXX
    def onToolsRect(self, event):
        pass
    # }}}
    # {{{ onToolsCircle(): XXX
    def onToolsCircle(self, event):
        pass
    # }}}
    # {{{ onToolsLine(): XXX
    def onToolsLine(self, event):
        pass
    # }}}
    # {{{ onPaletteEvent(): XXX
    def onPaletteEvent(self, leftDown, rightDown, numColour):
        self.panelCanvas.onPaletteEvent(leftDown, rightDown, numColour)
        self._updateStatusBar()
    # }}}
    # {{{ Initialisation method
    def __init__(self, parent, appSize=(800, 600), canvasPos=(25, 25), cellSize=(7, 14), canvasSize=(80, 25)):
        super().__init__(parent, wx.ID_ANY, "MiRCART", size=appSize)

        self.panelSkin = wx.Panel(self, wx.ID_ANY)
        self.panelCanvas = MiRCARTCanvas(self.panelSkin,            \
            canvasPos=canvasPos, cellSize=cellSize,                 \
            canvasSize=canvasSize, canvasTools=[MiRCARTToolRect])
        self.panelPalette = MiRCARTPalette(self.panelSkin,          \
            (25, (canvasSize[1] + 3) * cellSize[1]), cellSize, self.onPaletteEvent)

        self.menuFile = wx.Menu()
        self.menuFileNew = self.menuFile.Append(wx.ID_NEW, "&New", "New")
        self.Bind(wx.EVT_MENU, self.onFileNew, self.menuFileNew)
        self.menuFileOpen = self.menuFile.Append(wx.ID_OPEN, "&Open...", "Open...")
        self.Bind(wx.EVT_MENU, self.onFileOpen, self.menuFileOpen)
        self.menuFileSave = self.menuFile.Append(wx.ID_SAVE, "&Save", "Save")
        self.Bind(wx.EVT_MENU, self.onFileSave, self.menuFileSave)
        self.menuFileSaveAs = self.menuFile.Append(wx.ID_SAVEAS, "Save &As...", "Save As...")
        self.Bind(wx.EVT_MENU, self.onFileSaveAs, self.menuFileSaveAs)
        self.menuFile.AppendSeparator()
        self.menuFileExportPastebin = self.menuFile.Append(wx.NewId(), "Export to &Pastebin...", "Export to Pastebin...")
        self.Bind(wx.EVT_MENU, self.onFileExportPastebin, self.menuFileExportPastebin)
        self.menuFileExportPng = self.menuFile.Append(wx.NewId(), "Export as &PNG...", "Export as PNG...")
        self.Bind(wx.EVT_MENU, self.onFileExportPng, self.menuFileExportPng)
        self.menuFile.AppendSeparator()
        self.menuFileExit = self.menuFile.Append(wx.ID_EXIT, "E&xit", "Exit")
        self.Bind(wx.EVT_MENU, self.onFileExit, self.menuFileExit)

        self.menuEdit = wx.Menu()
        self.menuEditUndo = self.menuEdit.Append(wx.ID_UNDO, "&Undo", "Undo")
        self.menuEditUndo.Enable(False)
        self.Bind(wx.EVT_MENU, self.onEditUndo, self.menuEditUndo)
        self.menuEditRedo = self.menuEdit.Append(wx.ID_REDO, "&Redo", "Redo")
        self.menuEditRedo.Enable(False)
        self.Bind(wx.EVT_MENU, self.onEditRedo, self.menuEditRedo)
        self.menuEdit.AppendSeparator()
        self.menuEditCut = self.menuEdit.Append(wx.ID_CUT, "Cu&t", "Cut")
        self.Bind(wx.EVT_MENU, self.onEditCut, self.menuEditCut)
        self.menuEditCopy = self.menuEdit.Append(wx.ID_COPY, "&Copy", "Copy")
        self.Bind(wx.EVT_MENU, self.onEditCopy, self.menuEditCopy)
        self.menuEditPaste = self.menuEdit.Append(wx.ID_PASTE, "&Paste", "Paste")
        self.Bind(wx.EVT_MENU, self.onEditPaste, self.menuEditPaste)
        self.menuEditDelete = self.menuEdit.Append(wx.ID_DELETE, "De&lete", "Delete")
        self.Bind(wx.EVT_MENU, self.onEditDelete, self.menuEditDelete)
        self.menuEdit.AppendSeparator()
        self.menuEditIncrBrush = self.menuEdit.Append(wx.NewId(), "&Increase brush size", "Increase brush size")
        self.Bind(wx.EVT_MENU, self.onEditIncrBrush, self.menuEditIncrBrush)
        self.menuEditDecrBrush = self.menuEdit.Append(wx.NewId(), "&Decrease brush size", "Decrease brush size")
        self.Bind(wx.EVT_MENU, self.onEditDecrBrush, self.menuEditDecrBrush)
        self.menuEditSolidBrush = self.menuEdit.AppendRadioItem(wx.NewId(), "&Solid brush", "Solid brush")
        self.Bind(wx.EVT_MENU, self.onEditSolidBrush, self.menuEditSolidBrush)

        self.menuTools = wx.Menu()
        self.menuToolsRect = self.menuTools.AppendRadioItem(wx.NewId(), "&Rectangle", "Rectangle")
        self.Bind(wx.EVT_MENU, self.onToolsRect, self.menuToolsRect)
        self.menuToolsCircle = self.menuTools.AppendRadioItem(wx.NewId(), "&Circle", "Circle")
        self.Bind(wx.EVT_MENU, self.onToolsCircle, self.menuToolsCircle)
        self.menuToolsLine = self.menuTools.AppendRadioItem(wx.NewId(), "&Line", "Line")
        self.Bind(wx.EVT_MENU, self.onToolsLine, self.menuToolsLine)

        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.menuFile, "&File")
        self.menuBar.Append(self.menuEdit, "&Edit")
        self.menuBar.Append(self.menuTools, "&Tools")
        self.SetMenuBar(self.menuBar)

        accelTableEntries = [wx.AcceleratorEntry() for n in range(2)]
        self.accelRedoId = wx.NewId()
        accelTableEntries[0].Set(wx.ACCEL_CTRL, ord('Y'), self.accelRedoId)
        self.Bind(wx.EVT_MENU, self.onAccelRedo, id=self.accelRedoId)
        self.accelUndoId = wx.NewId()
        accelTableEntries[1].Set(wx.ACCEL_CTRL, ord('Z'), self.accelUndoId)
        self.Bind(wx.EVT_MENU, self.onAccelUndo, id=self.accelUndoId)
        self.accelTable = wx.AcceleratorTable(accelTableEntries)
        self.SetAcceleratorTable(self.accelTable)

        self.statusBar = self.CreateStatusBar()
        self._updateStatusBar()

        self.SetFocus()
        self.Show(True)
    # }}}

#
# Entry point
def main(*argv):
    wxApp = wx.App(False)
    MiRCARTFrame(None)
    wxApp.MainLoop()
if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
