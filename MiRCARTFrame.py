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

from MiRCARTCanvas import MiRCARTCanvas, haveUrllib
from MiRCARTCanvasInterface import MiRCARTCanvasInterface
from MiRCARTColours import MiRCARTColours
from MiRCARTGeneralFrame import MiRCARTGeneralFrame,                                    \
    TID_ACCELS, TID_COMMAND, TID_LIST, TID_MENU, TID_NOTHING, TID_SELECT, TID_TOOLBAR,  \
    NID_MENU_SEP, NID_TOOLBAR_SEP

import os, wx

class MiRCARTFrame(MiRCARTGeneralFrame):
    """XXX"""
    panelCanvas = None; lastPanelState = {};

    # {{{ Commands
    #                      Id     Type Id      Labels                           Icon bitmap                 Accelerator                 [Initial state]
    CID_NEW             = [0x100, TID_COMMAND, "New", "&New",                   ["", wx.ART_NEW],           [wx.ACCEL_CTRL, ord("N")],  None,           MiRCARTCanvasInterface.canvasNew]
    CID_OPEN            = [0x101, TID_COMMAND, "Open", "&Open",                 ["", wx.ART_FILE_OPEN],     [wx.ACCEL_CTRL, ord("O")],  None,           MiRCARTCanvasInterface.canvasOpen]
    CID_SAVE            = [0x102, TID_COMMAND, "Save", "&Save",                 ["", wx.ART_FILE_SAVE],     [wx.ACCEL_CTRL, ord("S")],  None,           MiRCARTCanvasInterface.canvasSave]
    CID_SAVEAS          = [0x103, TID_COMMAND, "Save As...", "Save &As...",     ["", wx.ART_FILE_SAVE_AS],  None,                       None,           MiRCARTCanvasInterface.canvasSaveAs]
    CID_EXPORT_AS_PNG   = [0x104, TID_COMMAND, "Export as PNG...",              \
                                               "Export as PN&G...",             None,                       None,                       None,           MiRCARTCanvasInterface.canvasExportAsPng]
    CID_EXPORT_IMGUR    = [0x105, TID_COMMAND, "Export to Imgur...",            \
                                               "Export to I&mgur...",           None,                       None,                       haveUrllib,     MiRCARTCanvasInterface.canvasExportImgur]
    CID_EXPORT_PASTEBIN = [0x106, TID_COMMAND, "Export to Pastebin...",         \
                                               "Export to Pasteb&in...",        None,                       None,                       haveUrllib,     MiRCARTCanvasInterface.canvasExportPastebin]
    CID_EXIT            = [0x107, TID_COMMAND, "Exit", "E&xit",                 None,                       None,                       None,           MiRCARTCanvasInterface.canvasExit]
    CID_UNDO            = [0x108, TID_COMMAND, "Undo", "&Undo",                 ["", wx.ART_UNDO],          [wx.ACCEL_CTRL, ord("Z")],  False,          MiRCARTCanvasInterface.canvasUndo]
    CID_REDO            = [0x109, TID_COMMAND, "Redo", "&Redo",                 ["", wx.ART_REDO],          [wx.ACCEL_CTRL, ord("Y")],  False,          MiRCARTCanvasInterface.canvasRedo]
    CID_CUT             = [0x10a, TID_COMMAND, "Cut", "Cu&t",                   ["", wx.ART_CUT],           None,                       False,          MiRCARTCanvasInterface.canvasCut]
    CID_COPY            = [0x10b, TID_COMMAND, "Copy", "&Copy",                 ["", wx.ART_COPY],          None,                       False,          MiRCARTCanvasInterface.canvasCopy]
    CID_PASTE           = [0x10c, TID_COMMAND, "Paste", "&Paste",               ["", wx.ART_PASTE],         None,                       False,          MiRCARTCanvasInterface.canvasPaste]
    CID_DELETE          = [0x10d, TID_COMMAND, "Delete", "De&lete",             ["", wx.ART_DELETE],        None,                       False,          MiRCARTCanvasInterface.canvasDelete]
    CID_INCRW_CANVAS    = [0x10e, TID_COMMAND, "Increase canvas width",         \
                                               "Increase canvas &width",        ["", wx.ART_PLUS],          [wx.ACCEL_ALT, ord("D")],   None,           MiRCARTCanvasInterface.canvasIncrCanvasWidth]
    CID_DECRW_CANVAS    = [0x10f, TID_COMMAND, "Decrease canvas width",         \
                                               "Decrease canvas w&idth",        ["", wx.ART_MINUS],         [wx.ACCEL_ALT, ord("A")],   None,           MiRCARTCanvasInterface.canvasDecrCanvasWidth]
    CID_INCRH_CANVAS    = [0x110, TID_COMMAND, "Increase canvas height",        \
                                               "Increase canvas &height",       ["", wx.ART_PLUS],          [wx.ACCEL_ALT, ord("S")],   None,           MiRCARTCanvasInterface.canvasIncrCanvasHeight]
    CID_DECRH_CANVAS    = [0x111, TID_COMMAND, "Decrease canvas height",        \
                                               "Decrease canvas h&eight",       ["", wx.ART_MINUS],         [wx.ACCEL_ALT, ord("W")],   None,           MiRCARTCanvasInterface.canvasDecrCanvasHeight]
    CID_INCR_BRUSH      = [0x112, TID_COMMAND, "Increase brush size",           \
                                               "I&ncrease brush size",          ["", wx.ART_PLUS],          [wx.ACCEL_CTRL, ord("+")],  None,           MiRCARTCanvasInterface.canvasIncrBrush]
    CID_DECR_BRUSH      = [0x113, TID_COMMAND, "Decrease brush size",           \
                                               "&Decrease brush size",          ["", wx.ART_MINUS],         [wx.ACCEL_CTRL, ord("-")],  None,           MiRCARTCanvasInterface.canvasDecrBrush]
    CID_SOLID_BRUSH     = [0x114, TID_SELECT,  "Solid brush", "&Solid brush",   None,                       None,                       True,           MiRCARTCanvasInterface.canvasBrushSolid]

    CID_RECT            = [0x150, TID_SELECT,  "Rectangle", "&Rectangle",       ["toolRect.png"],           [wx.ACCEL_CTRL, ord("R")],  True,           MiRCARTCanvasInterface.canvasToolRect]
    CID_CIRCLE          = [0x151, TID_SELECT,  "Circle", "&Circle",             ["toolCircle.png"],         [wx.ACCEL_CTRL, ord("C")],  False,          MiRCARTCanvasInterface.canvasToolCircle]
    CID_LINE            = [0x152, TID_SELECT,  "Line", "&Line",                 ["toolLine.png"],           [wx.ACCEL_CTRL, ord("L")],  False,          MiRCARTCanvasInterface.canvasToolLine]
    CID_TEXT            = [0x153, TID_SELECT,  "Text", "&Text",                 ["toolText.png"],           [wx.ACCEL_CTRL, ord("T")],  False,          MiRCARTCanvasInterface.canvasToolText]
    CID_CLONE_SELECT    = [0x154, TID_SELECT,  "Clone", "Cl&one",               ["toolClone.png"],          [wx.ACCEL_CTRL, ord("E")],  False,          MiRCARTCanvasInterface.canvasToolSelectClone]
    CID_MOVE_SELECT     = [0x155, TID_SELECT,  "Move", "&Move",                 ["toolMove.png"],           [wx.ACCEL_CTRL, ord("M")],  False,          MiRCARTCanvasInterface.canvasToolSelectMove]

    CID_COLOUR00        = [0x1a0, TID_COMMAND, "Colour #00", "Colour #00",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR01        = [0x1a1, TID_COMMAND, "Colour #01", "Colour #01",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR02        = [0x1a2, TID_COMMAND, "Colour #02", "Colour #02",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR03        = [0x1a3, TID_COMMAND, "Colour #03", "Colour #03",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR04        = [0x1a4, TID_COMMAND, "Colour #04", "Colour #04",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR05        = [0x1a5, TID_COMMAND, "Colour #05", "Colour #05",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR06        = [0x1a6, TID_COMMAND, "Colour #06", "Colour #06",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR07        = [0x1a7, TID_COMMAND, "Colour #07", "Colour #07",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR08        = [0x1a8, TID_COMMAND, "Colour #08", "Colour #08",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR09        = [0x1a9, TID_COMMAND, "Colour #09", "Colour #09",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR10        = [0x1aa, TID_COMMAND, "Colour #10", "Colour #10",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR11        = [0x1ab, TID_COMMAND, "Colour #11", "Colour #11",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR12        = [0x1ac, TID_COMMAND, "Colour #12", "Colour #12",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR13        = [0x1ad, TID_COMMAND, "Colour #13", "Colour #13",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR14        = [0x1ae, TID_COMMAND, "Colour #14", "Colour #14",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    CID_COLOUR15        = [0x1af, TID_COMMAND, "Colour #15", "Colour #15",      None,                       None,                       None,           MiRCARTCanvasInterface.canvasColour]
    # }}}
    # {{{ Menus
    MID_FILE            = (0x300, TID_MENU, "File", "&File", (                                          \
        CID_NEW, CID_OPEN, CID_SAVE, CID_SAVEAS, NID_MENU_SEP,                                          \
        CID_EXPORT_AS_PNG, CID_EXPORT_IMGUR, CID_EXPORT_PASTEBIN, NID_MENU_SEP,                         \
        CID_EXIT))
    MID_EDIT            = (0x301, TID_MENU, "Edit", "&Edit", (                                          \
        CID_UNDO, CID_REDO, NID_MENU_SEP,                                                               \
        CID_CUT, CID_COPY, CID_PASTE, CID_DELETE, NID_MENU_SEP,                                         \
        CID_INCRW_CANVAS, CID_DECRW_CANVAS, CID_INCRH_CANVAS, CID_DECRH_CANVAS, NID_MENU_SEP,           \
        CID_INCR_BRUSH, CID_DECR_BRUSH, CID_SOLID_BRUSH))
    MID_TOOLS           = (0x302, TID_MENU, "Tools", "&Tools", (                                        \
        CID_RECT, CID_CIRCLE, CID_LINE, CID_TEXT, CID_CLONE_SELECT, CID_MOVE_SELECT))
    # }}}
    # {{{ Toolbars
    BID_TOOLBAR         = (0x400, TID_TOOLBAR, (                                                        \
        CID_NEW, CID_OPEN, CID_SAVE, CID_SAVEAS, NID_TOOLBAR_SEP,                                       \
        CID_UNDO, CID_REDO, NID_TOOLBAR_SEP,                                                            \
        CID_CUT, CID_COPY, CID_PASTE, CID_DELETE, NID_TOOLBAR_SEP,                                      \
        CID_INCR_BRUSH, CID_DECR_BRUSH, NID_TOOLBAR_SEP,                                                \
        CID_RECT, CID_CIRCLE, CID_LINE, CID_TEXT, CID_CLONE_SELECT, CID_MOVE_SELECT, NID_TOOLBAR_SEP,   \
        CID_COLOUR00, CID_COLOUR01, CID_COLOUR02, CID_COLOUR03, CID_COLOUR04,                           \
        CID_COLOUR05, CID_COLOUR06, CID_COLOUR07, CID_COLOUR08, CID_COLOUR09,                           \
        CID_COLOUR10, CID_COLOUR11, CID_COLOUR12, CID_COLOUR13, CID_COLOUR14,                           \
        CID_COLOUR15))
    # }}}
    # {{{ Accelerators (hotkeys)
    AID_EDIT            = (0x500, TID_ACCELS, (                                                         \
        CID_NEW, CID_OPEN, CID_SAVE, CID_UNDO, CID_REDO,                                                \
        CID_INCRW_CANVAS, CID_DECRW_CANVAS, CID_INCRH_CANVAS, CID_DECRH_CANVAS,                         \
        CID_INCR_BRUSH, CID_DECR_BRUSH,                                                                 \
        CID_RECT, CID_CIRCLE, CID_LINE, CID_TEXT, CID_CLONE_SELECT, CID_MOVE_SELECT))
    # }}}
    # {{{ Lists
    LID_ACCELS          = (0x600, TID_LIST, (AID_EDIT))
    LID_MENUS           = (0x601, TID_LIST, (MID_FILE, MID_EDIT, MID_TOOLS))
    LID_TOOLBARS        = (0x602, TID_LIST, (BID_TOOLBAR))
    # }}}

    # {{{ _initPaletteToolBitmaps(self): XXX
    def _initPaletteToolBitmaps(self):
        paletteDescr = (                                                                                        \
                self.CID_COLOUR00, self.CID_COLOUR01, self.CID_COLOUR02, self.CID_COLOUR03, self.CID_COLOUR04,  \
                self.CID_COLOUR05, self.CID_COLOUR06, self.CID_COLOUR07, self.CID_COLOUR08, self.CID_COLOUR09,  \
                self.CID_COLOUR10, self.CID_COLOUR11, self.CID_COLOUR12, self.CID_COLOUR13, self.CID_COLOUR14,  \
                self.CID_COLOUR15)
        for numColour in range(len(paletteDescr)):
            toolBitmapColour = MiRCARTColours[numColour][0:4]
            toolBitmap = wx.Bitmap((16,16))
            toolBitmapDc = wx.MemoryDC(); toolBitmapDc.SelectObject(toolBitmap);
            toolBitmapBrush = wx.Brush(         \
                wx.Colour(toolBitmapColour), wx.BRUSHSTYLE_SOLID)
            toolBitmapDc.SetBrush(toolBitmapBrush)
            toolBitmapDc.SetBackground(toolBitmapBrush)
            toolBitmapDc.SetPen(wx.Pen(wx.Colour(toolBitmapColour), 1))
            toolBitmapDc.DrawRectangle(0, 0, 16, 16)
            paletteDescr[numColour][4] = ["", None, toolBitmap]
    # }}}

    # {{{ onInput(self, event): XXX
    def onInput(self, event):
        eventId = event.GetId()
        if  eventId >= self.CID_COLOUR00[0] \
        and eventId <= self.CID_COLOUR15[0]:
            numColour = eventId - self.CID_COLOUR00[0]
            self.itemsById[eventId][7](self.panelCanvas.canvasInterface, event, numColour)
        else:
            self.itemsById[eventId][7](self.panelCanvas.canvasInterface, event)
    # }}}
    # {{{ onCanvasUpdate(self, newBrushSize=None, newCellPos=None, newColours=None, newPathName=None, newSize=None, newToolName=None, newUndoLevel=None): XXX
    def onCanvasUpdate(self, **kwargs):
        self.lastPanelState.update(kwargs)
        textItems = []
        if "cellPos" in self.lastPanelState:
            textItems.append("X: {:03d} Y: {:03d}".format(              \
                *self.lastPanelState["cellPos"]))
        if "size" in self.lastPanelState:
            textItems.append("W: {:03d} H: {:03d}".format(              \
                *self.lastPanelState["size"]))
        if "brushSize" in self.lastPanelState:
            textItems.append("Brush: {:02d}x{:02d}".format(             \
                *self.lastPanelState["brushSize"]))
        if "colours" in self.lastPanelState:
            textItems.append("FG: {:02d}, BG: {:02d}".format(           \
                *self.lastPanelState["colours"]))
            textItems.append("{} on {}".format(                         \
                MiRCARTColours[self.lastPanelState["colours"][0]][4],   \
                MiRCARTColours[self.lastPanelState["colours"][1]][4]))
        if "pathName" in self.lastPanelState:
            if self.lastPanelState["pathName"] != "":
                basePathName = os.path.basename(self.lastPanelState["pathName"])
                textItems.append("Current file: {}".format(basePathName))
                self.SetTitle("{} - MiRCART".format(basePathName))
            else:
                self.SetTitle("MiRCART")
        if "toolName" in self.lastPanelState:
            textItems.append("Current tool: {}".format(                 \
                self.lastPanelState["toolName"]))
        self.statusBar.SetStatusText(" | ".join(textItems))
        if "undoLevel" in self.lastPanelState: 
            if self.lastPanelState["undoLevel"] >= 0:
                self.menuItemsById[self.CID_UNDO[0]].Enable(True)
                self.toolBar.EnableTool(self.CID_UNDO[0], True)
            else:
                self.menuItemsById[self.CID_UNDO[0]].Enable(False)
                self.toolBar.EnableTool(self.CID_UNDO[0], False)
            if self.lastPanelState["undoLevel"] > 0:
                self.menuItemsById[self.CID_REDO[0]].Enable(True)
                self.toolBar.EnableTool(self.CID_REDO[0], True)
            else:
                self.menuItemsById[self.CID_REDO[0]].Enable(False)
                self.toolBar.EnableTool(self.CID_REDO[0], False)
    # }}}

    #
    # __init__(self, parent, appSize=(840, 630), defaultCanvasPos=(25, 50), defaultCanvasSize=(100, 30), defaultCellSize=(7, 14)): initialisation method
    def __init__(self, parent, appSize=(840, 630), defaultCanvasPos=(25, 50), defaultCanvasSize=(100, 30), defaultCellSize=(7, 14)):
        self._initPaletteToolBitmaps()
        panelSkin = super().__init__(parent, wx.ID_ANY, "MiRCART", size=appSize)
        self.panelCanvas = MiRCARTCanvas(panelSkin, parentFrame=self,   \
            defaultCanvasPos=defaultCanvasPos,                          \
            defaultCanvasSize=defaultCanvasSize,                        \
            defaultCellSize=defaultCellSize)
        self.panelCanvas.canvasInterface.canvasNew(None)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
