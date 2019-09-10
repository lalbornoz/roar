#!/usr/bin/env python3
#
# GuiFrame.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import os, sys, wx

#
# Decorators
# {{{ GuiCommandDecorator(targetObject)
def GuiCommandDecorator(caption, label, icon, accel, initialState):
    def GuiCommandDecoratorOuter(targetObject):
        if callable(targetObject):
            if not hasattr(targetObject, "attrDict"):
                setattr(targetObject, "attrDict", [])
            targetObject.attrDict = {"caption": caption, "label": label, "icon": icon, "accel": accel, "initialState": initialState, "id": None}
            return targetObject
    return GuiCommandDecoratorOuter
# }}}
# {{{ GuiCommandListDecorator(targetObject)
def GuiCommandListDecorator(idx, caption, label, icon, accel, initialState):
    def GuiCommandListDecoratorOuter(targetObject):
        if callable(targetObject):
            if not hasattr(targetObject, "attrList"):
                setattr(targetObject, "attrList", [])
            targetObject.attrList.insert(0, {"caption": caption, "label": label, "icon": icon, "accel": accel, "initialState": initialState, "id": None, "idx": idx})
            return targetObject
    return GuiCommandListDecoratorOuter
# }}}
# {{{ GuiSelectDecorator(targetObject)
def GuiSelectDecorator(idx, caption, label, icon, accel, initialState):
    def GuiSelectDecoratorOuter(targetObject):
        if callable(targetObject):
            if not hasattr(targetObject, "attrList"):
                setattr(targetObject, "attrList", [])
            setattr(targetObject, "isSelect", True)
            targetObject.attrList.insert(0, {"caption": caption, "label": label, "icon": icon, "accel": accel, "initialState": initialState, "id": None, "idx": idx})
            return targetObject
    return GuiSelectDecoratorOuter
# }}}

#
# Non-items (0xf000-0xffff)
NID_MENU_SEP        = 0xf000
NID_TOOLBAR_HSEP    = 0xf001

class GuiFrame(wx.Frame):
    # {{{ _initIcon(self, iconPathName)
    def _initIcon(self, iconPathName):
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(iconPathName, wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
    # }}}

    # {{{ loadAccels(self, accels)
    def loadAccels(self, accels):
        accelTableEntries = []
        for accel in accels:
            if accel.attrDict["accel"] != None:
                accelTableEntries += [wx.AcceleratorEntry()]
                if accel.attrDict["id"] == None:
                    accel.attrDict["id"] = self.lastId; self.lastId += 1;
                accelTableEntries[-1].Set(*accel.attrDict["accel"], accel.attrDict["id"])
                accel.attrDict["accelEntry"] = accelTableEntries[-1]
                self.itemsById[accel.attrDict["id"]] = accel
                self.Bind(wx.EVT_MENU, self.onMenu, id=accel.attrDict["id"])
        self.SetAcceleratorTable(wx.AcceleratorTable(accelTableEntries))
    # }}}
    # {{{ loadBitmap(self, basePathName, descr, size=(16, 16))
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
    # }}}
    # {{{ loadMenus(self, menus)
    def loadMenus(self, menus):
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
                    self.Bind(wx.EVT_MENU, self.onMenu, menuItemWindow)
                    if menuItem.attrDict["initialState"] != None:
                        if hasattr(menuItem, "isSelect"):
                            menuItemWindow.Check(menuItem.attrDict["initialState"])
                        else:
                            menuItemWindow.Enable(menuItem.attrDict["initialState"])
            menuBar.Append(menuWindow, menu[0])
        self.SetMenuBar(menuBar)
    # }}}
    # {{{ loadToolBars(self, toolBars)
    def loadToolBars(self, toolBars):
        for toolBar in toolBars:
            self.toolBars.append(wx.ToolBar(self.panelSkin, -1, style=wx.TB_FLAT | wx.HORIZONTAL | wx.TB_NODIVIDER))
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
                    self.Bind(wx.EVT_TOOL, self.onMenu, toolBarItemWindow)
                    self.Bind(wx.EVT_TOOL_RCLICKED, self.onMenu, toolBarItemWindow)
                    if toolBarItem.attrDict["initialState"] != None:
                        if hasattr(toolBarItem, "isSelect"):
                            toolBarItemWindow.Toggle(toolBarItem.attrDict["initialState"])
                        else:
                            toolBarItemWindow.Enable(toolBarItem.attrDict["initialState"])
        for toolBar in self.toolBars:
            self.sizerSkin.Add(toolBar, 0, wx.ALIGN_LEFT | wx.ALL, 3)
            toolBar.Realize(); toolBar.Fit();
    # }}}
    # {{{ addWindow(self, window, border=14, expand=False)
    def addWindow(self, window, border=14, expand=False):
        flags = wx.ALL; flags = flags | wx.EXPAND if expand else flags;
        self.sizerSkin.Add(window, 0, flags, border); self.sizerSkin.Fit(self.panelSkin);
    # }}}
    # {{{ onChar(self, event)
    def onChar(self, event):
        event.Skip()
    # }}}
    # {{{ onMenu(self, event)
    def onMenu(self, event):
        eventId = event.GetId(); self.itemsById[eventId](event);
    # }}}
    # {{{ onMouseWheel(self, event)
    def onMouseWheel(self, event):
        event.Skip()
    # }}}

    #
    # __init__(self, iconPathName, size, parent=None, title=""): initialisation method
    def __init__(self, iconPathName, size, parent=None, title=""):
        super().__init__(parent, wx.ID_ANY, title, size=size)
        self.itemsById, self.lastId, self.menuItemsById, self.toolBarItemsById = {}, 0, {}, {}
        self.panelSkin, self.sizerSkin, self.toolBars = wx.Panel(self, wx.ID_ANY), wx.BoxSizer(wx.VERTICAL), []
        self.sizerSkin.AddSpacer(5); self.panelSkin.SetSizer(self.sizerSkin); self.panelSkin.SetAutoLayout(1);
        self._initIcon(iconPathName); self.statusBar = self.CreateStatusBar();
        self.sizerSkin.Fit(self.panelSkin); self.SetFocus(); self.Show(True);
        for event, f in ((wx.EVT_CHAR, self.onChar), (wx.EVT_MENU, self.onMenu), (wx.EVT_MOUSEWHEEL, self.onMouseWheel)):
            self.Bind(event, f)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
