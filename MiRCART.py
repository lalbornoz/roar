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

import enum
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
    parentFrame = None
    canvasPos = canvasSize = canvasWinSize = cellPos = cellSize = None
    canvasBitmap = canvasMap = canvasTools = None
    mircBg = mircFg = mircBrushes = mircPens = None
    patchesTmp = patchesUndo = patchesUndoLevel = None

    # {{{ _drawPatch(self, patch, eventDc, tmpDc, atPoint): XXX
    def _drawPatch(self, patch, eventDc, tmpDc, atPoint):
        absPoint = self._relMapPointToAbsPoint((patch[0], patch[1]), atPoint)
        brushFg = self.mircBrushes[patch[2]]; brushBg = self.mircBrushes[patch[3]];
        pen = self.mircPens[patch[2]]
        for dc in (eventDc, tmpDc):
            dc.SetBrush(brushFg); dc.SetBackground(brushBg); dc.SetPen(pen);
            dc.DrawRectangle(absPoint[0], absPoint[1], self.cellSize[0], self.cellSize[1])
    # }}}
    # {{{ _eventPointToMapPoint(self, eventPoint): XXX
    def _eventPointToMapPoint(self, eventPoint):
        rectX = eventPoint.x - (eventPoint.x % self.cellSize[0])
        rectY = eventPoint.y - (eventPoint.y % self.cellSize[1])
        mapX = int(rectX / self.cellSize[0] if rectX else 0)
        mapY = int(rectY / self.cellSize[1] if rectY else 0)
        return (mapX, mapY)
    # }}}
    # {{{ _getMapCell(self, absMapPoint): XXX
    def _getMapCell(self, absMapPoint):
        return self.canvasMap[absMapPoint[1]][absMapPoint[0]]
    # }}}
    # {{{ _processMapPatches(self, mapPatches, eventDc, tmpDc, atPoint): XXX
    def _processMapPatches(self, mapPatches, eventDc, tmpDc, atPoint):
        for mapPatch in mapPatches:
            mapPatchTmp = mapPatch[0]
            if mapPatchTmp and self.patchesTmp:
                for patch in self.patchesTmp:
                    patch[2:] = self._getMapCell([patch[0], patch[1]])
                    self._drawPatch(patch, eventDc, tmpDc, (0, 0))
                self.patchesTmp = []
            for patch in mapPatch[1]:
                absMapPoint = self._relMapPointToAbsMapPoint(patch[0:2], atPoint)
                mapItem = self._getMapCell(absMapPoint)
                if mapPatchTmp:
                    self.patchesTmp.append([*absMapPoint, None, None, None])
                    self._drawPatch(patch, eventDc, tmpDc, atPoint)
                elif mapItem != patch[2:5]:
                    self._pushUndo(atPoint, patch, mapItem)
                    self._setMapCell(absMapPoint, *patch[2:5])
                    self._drawPatch(patch, eventDc, tmpDc, atPoint)
                self.parentFrame.onCanvasUpdate()
    # }}}
    # {{{ _pushUndo(self, atPoint, patch): XXX
    def _pushUndo(self, atPoint, patch, mapItem):
        if self.patchesUndoLevel > 0:
            del self.patchesUndo[0:self.patchesUndoLevel]
            self.patchesUndoLevel = 0
        absMapPoint = self._relMapPointToAbsMapPoint((patch[0], patch[1]), atPoint)
        self.patchesUndo.insert(0, (                                                \
            (absMapPoint[0], absMapPoint[1], mapItem[0], mapItem[1], mapItem[2]),   \
            (absMapPoint[0], absMapPoint[1], patch[2], patch[3], patch[4])))
    # }}}
    # {{{ _relMapPointToAbsMapPoint(self, relMapPoint, atPoint): XXX
    def _relMapPointToAbsMapPoint(self, relMapPoint, atPoint):
        return (atPoint[0] + relMapPoint[0], atPoint[1] + relMapPoint[1])
    # }}}
    # {{{ _relMapPointToAbsPoint(self, relMapPoint, atPoint): XXX
    def _relMapPointToAbsPoint(self, relMapPoint, atPoint):
        absX = (atPoint[0] + relMapPoint[0]) * self.cellSize[0]
        absY = (atPoint[1] + relMapPoint[1]) * self.cellSize[1]
        return (absX, absY)
    # }}}
    # {{{ _setMapCell(self, absMapPoint, colourFg, colourBg, char): XXX
    def _setMapCell(self, absMapPoint, colourFg, colourBg, char):
        self.canvasMap[absMapPoint[1]][absMapPoint[0]] = [colourFg, colourBg, char]
    # }}}

    # {{{ onMouseEvent(self, event): XXX
    def onMouseEvent(self, event):
        eventObject = event.GetEventObject()
        eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
        tmpDc.SelectObject(self.canvasBitmap)
        eventPoint = event.GetLogicalPosition(eventDc)
        mapPoint = self._eventPointToMapPoint(eventPoint)
        for tool in self.canvasTools:
            mapPatches = tool.onMouseEvent(event, mapPoint, event.Dragging(),   \
                event.LeftIsDown(), event.RightIsDown())
            self._processMapPatches(mapPatches, eventDc, tmpDc, mapPoint)
    # }}}
    # {{{ onPaint(self, event): XXX
    def onPaint(self, event):
        eventDc = wx.BufferedPaintDC(self, self.canvasBitmap)
    # }}}
    # {{{ redo(self): XXX
    def redo(self):
        if self.patchesUndoLevel > 0:
            self.patchesUndoLevel -= 1
            redoPatch = self.patchesUndo[self.patchesUndoLevel][1]
            self._setMapCell([redoPatch[0], redoPatch[1]],  \
                redoPatch[2], redoPatch[3], redoPatch[4])
            eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
            tmpDc.SelectObject(self.canvasBitmap)
            self._drawPatch(redoPatch, eventDc, tmpDc, (0, 0))
            self.parentFrame.onCanvasUpdate()
            return True
        else:
            return False
    # }}}
    # {{{ undo(self): XXX
    def undo(self):
        if self.patchesUndo[self.patchesUndoLevel] != None:
            undoPatch = self.patchesUndo[self.patchesUndoLevel][0]
            self._setMapCell([undoPatch[0], undoPatch[1]],  \
                undoPatch[2], undoPatch[3], undoPatch[4])
            eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
            tmpDc.SelectObject(self.canvasBitmap)
            self._drawPatch(undoPatch, eventDc, tmpDc, (0, 0))
            self.patchesUndoLevel += 1
            self.parentFrame.onCanvasUpdate()
            return True
        else:
            return False
    # }}}
    # {{{ __init__(self, parent, parentFrame, canvasPos, cellSize, canvasSize, canvasTools): Initialisation method
    def __init__(self, parent, parentFrame, canvasPos, cellSize, canvasSize, canvasTools):
        self.parentFrame = parentFrame
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

        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseEvent)
        self.Bind(wx.EVT_MOTION, self.onMouseEvent)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onMouseEvent)
    # }}}

class MiRCARTTool():
    """XXX"""
    parentCanvas = None

    # {{{ onMouseEvent(self, event, mapPoint, isDragging, isLeftDown, isRightDown): XXX
    def onMouseEvent(self, event, mapPoint, isDragging, isLeftDown, isRightDown):
        pass
    # }}}
    # {{{ __init__(self, parentCanvas): initialisation method
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas
    # }}}

class MiRCARTToolRect(MiRCARTTool):
    """XXX"""

    # {{{ onMouseEvent(self, event, mapPoint, isDragging, isLeftDown, isRightDown): XXX
    def onMouseEvent(self, event, mapPoint, isDragging, isLeftDown, isRightDown):
        if isLeftDown:
            return [[False, [[0, 0,                 \
                self.parentCanvas.mircFg,           \
                self.parentCanvas.mircFg, " "]]],
                    [True, [[0, 0,                  \
                self.parentCanvas.mircFg,           \
                self.parentCanvas.mircFg, " "]]]]
        elif isRightDown:
            return [[False, [[0, 0,                 \
                self.parentCanvas.mircBg,           \
                self.parentCanvas.mircBg, " "]]],   \
                    [True, [[0, 0,                  \
                self.parentCanvas.mircBg,           \
                self.parentCanvas.mircBg, " "]]]]
        else:
            return [[True, [[0, 0,                  \
                self.parentCanvas.mircFg,           \
                self.parentCanvas.mircFg, " "]]]]
    # }}}

class MiRCARTFrame(wx.Frame):
    """XXX"""
    panelSkin = panelCanvas = None
    menuItemsById = menuBar = toolBar = accelTable = statusBar = None

    # {{{ Types
    TID_COMMAND         = (0x001)
    TID_NOTHING         = (0x002)
    TID_MENU            = (0x003)
    TID_TOOLBAR         = (0x004)
    TID_ACCELS          = (0x005)
    # }}}
    # {{{ Commands
    #                      Id     Type Id      Labels                           Icon bitmap             Accelerator
    CID_NEW             = (0x100, TID_COMMAND, "New", "&New",                   [wx.ART_NEW],           None)
    CID_OPEN            = (0x101, TID_COMMAND, "Open", "&Open",                 [wx.ART_FILE_OPEN],     None)
    CID_SAVE            = (0x102, TID_COMMAND, "Save", "&Save",                 [wx.ART_FILE_SAVE],     None)
    CID_SAVEAS          = (0x103, TID_COMMAND, "Save As...", "Save &As...",     [wx.ART_FILE_SAVE_AS],  None)
    CID_EXPORT_PASTEBIN = (0x104, TID_COMMAND, "Export to Pastebin...", "Export to Pasteb&in...", (),   None)
    CID_EXPORT_AS_PNG   = (0x105, TID_COMMAND, "Export as PNG...", "Export as PN&G...", (),             None)
    CID_EXIT            = (0x106, TID_COMMAND, "Exit", "E&xit",                 (),                     None)
    CID_UNDO            = (0x107, TID_COMMAND, "Undo", "&Undo",                 [wx.ART_UNDO],          (wx.ACCEL_CTRL, ord("Z")))
    CID_REDO            = (0x108, TID_COMMAND, "Redo", "&Redo",                 [wx.ART_REDO],          (wx.ACCEL_CTRL, ord("Y")))
    CID_CUT             = (0x109, TID_COMMAND, "Cut", "Cu&t",                   [wx.ART_CUT],           None)
    CID_COPY            = (0x10a, TID_COMMAND, "Copy", "&Copy",                 [wx.ART_COPY],          None)
    CID_PASTE           = (0x10b, TID_COMMAND, "Paste", "&Paste",               [wx.ART_PASTE],         None)
    CID_DELETE          = (0x10c, TID_COMMAND, "Delete", "De&lete",             [wx.ART_DELETE],        None)
    CID_INCRBRUSH       = (0x10d, TID_COMMAND, "Increase brush size", "&Increase brush size", [wx.ART_PLUS], None)
    CID_DECRBRUSH       = (0x10e, TID_COMMAND, "Decrease brush size", "&Decrease brush size", [wx.ART_MINUS], None)
    CID_SOLIDBRUSH      = (0x10f, TID_COMMAND, "Solid brush", "&Solid brush",   [None],                 None)
    CID_RECT            = (0x110, TID_COMMAND, "Rectangle", "&Rectangle",       [None],                 None)
    CID_CIRCLE          = (0x111, TID_COMMAND, "Circle", "&Circle",             [None],                 None)
    CID_LINE            = (0x112, TID_COMMAND, "Line", "&Line",                 [None],                 None)
    CID_COLOUR00        = (0x113, TID_COMMAND, "Colour #00", "Colour #00",      mircColours[0],         None)
    CID_COLOUR01        = (0x114, TID_COMMAND, "Colour #01", "Colour #01",      mircColours[1],         None)
    CID_COLOUR02        = (0x115, TID_COMMAND, "Colour #02", "Colour #02",      mircColours[2],         None)
    CID_COLOUR03        = (0x116, TID_COMMAND, "Colour #03", "Colour #03",      mircColours[3],         None)
    CID_COLOUR04        = (0x117, TID_COMMAND, "Colour #04", "Colour #04",      mircColours[4],         None)
    CID_COLOUR05        = (0x118, TID_COMMAND, "Colour #05", "Colour #05",      mircColours[5],         None)
    CID_COLOUR06        = (0x119, TID_COMMAND, "Colour #06", "Colour #06",      mircColours[6],         None)
    CID_COLOUR07        = (0x11a, TID_COMMAND, "Colour #07", "Colour #07",      mircColours[7],         None)
    CID_COLOUR08        = (0x11b, TID_COMMAND, "Colour #08", "Colour #08",      mircColours[8],         None)
    CID_COLOUR09        = (0x11c, TID_COMMAND, "Colour #09", "Colour #09",      mircColours[9],         None)
    CID_COLOUR10        = (0x11d, TID_COMMAND, "Colour #10", "Colour #10",      mircColours[10],        None)
    CID_COLOUR11        = (0x11e, TID_COMMAND, "Colour #11", "Colour #11",      mircColours[11],        None)
    CID_COLOUR12        = (0x11f, TID_COMMAND, "Colour #12", "Colour #12",      mircColours[12],        None)
    CID_COLOUR13        = (0x120, TID_COMMAND, "Colour #13", "Colour #13",      mircColours[13],        None)
    CID_COLOUR14        = (0x121, TID_COMMAND, "Colour #14", "Colour #14",      mircColours[14],        None)
    CID_COLOUR15        = (0x122, TID_COMMAND, "Colour #15", "Colour #15",      mircColours[15],        None)
    # }}}
    # {{{ Non-items
    NID_MENU_SEP        = (0x200, TID_NOTHING)
    NID_TOOLBAR_SEP     = (0x201, TID_NOTHING)
    # }}}
    # {{{ Menus
    MID_FILE            = (0x300, TID_MENU, "File", "&File", (                  \
        CID_NEW, CID_OPEN, CID_SAVE, CID_SAVEAS, NID_MENU_SEP,                  \
        CID_EXPORT_PASTEBIN, CID_EXPORT_AS_PNG, NID_MENU_SEP,                   \
        CID_EXIT))
    MID_EDIT            = (0x301, TID_MENU, "Edit", "&Edit", (                  \
        CID_UNDO, CID_REDO, NID_MENU_SEP,                                       \
        CID_CUT, CID_COPY, CID_PASTE, CID_DELETE, NID_MENU_SEP,                 \
        CID_INCRBRUSH, CID_DECRBRUSH, CID_SOLIDBRUSH))
    MID_TOOLS           = (0x302, TID_MENU, "Tools", "&Tools", (                \
        CID_RECT, CID_CIRCLE, CID_LINE))
    # }}}
    # {{{ Toolbars
    BID_TOOLBAR         = (0x400, TID_TOOLBAR, (                                \
        CID_NEW, CID_OPEN, CID_SAVE, CID_SAVEAS, NID_TOOLBAR_SEP,               \
        CID_UNDO, CID_REDO, NID_TOOLBAR_SEP,                                    \
        CID_CUT, CID_COPY, CID_PASTE, CID_DELETE, NID_TOOLBAR_SEP,              \
        CID_INCRBRUSH, CID_DECRBRUSH, CID_SOLIDBRUSH, NID_TOOLBAR_SEP,          \
        CID_RECT, CID_CIRCLE, CID_LINE, NID_TOOLBAR_SEP,                        \
        CID_COLOUR00, CID_COLOUR01, CID_COLOUR02, CID_COLOUR03, CID_COLOUR04,   \
        CID_COLOUR05, CID_COLOUR06, CID_COLOUR07, CID_COLOUR08, CID_COLOUR09,   \
        CID_COLOUR10, CID_COLOUR11, CID_COLOUR12, CID_COLOUR13, CID_COLOUR14,   \
        CID_COLOUR15))
    # }}}
    # {{{ Accelerators (hotkeys)
    AID_EDIT            = (0x500, TID_ACCELS, (CID_UNDO, CID_REDO))
    # }}}

    # {{{ _drawIcon(self, solidColour): XXX
    def _drawIcon(self, solidColour):
        iconBitmap = wx.Bitmap((16,16))
        iconDc = wx.MemoryDC(); iconDc.SelectObject(iconBitmap);
        iconBrush = wx.Brush(wx.Colour(solidColour), wx.BRUSHSTYLE_SOLID)
        iconDc.SetBrush(iconBrush); iconDc.SetBackground(iconBrush);
        iconDc.SetPen(wx.Pen(wx.Colour(solidColour), 1))
        iconDc.DrawRectangle(0, 0, 16, 16)
        return iconBitmap
    # }}}
    # {{{ _initAccelTable(self, accelsDescr, handler): XXX
    def _initAccelTable(self, accelsDescr, handler):
        accelTableEntries = [wx.AcceleratorEntry() for n in range(0, len(accelsDescr[2]))]
        for numAccel in range(0, len(accelsDescr[2])):
            accelDescr = accelsDescr[2][numAccel]
            if accelDescr[5] != None:
                accelTableEntries[numAccel].Set(accelDescr[5][0], accelDescr[5][1], accelDescr[0])
                self.Bind(wx.EVT_MENU, handler, id=accelDescr[0])
        return accelTableEntries
    # }}}
    # {{{ _initMenus(self, menuBar, menusDescr, handler): XXX
    def _initMenus(self, menuBar, menusDescr, handler):
        for menuDescr in menusDescr:
            menuWindow = wx.Menu()
            for menuItem in menuDescr[4]:
                if menuItem == self.NID_MENU_SEP:
                    menuWindow.AppendSeparator()
                else:
                    menuItemWindow = menuWindow.Append(menuItem[0], menuItem[3], menuItem[2])
                    self.menuItemsById[menuItem[0]] = menuItemWindow
                    self.Bind(wx.EVT_MENU, handler, menuItemWindow)
            menuBar.Append(menuWindow, menuDescr[3])
    # }}}
    # {{{ _initToolBars(self, toolBar, toolBarsDescr, handler): XXX
    def _initToolBars(self, toolBar, toolBarsDescr, handler):
        for toolBarDescr in toolBarsDescr:
            for toolBarItem in toolBarDescr[2]:
                if toolBarItem == self.NID_TOOLBAR_SEP:
                    toolBar.AddSeparator()
                else:
                    if len(toolBarItem[4]) == 4:
                        toolBarItemIcon = self._drawIcon(toolBarItem[4])
                    elif len(toolBarItem[4]) == 1                               \
                    and  toolBarItem[4][0] != None:
                        toolBarItemIcon = wx.ArtProvider.GetBitmap(             \
                            toolBarItem[4][0], wx.ART_TOOLBAR, (16,16))
                    else:
                        toolBarItemIcon = wx.ArtProvider.GetBitmap(             \
                            wx.ART_HELP, wx.ART_TOOLBAR, (16,16))
                    toolBarItemWindow = self.toolBar.AddTool(                   \
                        toolBarItem[0], toolBarItem[2], toolBarItemIcon)
                    self.Bind(wx.EVT_TOOL, handler, toolBarItemWindow)
                    self.Bind(wx.EVT_TOOL_RCLICKED, handler, toolBarItemWindow)
    # }}}
    # {{{ _saveAs(self, pathName): XXX
    def _saveAs(self, pathName):
        try:
            with open(pathName, "w") as file:
                canvasMap = self.panelCanvas.canvasMap
                canvasHeight = self.panelCanvas.canvasSize[1]
                canvasWidth = self.panelCanvas.canvasSize[0]
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
                return [True]
        except IOError as error:
            return [False, error]
    # }}}
    # {{{ _updateStatusBar(self): XXX
    def _updateStatusBar(self):
        text = "Foreground colour:"
        text += " " + str(self.panelCanvas.mircFg)
        text += " | "
        text += "Background colour:"
        text += " " + str(self.panelCanvas.mircBg)
        self.statusBar.SetStatusText(text)
    # }}}

    # {{{ onCanvasUpdate(self): XXX
    def onCanvasUpdate(self):
        if self.panelCanvas.patchesUndo[self.panelCanvas.patchesUndoLevel] != None:
            self.menuItemsById[self.CID_UNDO[0]].Enable(True)
        else:
            self.menuItemsById[self.CID_UNDO[0]].Enable(False)
        if self.panelCanvas.patchesUndoLevel > 0:
            self.menuItemsById[self.CID_REDO[0]].Enable(True)
        else:
            self.menuItemsById[self.CID_REDO[0]].Enable(False)
    # }}}
    # {{{ onFrameCommand(self, event): XXX
    def onFrameCommand(self, event):
        cid = event.GetId()
        if cid == self.CID_NEW[0]:
            pass
        elif cid == self.CID_OPEN[0]:
            pass
        elif cid == self.CID_SAVE[0]:
            pass
        elif cid == self.CID_SAVEAS[0]:
            with wx.FileDialog(self, self.CID_SAVEAS[2], os.getcwd(), "",   \
                    "*.txt", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
                if dialog.ShowModal() == wx.ID_CANCEL:
                    return
                else:
                    self._saveAs(dialog.GetPath())
        elif cid == self.CID_EXPORT_PASTEBIN[0]:
            pass
        elif cid == self.CID_EXPORT_AS_PNG[0]:
            pass
        elif cid == self.CID_EXIT[0]:
            self.Close(True)
        elif cid == self.CID_UNDO[0]:
            self.panelCanvas.undo()
        elif cid == self.CID_REDO[0]:
            self.panelCanvas.redo()
        elif cid == self.CID_CUT[0]:
            pass
        elif cid == self.CID_COPY[0]:
            pass
        elif cid == self.CID_PASTE[0]:
            pass
        elif cid == self.CID_DELETE[0]:
            pass
        elif cid == self.CID_INCRBRUSH[0]:
            pass
        elif cid == self.CID_DECRBRUSH[0]:
            pass
        elif cid == self.CID_SOLIDBRUSH[0]:
            pass
        elif cid == self.CID_RECT[0]:
            pass
        elif cid == self.CID_CIRCLE[0]:
            pass
        elif cid == self.CID_LINE[0]:
            pass
        elif cid >= self.CID_COLOUR00[0]                                    \
        and  cid <= self.CID_COLOUR15[0]:
            numColour = cid - self.CID_COLOUR00[0]
            if event.GetEventType() == wx.wxEVT_TOOL:
                self.panelCanvas.mircFg = numColour
            elif event.GetEventType() == wx.wxEVT_TOOL_RCLICKED:
                self.panelCanvas.mircBg = numColour
            self._updateStatusBar()
    # }}}
    # {{{ __init__(self, parent, appSize=(800, 600), canvasPos=(25, 50), cellSize=(7, 14), canvasSize=(80, 25)): initialisation method
    def __init__(self, parent, appSize=(800, 600), canvasPos=(25, 50), cellSize=(7, 14), canvasSize=(80, 25)):
        super().__init__(parent, wx.ID_ANY, "MiRCART", size=appSize)
        self.panelSkin = wx.Panel(self, wx.ID_ANY)
        self.panelCanvas = MiRCARTCanvas(self.panelSkin,                    \
            parentFrame=self, canvasPos=canvasPos, cellSize=cellSize,       \
            canvasSize=canvasSize, canvasTools=[MiRCARTToolRect])

        self.menuItemsById = {}; self.menuBar = wx.MenuBar();
        self._initMenus(self.menuBar,                                       \
            [self.MID_FILE, self.MID_EDIT, self.MID_TOOLS], self.onFrameCommand)
        self.SetMenuBar(self.menuBar)

        self.toolBar = wx.ToolBar(self.panelSkin, -1,                       \
            style=wx.HORIZONTAL|wx.TB_FLAT|wx.TB_NODIVIDER)
        self.toolBar.SetToolBitmapSize((16,16))
        self._initToolBars(self.toolBar, [self.BID_TOOLBAR], self.onFrameCommand)
        self.toolBar.Realize(); self.toolBar.Fit();

        self.accelTable = wx.AcceleratorTable(                              \
            self._initAccelTable(self.AID_EDIT, self.onFrameCommand))
        self.SetAcceleratorTable(self.accelTable)

        self.statusBar = self.CreateStatusBar(); self._updateStatusBar();
        self.SetFocus(); self.Show(True); self.onCanvasUpdate();
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
