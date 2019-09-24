#!/usr/bin/env python3
#
# GuiFrame.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import os, sys, wx, wx.lib.agw.aui

#
# Decorators
def GuiCommandDecorator(caption, label, icon, accel, initialState):
    def GuiCommandDecoratorOuter(targetObject):
        if callable(targetObject):
            if not hasattr(targetObject, "attrDict"):
                setattr(targetObject, "attrDict", [])
            targetObject.attrDict = {"caption": caption, "label": label, "icon": icon, "accel": accel, "initialState": initialState, "id": None}
            return targetObject
    return GuiCommandDecoratorOuter

def GuiCommandListDecorator(idx, caption, label, icon, accel, initialState):
    def GuiCommandListDecoratorOuter(targetObject):
        if callable(targetObject):
            if not hasattr(targetObject, "attrList"):
                setattr(targetObject, "attrList", [])
            targetObject.attrList.insert(0, {"caption": caption, "label": label, "icon": icon, "accel": accel, "initialState": initialState, "id": None, "idx": idx})
            return targetObject
    return GuiCommandListDecoratorOuter

def GuiSelectDecorator(idx, caption, label, icon, accel, initialState):
    def GuiSelectDecoratorOuter(targetObject):
        if callable(targetObject):
            if not hasattr(targetObject, "attrList"):
                setattr(targetObject, "attrList", [])
            setattr(targetObject, "isSelect", True)
            targetObject.attrList.insert(0, {"caption": caption, "label": label, "icon": icon, "accel": accel, "initialState": initialState, "id": None, "idx": idx})
            return targetObject
    return GuiSelectDecoratorOuter

def GuiSubMenuDecorator(caption, label, icon, accel, initialState):
    def GuiSubMenuDecoratorOuter(targetObject):
        if callable(targetObject):
            if not hasattr(targetObject, "attrDict"):
                setattr(targetObject, "attrDict", [])
            setattr(targetObject, "isSubMenu", True)
            targetObject.attrDict = {"caption": caption, "label": label, "icon": icon, "accel": accel, "initialState": initialState, "id": None, "menu":None}
            return targetObject
    return GuiSubMenuDecoratorOuter

class GuiToolBarArtProvider(wx.lib.agw.aui.AuiDefaultToolBarArt):
    def DrawBackground(self, dc, wnd, _rect, horizontal=True):
        dc.SetBrush(wx.Brush(wx.Colour(240, 240, 240, 0), wx.BRUSHSTYLE_SOLID)); dc.SetPen(wx.Pen(wx.Colour(240, 240, 240, 0), 1));
        dc.DrawRectangle(*_rect)
        dc.SetPen(wx.Pen(wx.Colour(180, 180, 180, 0), 1))
        dc.DrawLine(0, _rect[3]-1, _rect[2], _rect[3]-1); dc.DrawLine(_rect[2]-1, 0, _rect[2]-1, _rect[3]-1);
        dc.SetPen(wx.Pen(wx.Colour(255, 255, 255, 0), 1))
        dc.DrawLine(0, 0, _rect[2]-1, 0); dc.DrawLine(0, 0, 0, _rect[3]-1);

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

#
# Non-items (0xf000-0xffff)
NID_MENU_SEP        = 0xf000
NID_TOOLBAR_HSEP    = 0xf001

class GuiFrame(wx.Frame):
    def _initIcon(self, iconPathName):
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(iconPathName, wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

    def _initMenu(self, menuItem, menuWindow):
        if menuItem == NID_MENU_SEP:
            menuWindow.AppendSeparator()
        else:
            if menuItem.attrDict["id"] == None:
                menuItem.attrDict["id"] = wx.NewId()
            self.itemsById[menuItem.attrDict["id"]] = menuItem
            if hasattr(menuItem, "isSelect"):
                menuItemWindow = menuWindow.AppendRadioItem(menuItem.attrDict["id"], menuItem.attrDict["label"], menuItem.attrDict["caption"])
            elif hasattr(menuItem, "isSubMenu"):
                menuItem.attrDict["menu"] = wx.Menu()
                menuItemWindow = menuWindow.AppendSubMenu(menuItem.attrDict["menu"], menuItem.attrDict["label"], menuItem.attrDict["caption"])
            else:
                menuItemWindow = menuWindow.Append(menuItem.attrDict["id"], menuItem.attrDict["label"], menuItem.attrDict["caption"])
            if menuItem.attrDict["accel"] != None:
                menuItemWindow.SetAccel(menuItem.attrDict["accelEntry"])
            self.menuItemsById[menuItem.attrDict["id"]] = menuItemWindow
            self.Bind(wx.EVT_MENU, self.onMenu, menuItemWindow)
            if menuItem.attrDict["initialState"] != None:
                if hasattr(menuItem, "isSelect"):
                    menuItemWindow.Check(menuItem.attrDict["initialState"])
                else:
                    menuItemWindow.Enable(menuItem.attrDict["initialState"])

    def loadAccels(self, accelsIn, menus, toolBars):
        def loadAccels_(accels):
            nonlocal accelTableEntries
            accels_ = []
            for accel in accels:
                if type(accel) == tuple:
                    accels_ += accel[1:]
                else:
                    accels_ += [accel]
            for accel in accels_:
                if  (not accel in [NID_MENU_SEP, NID_TOOLBAR_HSEP]) \
                and (accel.attrDict["accel"] != None):
                    accelTableEntries += [wx.AcceleratorEntry()]
                    if accel.attrDict["id"] == None:
                        accel.attrDict["id"] = wx.NewId()
                    accelTableEntries[-1].Set(*accel.attrDict["accel"], accel.attrDict["id"])
                    accel.attrDict["accelEntry"] = accelTableEntries[-1]
                    self.itemsById[accel.attrDict["id"]] = accel
                    self.Bind(wx.EVT_MENU, self.onMenu, id=accel.attrDict["id"])
        accelTableEntries = []
        [loadAccels_(accel) for accel in accelsIn]; [loadAccels_(menu[1:]) for menu in menus]; [loadAccels_(toolBar) for toolBar in toolBars];
        self.SetAcceleratorTable(wx.AcceleratorTable(accelTableEntries))

    def loadBitmap(self, basePathName, descr, size=(16, 16)):
        if descr == None:
            descr = ["", None, wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, size)]
        elif (descr[0] == "") and (descr[1] != None):
            descr = ["", None, wx.ArtProvider.GetBitmap(descr[1], wx.ART_TOOLBAR, size)]
        elif descr[0] != "":
            bitmap, bitmapPathName = wx.Bitmap((16, 16)), os.path.join(basePathName, descr[0])
            bitmap.LoadFile(bitmapPathName, wx.BITMAP_TYPE_ANY)
            descr = ["", None, bitmap]
        elif len(descr) == 3:
            descr = ("", None, descr[2])
        return descr

    def loadMenus(self, menus):
        self.menuBar = wx.MenuBar()
        for menu in menus:
            menuWindow = wx.Menu()
            for menuItem in menu[1:]:
                if type(menuItem) == tuple:
                    menuSubWindow = wx.Menu()
                    for menuSubItem in menuItem[1:]:
                        self._initMenu(menuSubItem, menuSubWindow)
                    menuWindow.AppendSubMenu(menuSubWindow, menuItem[0], menuItem[0])
                else:
                    self._initMenu(menuItem, menuWindow)
            self.menuBar.Append(menuWindow, menu[0])
        self.SetMenuBar(self.menuBar)

    def loadToolBars(self, toolBars):
        for toolBar in toolBars:
            self.toolBars.append(wx.lib.agw.aui.AuiToolBar(self.panelSkin, -1))
            self.toolBars[-1].SetArtProvider(GuiToolBarArtProvider())
            self.toolBars[-1].SetToolBitmapSize((16, 16))
            for toolBarItem in toolBar:
                if toolBarItem == NID_TOOLBAR_HSEP:
                    self.toolBars[-1].AddSeparator()
                else:
                    if toolBarItem.attrDict["id"] == None:
                        toolBarItem.attrDict["id"] = wx.NewId()
                    self.itemsById[toolBarItem.attrDict["id"]] = toolBarItem
                    if hasattr(toolBarItem, "isSelect"):
                        toolBarItemWindow = self.toolBars[-1].AddRadioTool(toolBarItem.attrDict["id"], toolBarItem.attrDict["caption"], toolBarItem.attrDict["icon"][2], wx.NullBitmap, short_help_string=toolBarItem.attrDict["caption"])
                    else:
                        toolBarItemWindow = self.toolBars[-1].AddTool(toolBarItem.attrDict["id"], toolBarItem.attrDict["caption"], toolBarItem.attrDict["icon"][2], wx.NullBitmap, wx.ITEM_NORMAL, short_help_string=toolBarItem.attrDict["caption"])
                    self.toolBarItemsById[toolBarItem.attrDict["id"]] = (self.toolBars[-1], toolBarItemWindow,)
                    self.Bind(wx.EVT_TOOL, self.onMenu, toolBarItemWindow)
                    self.Bind(wx.EVT_TOOL_RCLICKED, self.onMenu, toolBarItemWindow)
                    if toolBarItem.attrDict["initialState"] != None:
                        if hasattr(toolBarItem, "isSelect"):
                            if toolBarItem.attrDict["initialState"]:
                                self.toolBars[-1].ToggleTool(toolBarItemWindow, True)
                        else:
                            self.toolBars[-1].EnableTool(toolBarItem.attrDict["id"], toolBarItem.attrDict["initialState"])
        self.toolBars[-1].Refresh()
        for toolBar in self.toolBars:
            self.sizerSkin.Add(toolBar, 0, wx.ALIGN_LEFT | wx.ALL, 3)
            toolBar.Realize(); toolBar.Fit();

    def addWindow(self, window, border=14, expand=False):
        flags = wx.ALL; flags = flags | wx.EXPAND if expand else flags;
        self.sizerSkin.Add(window, 0, flags, border); self.sizerSkin.Fit(self.panelSkin);

    def onChar(self, event):
        event.Skip()

    def onMenu(self, event):
        eventId = event.GetId()
        if eventId in self.itemsById:
            self.itemsById[eventId](event)
        else:
            event.Skip()

    def onMouseWheel(self, event):
        event.Skip()

    def __init__(self, iconPathName, size, parent=None, title=""):
        super().__init__(parent, wx.ID_ANY, title, size=size)
        self.itemsById, self.menuItemsById, self.toolBarItemsById = {}, {}, {}
        self.panelSkin, self.sizerSkin, self.toolBars = wx.Panel(self, wx.ID_ANY), wx.BoxSizer(wx.VERTICAL), []
        self.sizerSkin.AddSpacer(5); self.panelSkin.SetSizer(self.sizerSkin); self.panelSkin.SetAutoLayout(1);
        self._initIcon(iconPathName); self.statusBar = self.CreateStatusBar();
        self.sizerSkin.Fit(self.panelSkin); self.SetFocus(); self.Show(True);
        for event, f in ((wx.EVT_CHAR, self.onChar), (wx.EVT_MENU, self.onMenu), (wx.EVT_MOUSEWHEEL, self.onMouseWheel)):
            self.Bind(event, f)

class GuiMiniFrame(wx.MiniFrame):
    def __init__(self, parent, size, title, pos=wx.DefaultPosition):
        super().__init__(parent, id=wx.ID_ANY, pos=pos, size=size, title=title)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
