#!/usr/bin/env python3
#
# GuiFrame.py -- XXX
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Canvas import Canvas, haveUrllib
from Colours import Colours
from GuiCanvasInterface import GuiCanvasInterface
from GuiGeneralFrame import GuiGeneralFrame,                                            \
    TID_ACCELS, TID_COMMAND, TID_LIST, TID_MENU, TID_NOTHING, TID_SELECT, TID_TOOLBAR,  \
    NID_MENU_SEP, NID_TOOLBAR_HSEP, NID_TOOLBAR_VSEP

from glob import glob
import os, random, wx

class GuiFrame(GuiGeneralFrame):
    """XXX"""

    # {{{ Commands (0x0100-0x0fff)
    #
    # MID_FILE
    #                      Id       Type Id      Labels                           Icon bitmap                 Accelerator                 [Initial state]
    CID_NEW             = [0x0100,  TID_COMMAND, "New", "&New",                   ["", wx.ART_NEW],           [wx.ACCEL_CTRL, ord("N")],  None,   GuiCanvasInterface.canvasNew]
    CID_OPEN            = [0x0101,  TID_COMMAND, "Open", "&Open",                 ["", wx.ART_FILE_OPEN],     [wx.ACCEL_CTRL, ord("O")],  None,   GuiCanvasInterface.canvasOpen]
    CID_SAVE            = [0x0102,  TID_COMMAND, "Save", "&Save",                 ["", wx.ART_FILE_SAVE],     [wx.ACCEL_CTRL, ord("S")],  None,   GuiCanvasInterface.canvasSave]
    CID_SAVEAS          = [0x0103,  TID_COMMAND, "Save As...", "Save &As...",     ["", wx.ART_FILE_SAVE_AS],  None,                       None,   GuiCanvasInterface.canvasSaveAs]
    CID_EXPORT_CLIPB    = [0x0104,  TID_COMMAND, "Export to clipboard",           "&Export to clipboard",     None,                       None,   None,       GuiCanvasInterface.canvasExportToClipboard]
    CID_EXPORT_AS_PNG   = [0x0105,  TID_COMMAND, "Export as PNG...",              "Export as PN&G...",        None,                       None,   None,       GuiCanvasInterface.canvasExportAsPng]
    CID_EXPORT_IMGUR    = [0x0106,  TID_COMMAND, "Export to Imgur...",            "Export to I&mgur...",      None,                       None,   haveUrllib, GuiCanvasInterface.canvasExportImgur]
    CID_EXPORT_PASTEBIN = [0x0107,  TID_COMMAND, "Export to Pastebin...",         "Export to Pasteb&in...",   None,                       None,   haveUrllib, GuiCanvasInterface.canvasExportPastebin]
    CID_IMPORT_CLIPB    = [0x0108,  TID_COMMAND, "Import from clipboard",         "&Import from clipboard",   None,                       None,   None,       GuiCanvasInterface.canvasImportFromClipboard]
    CID_EXIT            = [0x0109,  TID_COMMAND, "Exit", "E&xit",                 None,                       [wx.ACCEL_CTRL, ord("X")],  None,   GuiCanvasInterface.canvasExit]

    #
    # MID_EDIT
    #                      Id       Type Id      Labels                           Icon bitmap                 Accelerator                 [Initial state]
    CID_UNDO            = [0x0200,  TID_COMMAND, "Undo", "&Undo",                 ["", wx.ART_UNDO],          [wx.ACCEL_CTRL, ord("Z")],  False,  GuiCanvasInterface.canvasUndo]
    CID_REDO            = [0x0201,  TID_COMMAND, "Redo", "&Redo",                 ["", wx.ART_REDO],          [wx.ACCEL_CTRL, ord("Y")],  False,  GuiCanvasInterface.canvasRedo]
    CID_CUT             = [0x0202,  TID_COMMAND, "Cut", "Cu&t",                   ["", wx.ART_CUT],           None,                       False,  GuiCanvasInterface.canvasCut]
    CID_COPY            = [0x0203,  TID_COMMAND, "Copy", "&Copy",                 ["", wx.ART_COPY],          None,                       False,  GuiCanvasInterface.canvasCopy]
    CID_PASTE           = [0x0204,  TID_COMMAND, "Paste", "&Paste",               ["", wx.ART_PASTE],         None,                       False,  GuiCanvasInterface.canvasPaste]
    CID_DELETE          = [0x0205,  TID_COMMAND, "Delete", "De&lete",             ["", wx.ART_DELETE],        None,                       False,  GuiCanvasInterface.canvasDelete]
    CID_INCRW_CANVAS    = [0x0206,  TID_COMMAND, "Increase canvas width",         "Increase canvas width",    ["toolIncrCanvasW.png"],    None,   None,       GuiCanvasInterface.canvasIncrCanvasWidth]
    CID_DECRW_CANVAS    = [0x0207,  TID_COMMAND, "Decrease canvas width",         "Decrease canvas width",    ["toolDecrCanvasW.png"],    None,   None,       GuiCanvasInterface.canvasDecrCanvasWidth]
    CID_INCRH_CANVAS    = [0x0208,  TID_COMMAND, "Increase canvas height",        "Increase canvas height",   ["toolIncrCanvasH.png"],    None,   None,       GuiCanvasInterface.canvasIncrCanvasHeight]
    CID_DECRH_CANVAS    = [0x0209,  TID_COMMAND, "Decrease canvas height",        "Decrease canvas height",   ["toolDecrCanvasH.png"],    None,   None,       GuiCanvasInterface.canvasDecrCanvasHeight]
    CID_INCRHW_CANVAS   = [0x020a,  TID_COMMAND, "Increase canvas size",          "Increase canvas size",     ["toolIncrCanvasHW.png"],   None,   None,       GuiCanvasInterface.canvasIncrCanvasHeightWidth]
    CID_DECRHW_CANVAS   = [0x020b,  TID_COMMAND, "Decrease canvas size",          "Decrease canvas size",     ["toolDecrCanvasHW.png"],   None,   None,       GuiCanvasInterface.canvasDecrCanvasHeightWidth]
    CID_INCRW_BRUSH     = [0x020c,  TID_COMMAND, "Increase brush width",          "Increase brush width",     ["toolIncrBrushW.png"],     None,   None,       GuiCanvasInterface.canvasIncrBrushWidth]
    CID_DECRW_BRUSH     = [0x020d,  TID_COMMAND, "Decrease brush width",          "Decrease brush width",     ["toolDecrBrushW.png"],     None,   None,       GuiCanvasInterface.canvasDecrBrushWidth]
    CID_INCRH_BRUSH     = [0x020e,  TID_COMMAND, "Increase brush height",         "Increase brush height",    ["toolIncrBrushH.png"],     None,   None,       GuiCanvasInterface.canvasIncrBrushHeight]
    CID_DECRH_BRUSH     = [0x020f,  TID_COMMAND, "Decrease brush height",         "Decrease brush height",    ["toolDecrBrushH.png"],     None,   None,       GuiCanvasInterface.canvasDecrBrushHeight]
    CID_INCRHW_BRUSH    = [0x0210,  TID_COMMAND, "Increase brush size",           "Increase brush size",      ["toolIncrBrushHW.png"],    None,   None,       GuiCanvasInterface.canvasIncrBrushHeightWidth]
    CID_DECRHW_BRUSH    = [0x0211,  TID_COMMAND, "Decrease brush size",           "Decrease brush size",      ["toolDecrBrushHW.png"],    None,   None,       GuiCanvasInterface.canvasDecrBrushHeightWidth]
    CID_SOLID_BRUSH     = [0x0212,  TID_SELECT,  "Solid brush", "Solid brush",    None,                       None,                       True,   GuiCanvasInterface.canvasBrushSolid]

    #
    # MID_TOOLS
    #                      Id       Type Id      Labels                           Icon bitmap                 Accelerator                 [Initial state]
    CID_RECT            = [0x0300,  TID_SELECT,  "Rectangle", "&Rectangle",       ["toolRect.png"],           [wx.ACCEL_CTRL, ord("R")],  True,   GuiCanvasInterface.canvasToolRect]
    CID_CIRCLE          = [0x0301,  TID_SELECT,  "Circle", "&Circle",             ["toolCircle.png"],         [wx.ACCEL_CTRL, ord("C")],  False,  GuiCanvasInterface.canvasToolCircle]
    CID_FILL            = [0x0302,  TID_SELECT,  "Fill", "&Fill",                 ["toolFill.png"],           [wx.ACCEL_CTRL, ord("F")],  False,  GuiCanvasInterface.canvasToolFill]
    CID_LINE            = [0x0303,  TID_SELECT,  "Line", "&Line",                 ["toolLine.png"],           [wx.ACCEL_CTRL, ord("L")],  False,  GuiCanvasInterface.canvasToolLine]
    CID_TEXT            = [0x0304,  TID_SELECT,  "Text", "&Text",                 ["toolText.png"],           [wx.ACCEL_CTRL, ord("T")],  False,  GuiCanvasInterface.canvasToolText]
    CID_CLONE_SELECT    = [0x0305,  TID_SELECT,  "Clone", "Cl&one",               ["toolClone.png"],          [wx.ACCEL_CTRL, ord("E")],  False,  GuiCanvasInterface.canvasToolSelectClone]
    CID_MOVE_SELECT     = [0x0306,  TID_SELECT,  "Move", "&Move",                 ["toolMove.png"],           [wx.ACCEL_CTRL, ord("M")],  False,  GuiCanvasInterface.canvasToolSelectMove]

    #
    # BID_TOOLBAR
    #                      Id       Type Id      Labels                           Icon bitmap                 Accelerator                 [Initial state]
    CID_COLOUR00        = [0x0400,  TID_SELECT,  "Colour #00", "Colour #00",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR01        = [0x0401,  TID_SELECT,  "Colour #01", "Colour #01",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR02        = [0x0402,  TID_SELECT,  "Colour #02", "Colour #02",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR03        = [0x0403,  TID_SELECT,  "Colour #03", "Colour #03",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR04        = [0x0404,  TID_SELECT,  "Colour #04", "Colour #04",      None,                       None,                       True,   GuiCanvasInterface.canvasColour]
    CID_COLOUR05        = [0x0405,  TID_SELECT,  "Colour #05", "Colour #05",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR06        = [0x0406,  TID_SELECT,  "Colour #06", "Colour #06",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR07        = [0x0407,  TID_SELECT,  "Colour #07", "Colour #07",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR08        = [0x0408,  TID_SELECT,  "Colour #08", "Colour #08",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR09        = [0x0409,  TID_SELECT,  "Colour #09", "Colour #09",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR10        = [0x040a,  TID_SELECT,  "Colour #10", "Colour #10",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR11        = [0x040b,  TID_SELECT,  "Colour #11", "Colour #11",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR12        = [0x040c,  TID_SELECT,  "Colour #12", "Colour #12",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR13        = [0x040d,  TID_SELECT,  "Colour #13", "Colour #13",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR14        = [0x040e,  TID_SELECT,  "Colour #14", "Colour #14",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]
    CID_COLOUR15        = [0x040f,  TID_SELECT,  "Colour #15", "Colour #15",      None,                       None,                       False,  GuiCanvasInterface.canvasColour]

    #
    # MID_ABOUT
    #                      Id       Type Id      Labels                           Icon bitmap                 Accelerator                 [Initial state]
    CID_ABOUT           = [0x0500,  TID_COMMAND, "About", "&About",               None,                       None,                       True,   GuiCanvasInterface.canvasAbout]
    # }}}
    # {{{ Menus (0x1100-0x1fff)
    MID_FILE            = (0x1100,  TID_MENU, "File", "&File", (CID_NEW, CID_OPEN, CID_SAVE, CID_SAVEAS, NID_MENU_SEP, CID_EXPORT_CLIPB, CID_EXPORT_AS_PNG, CID_EXPORT_IMGUR, CID_EXPORT_PASTEBIN, NID_MENU_SEP, CID_IMPORT_CLIPB, NID_MENU_SEP, CID_EXIT))
    MID_EDIT            = (0x1101,  TID_MENU, "Edit", "&Edit", (CID_UNDO, CID_REDO, NID_MENU_SEP, CID_CUT, CID_COPY, CID_PASTE, CID_DELETE, NID_MENU_SEP, CID_INCRW_CANVAS, CID_DECRW_CANVAS, CID_INCRH_CANVAS, CID_DECRH_CANVAS, NID_MENU_SEP, CID_INCRHW_CANVAS, CID_DECRHW_CANVAS, NID_MENU_SEP, CID_INCRW_BRUSH, CID_DECRW_BRUSH, CID_INCRH_BRUSH, CID_DECRH_BRUSH, NID_MENU_SEP, CID_INCRHW_BRUSH, CID_DECRHW_BRUSH, NID_MENU_SEP, CID_SOLID_BRUSH))
    MID_TOOLS           = (0x1102,  TID_MENU, "Tools", "&Tools", (CID_RECT, CID_CIRCLE, CID_FILL, CID_LINE, CID_TEXT, CID_CLONE_SELECT, CID_MOVE_SELECT))
    MID_HELP            = (0x1103,  TID_MENU, "Help", "&Help", (CID_ABOUT,))
    # }}}
    # {{{ Toolbars (0x2100-0x2fff)
    BID_TOOLBAR         = (0x2100,  TID_TOOLBAR, (CID_NEW, CID_OPEN, CID_SAVE, CID_SAVEAS, NID_TOOLBAR_HSEP, CID_UNDO, CID_REDO, NID_TOOLBAR_HSEP, CID_CUT, CID_COPY, CID_PASTE, CID_DELETE, NID_TOOLBAR_HSEP, CID_INCRW_CANVAS, CID_DECRW_CANVAS, CID_INCRH_CANVAS, CID_DECRH_CANVAS, NID_TOOLBAR_HSEP, CID_INCRHW_CANVAS, CID_DECRHW_CANVAS, NID_TOOLBAR_HSEP, CID_RECT, CID_CIRCLE, CID_FILL, CID_LINE, CID_TEXT, CID_CLONE_SELECT, CID_MOVE_SELECT, NID_TOOLBAR_VSEP, CID_COLOUR00, CID_COLOUR01, CID_COLOUR02, CID_COLOUR03, CID_COLOUR04, CID_COLOUR05, CID_COLOUR06, CID_COLOUR07, CID_COLOUR08, CID_COLOUR09, CID_COLOUR10, CID_COLOUR11, CID_COLOUR12, CID_COLOUR13, CID_COLOUR14, CID_COLOUR15, NID_TOOLBAR_HSEP, CID_INCRW_BRUSH, CID_DECRW_BRUSH, CID_INCRH_BRUSH, CID_DECRH_BRUSH, NID_TOOLBAR_HSEP, CID_INCRHW_BRUSH, CID_DECRHW_BRUSH))
    # }}}
    # {{{ Accelerators (hotkeys) (0x3100-0x3fff)
    AID_EDIT            = (0x3100, TID_ACCELS, (CID_NEW, CID_OPEN, CID_SAVE, CID_EXIT, CID_UNDO, CID_REDO, CID_RECT, CID_CIRCLE, CID_FILL, CID_LINE, CID_TEXT, CID_CLONE_SELECT, CID_MOVE_SELECT))
    # }}}
    # {{{ Lists (0x4100-0x4fff)
    LID_ACCELS          = (0x4100,  TID_LIST, (AID_EDIT))
    LID_MENUS           = (0x4101,  TID_LIST, (MID_FILE, MID_EDIT, MID_TOOLS, MID_HELP))
    LID_TOOLBARS        = (0x4102,  TID_LIST, (BID_TOOLBAR))
    # }}}

    # {{{ _initIcon(self): XXX
    def _initIcon(self):
        iconPathNames = glob(os.path.join("assets", "images", "logo*.bmp"))
        iconPathName = iconPathNames[random.randint(0, len(iconPathNames) - 1)]
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(iconPathName, wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
    # }}}
    # {{{ _initPaletteToolBitmaps(self): XXX
    def _initPaletteToolBitmaps(self):
        paletteDescr = (                                                                                        \
                self.CID_COLOUR00, self.CID_COLOUR01, self.CID_COLOUR02, self.CID_COLOUR03, self.CID_COLOUR04,  \
                self.CID_COLOUR05, self.CID_COLOUR06, self.CID_COLOUR07, self.CID_COLOUR08, self.CID_COLOUR09,  \
                self.CID_COLOUR10, self.CID_COLOUR11, self.CID_COLOUR12, self.CID_COLOUR13, self.CID_COLOUR14,  \
                self.CID_COLOUR15)
        for numColour in range(len(paletteDescr)):
            toolBitmapColour = Colours[numColour][0:4]
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
                Colours[self.lastPanelState["colours"][0]][4],   \
                Colours[self.lastPanelState["colours"][1]][4]))
        if "pathName" in self.lastPanelState:
            if self.lastPanelState["pathName"] != "":
                basePathName = os.path.basename(self.lastPanelState["pathName"])
                textItems.append("Current file: {}".format(basePathName))
                self.SetTitle("{} - roar".format(basePathName))
            else:
                self.SetTitle("roar")
        if "toolName" in self.lastPanelState:
            textItems.append("Current tool: {}".format(                 \
                self.lastPanelState["toolName"]))
        self.statusBar.SetStatusText(" | ".join(textItems))
        if "undoLevel" in self.lastPanelState: 
            if self.lastPanelState["undoLevel"] >= 0:
                self.menuItemsById[self.CID_UNDO[0]].Enable(True)
                toolBar = self.toolBarItemsById[self.CID_UNDO[0]].GetToolBar()
                toolBar.EnableTool(self.CID_UNDO[0], True)
            else:
                self.menuItemsById[self.CID_UNDO[0]].Enable(False)
                toolBar = self.toolBarItemsById[self.CID_UNDO[0]].GetToolBar()
                toolBar.EnableTool(self.CID_UNDO[0], False)
            if self.lastPanelState["undoLevel"] > 0:
                self.menuItemsById[self.CID_REDO[0]].Enable(True)
                toolBar = self.toolBarItemsById[self.CID_REDO[0]].GetToolBar()
                toolBar.EnableTool(self.CID_REDO[0], True)
            else:
                self.menuItemsById[self.CID_REDO[0]].Enable(False)
                toolBar = self.toolBarItemsById[self.CID_REDO[0]].GetToolBar()
                toolBar.EnableTool(self.CID_REDO[0], False)
    # }}}

    # {{{ __del__(self): destructor method
    def __del__(self):
        if self.panelCanvas != None:
            del self.panelCanvas; self.panelCanvas = None;
    # }}}

    #
    # __init__(self, parent, appSize=(840, 630), defaultCanvasPos=(0, 75), defaultCanvasSize=(100, 30), defaultCellSize=(7, 14)): initialisation method
    def __init__(self, parent, appSize=(840, 630), defaultCanvasPos=(0, 75), defaultCanvasSize=(100, 30), defaultCellSize=(7, 14)):
        self._initPaletteToolBitmaps()
        self.panelSkin = super().__init__(parent, wx.ID_ANY, "", size=appSize)
        self.lastPanelState, self.panelCanvas = {}, None
        self._initIcon()

        self.panelCanvas = Canvas(self.panelSkin, parentFrame=self, \
            canvasInterface=GuiCanvasInterface,                     \
            defaultCanvasPos=defaultCanvasPos,                      \
            defaultCanvasSize=defaultCanvasSize,                    \
            defaultCellSize=defaultCellSize)
        self.panelCanvas.canvasInterface.canvasNew(None)

        self.sizerSkin.AddSpacer(5)
        self.sizerSkin.Add(self.panelCanvas, 0, wx.ALL|wx.EXPAND, 14)
        self.panelSkin.SetSizer(self.sizerSkin)
        self.panelSkin.SetAutoLayout(1)
        self.sizerSkin.Fit(self.panelSkin)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
