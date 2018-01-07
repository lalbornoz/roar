#!/usr/bin/env python3
#
# MiRCARTGeneralFrame.py -- XXX
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

import os, wx

#
# Types
TID_COMMAND         = (0x001)
TID_MENU            = (0x002)
TID_NOTHING         = (0x003)
TID_SELECT          = (0x004)
TID_TOOLBAR         = (0x005)
TID_ACCELS          = (0x006)

class MiRCARTGeneralFrame(wx.Frame):
    """XXX"""
    menuItemsById = toolBarItemsById = None
    statusBar = toolBar = None

    # {{{ _initAccelTable(self, accelsDescr, handler): XXX
    def _initAccelTable(self, accelsDescr, handler):
        accelTableEntries = [wx.AcceleratorEntry() for n in range(len(accelsDescr[2]))]
        for numAccel in range(len(accelsDescr[2])):
            accelDescr = accelsDescr[2][numAccel]
            if accelDescr[5] != None:
                accelTableEntries[numAccel].Set(*accelDescr[5], accelDescr[0])
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
                elif menuItem[1] == TID_SELECT:
                    menuItemWindow = menuWindow.AppendRadioItem(menuItem[0], menuItem[3], menuItem[2])
                    self.menuItemsById[menuItem[0]] = menuItemWindow
                    self.Bind(wx.EVT_MENU, handler, menuItemWindow)
                    if len(menuItem) == 7:
                        menuItemWindow.Check(menuItem[6])
                else:
                    menuItemWindow = menuWindow.Append(menuItem[0], menuItem[3], menuItem[2])
                    self.menuItemsById[menuItem[0]] = menuItemWindow
                    self.Bind(wx.EVT_MENU, handler, menuItemWindow)
                    if len(menuItem) == 7:
                        menuItemWindow.Enable(menuItem[6])
            menuBar.Append(menuWindow, menuDescr[3])
    # }}}
    # {{{ _initToolBars(self, toolBar, toolBarsDescr, handler): XXX
    def _initToolBars(self, toolBar, toolBarsDescr, handler):
        for toolBarDescr in toolBarsDescr:
            for toolBarItem in toolBarDescr[2]:
                if toolBarItem == self.NID_TOOLBAR_SEP:
                    toolBar.AddSeparator()
                else:
                    if toolBarItem[4] != None:
                        toolBarItemIcon = wx.ArtProvider.GetBitmap(     \
                            toolBarItem[4], wx.ART_TOOLBAR, (16,16))
                    else:
                        toolBarItemIcon = wx.ArtProvider.GetBitmap(     \
                            wx.ART_HELP, wx.ART_TOOLBAR, (16,16))
                    toolBarItemWindow = self.toolBar.AddTool(           \
                        toolBarItem[0], toolBarItem[2], toolBarItemIcon)
                    self.toolBarItemsById[toolBarItem[0]] = toolBarItemWindow
                    if  len(toolBarItem) == 7                           \
                    and toolBarItem[1] == TID_COMMAND:
                        toolBarItemWindow.Enable(toolBarItem[6])
                    self.Bind(wx.EVT_TOOL, handler, toolBarItemWindow)
                    self.Bind(wx.EVT_TOOL_RCLICKED, handler, toolBarItemWindow)
    # }}}
    # {{{ onClose(self, event): XXX
    def onClose(self, event):
        self.Destroy(); self.__del__();
    # }}}
    # {{{ onFrameCommand(self, event): XXX
    def onFrameCommand(self, event):
        pass
    # }}}

    #
    # __init__(self, *args, **kwargs): initialisation method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        panelSkin = wx.Panel(self, wx.ID_ANY)

        # Initialise menu bar, menus & menu items
        self.menuItemsById = {}; menuBar = wx.MenuBar();
        self._initMenus(menuBar,                    \
            [self.MID_FILE, self.MID_EDIT, self.MID_TOOLS],
            self.onFrameCommand)
        self.SetMenuBar(menuBar)

        # Initialise toolbar & toolbar items
        self.toolBarItemsById = {}
        self.toolBar = wx.ToolBar(panelSkin, -1,    \
            style=wx.HORIZONTAL|wx.TB_FLAT|wx.TB_NODIVIDER)
        self.toolBar.SetToolBitmapSize((16,16))
        self._initToolBars(self.toolBar, [self.BID_TOOLBAR], self.onFrameCommand)
        self.toolBar.Realize(); self.toolBar.Fit();

        # Initialise accelerators (hotkeys)
        accelTable = wx.AcceleratorTable(           \
            self._initAccelTable(self.AID_EDIT, self.onFrameCommand))
        self.SetAcceleratorTable(accelTable)

        # Initialise status bar
        self.statusBar = self.CreateStatusBar()

        # Bind event handlers
        self.Bind(wx.EVT_CLOSE, self.onClose)

        # Set focus on & show window
        self.SetFocus(); self.Show(True);

        return panelSkin

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
