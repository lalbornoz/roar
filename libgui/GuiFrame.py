#!/usr/bin/env python3
#
# GuiFrame.py 
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Canvas import Canvas
from GuiCanvasColours import Colours
from GuiCanvasPanel import GuiCanvasPanel
from GuiCanvasWxBackend import GuiCanvasWxBackend

from glob import glob
import os, random, sys, wx

#
# Non-items (0xf000-0xffff)
NID_MENU_SEP     = 0xf000
NID_TOOLBAR_HSEP = 0xf001

class GuiFrame(wx.Frame):
    # {{{ _initAccelTable(self, accels)
    def _initAccelTable(self, accels):
        accelTableEntries = []
        for accel in accels:
            if accel.attrDict["accel"] != None:
                accelTableEntries += [wx.AcceleratorEntry()]
                if accel.attrDict["id"] == None:
                    accel.attrDict["id"] = self.lastId; self.lastId += 1;
                accelTableEntries[-1].Set(*accel.attrDict["accel"], accel.attrDict["id"])
                accel.attrDict["accelEntry"] = accelTableEntries[-1]
                self.itemsById[accel.attrDict["id"]] = accel
                self.Bind(wx.EVT_MENU, self.onInput, id=accel.attrDict["id"])
        self.SetAcceleratorTable(wx.AcceleratorTable(accelTableEntries))
    # }}}
    # {{{ _initIcon(self)
    def _initIcon(self):
        iconPathNames = glob(os.path.join("assets", "images", "logo*.bmp"))
        iconPathName = iconPathNames[random.randint(0, len(iconPathNames) - 1)]
        icon = wx.Icon(); icon.CopyFromBitmap(wx.Bitmap(iconPathName, wx.BITMAP_TYPE_ANY)); self.SetIcon(icon);
    # }}}
    # {{{ _initMenus(self, menus)
    def _initMenus(self, menus):
        menuBar = wx.MenuBar()
        for menu in menus:
            menuWindow = wx.Menu()
            for menuItem in menu[1:]:
                if menuItem == NID_MENU_SEP:
                    menuWindow.AppendSeparator()
                else:
                    if menuItem.attrDict["id"] == None:
                        menuItem.attrDict["id"] = self.lastId; self.lastId += 1;
                    self.itemsById[menuItem.attrDict["id"]] = menuItem
                    if hasattr(menuItem, "isSelect"):
                        menuItemWindow = menuWindow.AppendRadioItem(menuItem.attrDict["id"], menuItem.attrDict["label"], menuItem.attrDict["caption"])
                    else:
                        menuItemWindow = menuWindow.Append(menuItem.attrDict["id"], menuItem.attrDict["label"], menuItem.attrDict["caption"])
                    if menuItem.attrDict["accel"] != None:
                        menuItemWindow.SetAccel(menuItem.attrDict["accelEntry"])
                    self.menuItemsById[menuItem.attrDict["id"]] = menuItemWindow
                    self.Bind(wx.EVT_MENU, self.onInput, menuItemWindow)
                    if menuItem.attrDict["initialState"] != None:
                        if hasattr(menuItem, "isSelect"):
                            menuItemWindow.Check(menuItem.attrDict["initialState"])
                        else:
                            menuItemWindow.Enable(menuItem.attrDict["initialState"])
            menuBar.Append(menuWindow, menu[0])
        self.SetMenuBar(menuBar)
    # }}}
    # {{{ _initStatusBar(self)
    def _initStatusBar(self):
        self.statusBar = self.CreateStatusBar()
    # }}}
    # {{{ _initToolBars(self, toolBars, panelSkin)
    def _initToolBars(self, toolBars, panelSkin):
        for toolBar in toolBars:
            self.toolBars.append(wx.ToolBar(panelSkin, -1, style=wx.TB_FLAT | wx.HORIZONTAL | wx.TB_NODIVIDER))
            self.toolBars[-1].SetToolBitmapSize((16, 16))
            for toolBarItem in toolBar:
                if toolBarItem == NID_TOOLBAR_HSEP:
                    self.toolBars[-1].AddSeparator()
                else:
                    if toolBarItem.attrDict["id"] == None:
                        toolBarItem.attrDict["id"] = self.lastId; self.lastId += 1;
                    self.itemsById[toolBarItem.attrDict["id"]] = toolBarItem
                    if hasattr(toolBarItem, "isSelect"):
                        toolBarItemWindow = self.toolBars[-1].AddRadioTool(toolBarItem.attrDict["id"], toolBarItem.attrDict["caption"], toolBarItem.attrDict["icon"][2], shortHelp=toolBarItem.attrDict["label"])
                    else:
                        toolBarItemWindow = self.toolBars[-1].AddTool(toolBarItem.attrDict["id"], toolBarItem.attrDict["caption"], toolBarItem.attrDict["icon"][2], shortHelp=toolBarItem.attrDict["label"])
                    self.toolBarItemsById[toolBarItem.attrDict["id"]] = toolBarItemWindow
                    self.Bind(wx.EVT_TOOL, self.onInput, toolBarItemWindow)
                    self.Bind(wx.EVT_TOOL_RCLICKED, self.onInput, toolBarItemWindow)
                    if toolBarItem.attrDict["initialState"] != None:
                        if hasattr(toolBarItem, "isSelect"):
                            toolBarItemWindow.Toggle(toolBarItem.attrDict["initialState"])
                        else:
                            toolBarItemWindow.Enable(toolBarItem.attrDict["initialState"])
        for toolBar in self.toolBars:
            self.sizerSkin.Add(toolBar, 0, wx.ALIGN_LEFT | wx.ALL, 3)
            toolBar.Realize(); toolBar.Fit();
    # }}}
    # {{{ _initToolBitmaps(self, toolBars)
    def _initToolBitmaps(self, toolBars):
        for toolBar in toolBars:
            for toolBarItem in toolBar:
                if   toolBarItem == NID_TOOLBAR_HSEP:
                    continue
                elif toolBarItem.attrDict["icon"] == None:
                    toolBarItem.attrDict["icon"] = ["", None, wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, (16, 16))]
                elif (toolBarItem.attrDict["icon"][0] == "")    \
                and  (toolBarItem.attrDict["icon"][1] != None):
                    toolBarItem.attrDict["icon"] = ["", None, wx.ArtProvider.GetBitmap(toolBarItem.attrDict["icon"][1], wx.ART_TOOLBAR, (16, 16))]
                elif (toolBarItem.attrDict["icon"][0] == "")    \
                and  (toolBarItem.attrDict["icon"][1] == None):
                    toolBarItem.attrDict["icon"] = ["", None, toolBarItem.attrDict["icon"][2]]
                elif toolBarItem.attrDict["icon"][0] != "":
                    toolBitmapPathName = os.path.dirname(sys.argv[0])
                    toolBitmapPathName = os.path.join(toolBitmapPathName, "assets", "images", toolBarItem.attrDict["icon"][0])
                    toolBitmap = wx.Bitmap((16, 16))
                    toolBitmap.LoadFile(toolBitmapPathName, wx.BITMAP_TYPE_ANY)
                    toolBarItem.attrDict["icon"] = ["", None, toolBitmap]
    # }}}

    # {{{ onChar(self, event)
    def onChar(self, event):
        self.canvasPanel.onPanelInput(event)
    # }}}
    # {{{ onInput(self, event)
    def onInput(self, event):
        eventId = event.GetId(); self.itemsById[eventId](self.canvasPanel.interface, event);
    # }}}
    # {{{ onMouseWheel(self, event)
    def onMouseWheel(self, event):
        self.canvasPanel.GetEventHandler().ProcessEvent(event)
    # }}}

    #
    # __init__(self, canvasInterface, parent, appSize=(840, 630), defaultCanvasPos=(0, 75), defaultCanvasSize=(100, 30), defaultCellSize=(7, 14)): initialisation method
    def __init__(self, canvasInterface, parent, appSize=(840, 630), defaultCanvasPos=(0, 75), defaultCanvasSize=(100, 30), defaultCellSize=(7, 14)):
        super().__init__(parent, wx.ID_ANY, "", size=appSize)
        self.itemsById, self.menuItemsById, self.toolBarItemsById = {}, {}, {}; self.lastId = 0;
        self.panelSkin, self.sizerSkin, self.toolBars = wx.Panel(self, wx.ID_ANY), wx.BoxSizer(wx.VERTICAL), []

        self.canvas, self.canvasPanel = Canvas(defaultCanvasSize), None
        self.canvasPanel = GuiCanvasPanel(self.panelSkin, self, GuiCanvasWxBackend, self.canvas, defaultCanvasPos, defaultCanvasSize, defaultCellSize, canvasInterface)

        # Initialise accelerators (hotkeys)
        # Initialise icon
        # Initialise menu bar, menus & menu items
        # Initialise status bar
        # Initialise toolbar & toolbar items
        self._initAccelTable(self.canvasPanel.interface.accels)
        self._initIcon()
        self._initMenus(self.canvasPanel.interface.menus)
        self._initStatusBar()
        self._initToolBitmaps(self.canvasPanel.interface.toolBars)
        self._initToolBars(self.canvasPanel.interface.toolBars, self.panelSkin)

        self.sizerSkin.AddSpacer(5)
        self.sizerSkin.Add(self.canvasPanel, 0, wx.ALL | wx.EXPAND, 14)
        self.panelSkin.SetSizer(self.sizerSkin)
        self.panelSkin.SetAutoLayout(1)
        self.sizerSkin.Fit(self.panelSkin)

        self.canvasPanel.interface.canvasNew(None)
        self.canvasPanel.interface.canvasTool(self.canvasPanel.interface.canvasTool, 5)(self.canvasPanel.interface, None)
        self.canvasPanel.interface.update(brushSize=self.canvasPanel.brushSize, colours=self.canvasPanel.brushColours)

        self.Bind(wx.EVT_CHAR, self.onChar)
        self.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)

        # Set focus on & show window
        self.SetFocus(); self.Show(True);

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
