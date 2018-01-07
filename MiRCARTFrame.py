#!/usr/bin/env python3
#
# MiRCARTFrame.py -- XXX
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

from MiRCARTCanvas import MiRCARTCanvas
from MiRCARTColours import MiRCARTColours
from MiRCARTFromTextFile import MiRCARTFromTextFile
from MiRCARTToTextFile import MiRCARTToTextFile
import os, wx

try:
    from MiRCARTToPastebin import MiRCARTToPastebin
    haveMiRCARTToPastebin = True
except ImportError:
    haveMiRCARTToPastebin = False

try:
    from MiRCARTToPngFile import MiRCARTToPngFile
    haveMiRCARTToPngFile = True
except ImportError:
    haveMiRCARTToPngFile = False

class MiRCARTFrame(wx.Frame):
    """XXX"""
    panelSkin = panelCanvas = canvasPathName = None
    canvasPos = canvasSize = canvasTools = cellSize = None
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
    CID_EXPORT_AS_PNG   = (0x104, TID_COMMAND, "Export as PNG...", "Export as PN&G...", (),             None)
    CID_EXPORT_PASTEBIN = (0x105, TID_COMMAND, "Export to Pastebin...", "Export to Pasteb&in...", (),   None)
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
    CID_COLOUR00        = (0x113, TID_COMMAND, "Colour #00", "Colour #00",      MiRCARTColours[0],      None)
    CID_COLOUR01        = (0x114, TID_COMMAND, "Colour #01", "Colour #01",      MiRCARTColours[1],      None)
    CID_COLOUR02        = (0x115, TID_COMMAND, "Colour #02", "Colour #02",      MiRCARTColours[2],      None)
    CID_COLOUR03        = (0x116, TID_COMMAND, "Colour #03", "Colour #03",      MiRCARTColours[3],      None)
    CID_COLOUR04        = (0x117, TID_COMMAND, "Colour #04", "Colour #04",      MiRCARTColours[4],      None)
    CID_COLOUR05        = (0x118, TID_COMMAND, "Colour #05", "Colour #05",      MiRCARTColours[5],      None)
    CID_COLOUR06        = (0x119, TID_COMMAND, "Colour #06", "Colour #06",      MiRCARTColours[6],      None)
    CID_COLOUR07        = (0x11a, TID_COMMAND, "Colour #07", "Colour #07",      MiRCARTColours[7],      None)
    CID_COLOUR08        = (0x11b, TID_COMMAND, "Colour #08", "Colour #08",      MiRCARTColours[8],      None)
    CID_COLOUR09        = (0x11c, TID_COMMAND, "Colour #09", "Colour #09",      MiRCARTColours[9],      None)
    CID_COLOUR10        = (0x11d, TID_COMMAND, "Colour #10", "Colour #10",      MiRCARTColours[10],     None)
    CID_COLOUR11        = (0x11e, TID_COMMAND, "Colour #11", "Colour #11",      MiRCARTColours[11],     None)
    CID_COLOUR12        = (0x11f, TID_COMMAND, "Colour #12", "Colour #12",      MiRCARTColours[12],     None)
    CID_COLOUR13        = (0x120, TID_COMMAND, "Colour #13", "Colour #13",      MiRCARTColours[13],     None)
    CID_COLOUR14        = (0x121, TID_COMMAND, "Colour #14", "Colour #14",      MiRCARTColours[14],     None)
    CID_COLOUR15        = (0x122, TID_COMMAND, "Colour #15", "Colour #15",      MiRCARTColours[15],     None)
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
    # {{{ _updateStatusBar(self): XXX
    def _updateStatusBar(self):
        text = "Foreground colour:"
        text += " " + str(self.panelCanvas.mircFg)
        text += " | "
        text += "Background colour:"
        text += " " + str(self.panelCanvas.mircBg)
        self.statusBar.SetStatusText(text)
    # }}}

    # {{{ canvasExportAsPng(self): XXX
    def canvasExportAsPng(self):
        with wx.FileDialog(self, self.CID_SAVEAS[2], os.getcwd(), "",   \
                "*.png", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                outPathName = dialog.GetPath()
                outTmpFile = io.StringIO()
                outToTextFile = MiRCARTToTextFile(                      \
                    self.panelCanvas.canvasMap, self.canvasSize)
                outToTextFile.export(outTmpFile)
                MiRCARTToPngFile(tmpFile).export(outPathName)
                return True
    # }}}
    # {{{ canvasExportPastebin(self): XXX
    def canvasExportPastebin(self):
        MiRCARTToPastebin("253ce2f0a45140ee0a44ca99aa49260",            \
            self.panelCanvas.canvasMap, self.canvasSize).export()
    # }}}
    # {{{ canvasNew(self, canvasPos=None, canvasSize=None, cellSize=None): XXX
    def canvasNew(self, canvasPos=None, canvasSize=None, cellSize=None):
        canvasPos = canvasPos if canvasPos != None else self.canvasPos
        canvasSize = canvasSize if canvasSize != None else self.canvasSize
        cellSize = cellSize if cellSize != None else self.cellSize
        if self.panelCanvas != None:
            self.panelCanvas.Close(); self.panelCanvas = None;
        self.canvasPos = canvasPos; self.canvasSize = canvasSize;
        self.cellSize = cellSize
        self.panelCanvas = MiRCARTCanvas(self.panelSkin, parentFrame=self,  \
            canvasPos=self.canvasPos, cellSize=self.cellSize,               \
            canvasSize=self.canvasSize, canvasTools=self.canvasTools)
        self._updateStatusBar(); self.onCanvasUpdate();
    # }}}
    # {{{ canvasOpen(self): XXX
    def canvasOpen(self):
        with wx.FileDialog(self, self.CID_OPEN[2], os.getcwd(), "",     \
                "*.txt", wx.FD_OPEN) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                self.canvasPathName = dialog.GetPath()
                with open(self.canvasPathName, "r") as newFile:
                    newFromTextFile = MiRCARTFromTextFile(newFile)
                    newMap = newFromTextFile.getMap()
                    self.canvasNew(canvasSize=newFromTextFile.getSize())
                    eventDc = wx.ClientDC(self); tmpDc = wx.MemoryDC();
                    tmpDc.SelectObject(self.panelCanvas.canvasBitmap)
                    for newNumRow in range(0, len(newMap)):
                        for newNumCol in range(0, len(newMap[newNumRow])):
                            self.panelCanvas.onJournalUpdate(False,     \
                                (newNumCol, newNumRow),                 \
                                [newNumCol, newNumRow,                  \
                                newMap[newNumRow][newNumCol][0][0],     \
                                newMap[newNumRow][newNumCol][0][1],     \
                                newMap[newNumRow][newNumCol][2]],       \
                                eventDc, tmpDc, (0, 0))
                    wx.SafeYield()
                    return True
    # }}}
    # {{{ canvasSave(self): XXX
    def canvasSave(self):
        if self.canvasPathName == None:
            if self.canvasSaveAs() == False:
                return
        try:
            with open(self.canvasPathName, "w") as outFile:
                MiRCARTToTextFile(self.panelCanvas.canvasMap,   \
                    self.panelCanvas.canvasSize).export(outFile)
        except IOError as error:
            pass
    # }}}
    # {{{ canvasSaveAs(self): XXX
    def canvasSaveAs(self):
        with wx.FileDialog(self, self.CID_SAVEAS[2], os.getcwd(), "",   \
                "*.txt", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                self.canvasPathName = dialog.GetPath()
                return True
    # }}}
    # {{{ onCanvasUpdate(self): XXX
    def onCanvasUpdate(self):
        if self.panelCanvas.canvasJournal.patchesUndo[self.panelCanvas.canvasJournal.patchesUndoLevel] != None:
            self.menuItemsById[self.CID_UNDO[0]].Enable(True)
        else:
            self.menuItemsById[self.CID_UNDO[0]].Enable(False)
        if self.panelCanvas.canvasJournal.patchesUndoLevel > 0:
            self.menuItemsById[self.CID_REDO[0]].Enable(True)
        else:
            self.menuItemsById[self.CID_REDO[0]].Enable(False)
    # }}}
    # {{{ onClose(self, event): XXX
    def onClose(self, event):
        self.Destroy(); self.__del__();
    # }}}
    # {{{ onFrameCommand(self, event): XXX
    def onFrameCommand(self, event):
        cid = event.GetId()
        if cid == self.CID_NEW[0]:
            self.canvasNew()
        elif cid == self.CID_OPEN[0]:
            self.canvasOpen()
        elif cid == self.CID_SAVE[0]:
            self.canvasSave()
        elif cid == self.CID_SAVEAS[0]:
            self.canvasSaveAs()
        elif cid == self.CID_EXPORT_AS_PNG[0]:
            self.canvasExportAsPng()
        elif cid == self.CID_EXPORT_PASTEBIN[0]:
            self.canvasExportPastebin()
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
    # {{{ __del__(self): destructor method
    def __del__(self):
        if self.panelCanvas != None:
            self.panelCanvas.Close(); self.panelCanvas = None;
    # }}}

    #
    # __init__(self, parent, appSize=(800, 600), canvasPos=(25, 50), cellSize=(7, 14), canvasSize=(100, 30), canvasTools=[]): initialisation method
    def __init__(self, parent, appSize=(800, 600), canvasPos=(25, 50), cellSize=(7, 14), canvasSize=(100, 30), canvasTools=[]):
        super().__init__(parent, wx.ID_ANY, "MiRCART", size=appSize)
        self.panelSkin = wx.Panel(self, wx.ID_ANY)
        self.canvasPathName = None

        self.menuItemsById = {}; self.menuBar = wx.MenuBar();
        self._initMenus(self.menuBar,                   \
            [self.MID_FILE, self.MID_EDIT, self.MID_TOOLS], self.onFrameCommand)
        self.SetMenuBar(self.menuBar)
        if not haveMiRCARTToPastebin:
            self.menuItemsById[self.CID_EXPORT_PASTEBIN[0]].Enable(False)
        if not haveMiRCARTToPngFile:
            self.menuItemsById[self.CID_EXPORT_AS_PNG[0]].Enable(False)

        self.toolBar = wx.ToolBar(self.panelSkin, -1,   \
            style=wx.HORIZONTAL|wx.TB_FLAT|wx.TB_NODIVIDER)
        self.toolBar.SetToolBitmapSize((16,16))
        self._initToolBars(self.toolBar, [self.BID_TOOLBAR], self.onFrameCommand)
        self.toolBar.Realize(); self.toolBar.Fit();

        self.accelTable = wx.AcceleratorTable(          \
            self._initAccelTable(self.AID_EDIT, self.onFrameCommand))
        self.SetAcceleratorTable(self.accelTable)

        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.statusBar = self.CreateStatusBar();
        self.SetFocus(); self.Show(True);
        self.canvasTools = canvasTools
        self.canvasNew(canvasPos, canvasSize, cellSize)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
