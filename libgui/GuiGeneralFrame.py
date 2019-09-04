#!/usr/bin/env python3
#
# GuiGeneralFrame.py -- XXX
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import os, sys, wx

#
# Types (0xe000-0xefff)
TID_ACCELS          = (0xe000)
TID_COMMAND         = (0xe001)
TID_LIST            = (0xe002)
TID_MENU            = (0xe003)
TID_NOTHING         = (0xe004)
TID_SELECT          = (0xe005)
TID_TOOLBAR         = (0xe006)

#
# Non-items (0xf000-0xffff)
NID_MENU_SEP        = (0xf000, TID_NOTHING)
NID_TOOLBAR_HSEP    = (0xf001, TID_NOTHING)
NID_TOOLBAR_VSEP    = (0xf002, TID_NOTHING)

class GuiGeneralFrame(wx.Frame):
    """XXX"""

    # {{{ _initAccelTable(self, accelsDescr): XXX
    def _initAccelTable(self, accelsDescr):
        accelTableEntries = [wx.AcceleratorEntry() for n in range(len(accelsDescr[2]))]
        self.accelItemsById = {}
        for numAccel in range(len(accelsDescr[2])):
            accelDescr = accelsDescr[2][numAccel]
            if accelDescr[5] != None:
                self.itemsById[accelDescr[0]] = accelDescr
                accelTableEntries[numAccel].Set(*accelDescr[5], accelDescr[0])
                self.accelItemsById[accelDescr[0]] = accelTableEntries[numAccel]
                self.Bind(wx.EVT_MENU, self.onInput, id=accelDescr[0])
        return accelTableEntries
    # }}}
    # {{{ _initMenus(self, menusDescr): XXX
    def _initMenus(self, menusDescr):
        self.menuItemsById = {}; menuBar = wx.MenuBar();
        for menuDescr in menusDescr:
            menuWindow = wx.Menu()
            for menuItem in menuDescr[4]:
                if menuItem == NID_MENU_SEP:
                    menuWindow.AppendSeparator()
                elif menuItem[1] == TID_SELECT:
                    self.itemsById[menuItem[0]] = menuItem
                    menuItemWindow = menuWindow.AppendRadioItem(menuItem[0], menuItem[3], menuItem[2])
                    if menuItem[5] != None:
                        menuItemWindow.SetAccel(self.accelItemsById[menuItem[0]])
                    self.menuItemsById[menuItem[0]] = menuItemWindow
                    self.Bind(wx.EVT_MENU, self.onInput, menuItemWindow)
                    if menuItem[6] != None:
                        menuItemWindow.Check(menuItem[6])
                else:
                    self.itemsById[menuItem[0]] = menuItem
                    menuItemWindow = menuWindow.Append(menuItem[0], menuItem[3], menuItem[2])
                    if menuItem[5] != None:
                        menuItemWindow.SetAccel(self.accelItemsById[menuItem[0]])
                    self.menuItemsById[menuItem[0]] = menuItemWindow
                    self.Bind(wx.EVT_MENU, self.onInput, menuItemWindow)
                    if menuItem[6] != None:
                        menuItemWindow.Enable(menuItem[6])
            menuBar.Append(menuWindow, menuDescr[3])
        return menuBar
    # }}}
    # {{{ _initToolBars(self, toolBarsDescr, panelSkin): XXX
    def _initToolBars(self, toolBarsDescr, panelSkin):
        self.toolBarItemsById = {}
        self.sizerSkin = wx.BoxSizer(wx.VERTICAL)
        self.toolBars = [None]; numToolBar = 0;
        for toolBarItem in toolBarsDescr[2]:
            if self.toolBars[numToolBar] == None:
                self.toolBars[numToolBar] = wx.ToolBar(panelSkin, -1, style=wx.TB_FLAT | wx.HORIZONTAL | wx.TB_NODIVIDER)
                self.toolBars[numToolBar].SetToolBitmapSize((16,16))
            if toolBarItem == NID_TOOLBAR_HSEP:
                self.toolBars[numToolBar].AddSeparator()
            elif toolBarItem == NID_TOOLBAR_VSEP:
                numToolBar += 1; self.toolBars.append(None);
            elif toolBarItem[1] == TID_SELECT:
                self.itemsById[toolBarItem[0]] = toolBarItem
                toolBarItemWindow = self.toolBars[numToolBar].AddRadioTool(toolBarItem[0], toolBarItem[2], toolBarItem[4][2], shortHelp=toolBarItem[2])
                self.toolBarItemsById[toolBarItem[0]] = toolBarItemWindow
                if toolBarItem[6] != None:
                    toolBarItemWindow.Toggle(toolBarItem[6])
                self.Bind(wx.EVT_TOOL, self.onInput, toolBarItemWindow)
                self.Bind(wx.EVT_TOOL_RCLICKED, self.onInput, toolBarItemWindow)
            else:
                self.itemsById[toolBarItem[0]] = toolBarItem
                toolBarItemWindow = self.toolBars[numToolBar].AddTool(toolBarItem[0], toolBarItem[2], toolBarItem[4][2], toolBarItem[2])
                self.toolBarItemsById[toolBarItem[0]] = toolBarItemWindow
                if toolBarItem[6] != None:
                    toolBarItemWindow.Enable(toolBarItem[6])
                self.Bind(wx.EVT_TOOL, self.onInput, toolBarItemWindow)
                self.Bind(wx.EVT_TOOL_RCLICKED, self.onInput, toolBarItemWindow)
        for numToolBar in range(len(self.toolBars)):
            self.sizerSkin.Add(self.toolBars[numToolBar], 0, wx.ALL|wx.ALIGN_LEFT, 3)
            self.toolBars[numToolBar].Realize()
            self.toolBars[numToolBar].Fit()
    # }}}
    # {{{ _initToolBitmaps(self, toolBarsDescr): XXX
    def _initToolBitmaps(self, toolBarsDescr):
        for toolBarItem in toolBarsDescr[2]:
            if toolBarItem == NID_TOOLBAR_HSEP  \
            or toolBarItem == NID_TOOLBAR_VSEP:
                continue
            elif toolBarItem[4] == None:
                toolBarItem[4] = ["", None, wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, (16,16))]
            elif toolBarItem[4][0] == ""        \
            and  toolBarItem[4][1] != None:
                toolBarItem[4] = ["", None, wx.ArtProvider.GetBitmap(toolBarItem[4][1], wx.ART_TOOLBAR, (16,16))]
            elif toolBarItem[4][0] == ""        \
            and  toolBarItem[4][1] == None:
                toolBarItem[4] = ["", None, toolBarItem[4][2]]
            elif toolBarItem[4][0] != "":
                toolBitmapPathName = os.path.dirname(sys.argv[0])
                toolBitmapPathName = os.path.join(toolBitmapPathName, "assets", "images", toolBarItem[4][0])
                toolBitmap = wx.Bitmap((16,16))
                toolBitmap.LoadFile(toolBitmapPathName, wx.BITMAP_TYPE_ANY)
                toolBarItem[4] = ["", None, toolBitmap]
    # }}}
    # {{{ onInput(self, event): XXX
    def onInput(self, event):
        pass
    # }}}

    #
    # __init__(self, *args, **kwargs): initialisation method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); self.itemsById = {};
        panelSkin = wx.Panel(self, wx.ID_ANY)

        # Initialise accelerators (hotkeys)
        accelTable = wx.AcceleratorTable(self._initAccelTable(self.LID_ACCELS[2]))
        self.SetAcceleratorTable(accelTable)

        # Initialise menu bar, menus & menu items
        # Initialise toolbar & toolbar items
        menuBar = self._initMenus(self.LID_MENUS[2])
        self.SetMenuBar(menuBar)
        self._initToolBitmaps(self.LID_TOOLBARS[2])
        toolBar = self._initToolBars(self.LID_TOOLBARS[2], panelSkin)

        # Initialise status bar
        self.statusBar = self.CreateStatusBar()

        # Set focus on & show window
        self.SetFocus(); self.Show(True);

        return panelSkin

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
