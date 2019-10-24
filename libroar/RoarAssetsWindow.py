#!/usr/bin/env python3
#
# RoarAssetsWindow.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Canvas import Canvas
from GuiFrame import GuiMiniFrame
from GuiWindow import GuiWindow
from RtlPlatform import getLocalConfPathName
import json, os, sys, wx

class RoarAssetsWindow(GuiMiniFrame):
    def _import(self, f, pathName):
        rc = False
        self.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        try:
            canvas = Canvas((0, 0))
            rc, error, newMap, newPathName, newSize = f(canvas, pathName)
            if rc:
                self.update(canvas, newSize, newMap)
        except FileNotFoundError as e:
            rc, error, newMap, newPathName, newSize = False, str(e), None, None, None
        self.SetCursor(wx.Cursor(wx.NullCursor))
        return rc, error, canvas, newMap, newPathName, newSize

    def _importFiles(self, f, wildcard):
        resultList = []
        with wx.FileDialog(self, "Load...", os.getcwd(), "", wildcard, wx.FD_MULTIPLE | wx.FD_OPEN) as dialog:
            if self.lastDir != None:
                dialog.SetDirectory(self.lastDir)
            if dialog.ShowModal() == wx.ID_CANCEL:
                resultList += [[None, "(cancelled)", None, None, None, None]]
            else:
                for pathName in dialog.GetPaths():
                    resultList += [self._import(f, pathName)]
                    lastDir = os.path.dirname(pathName)
                    if self.lastDir != lastDir:
                        self.lastDir = lastDir; self._storeLastDir(self.lastDir);
        return resultList

    def _load_list(self, pathName):
        try:
            with open(pathName, "r") as fileObject:
                try:
                    for line in fileObject.readlines():
                        line = line.rstrip("\r\n")
                        if not os.path.isabs(line):
                            line = os.path.join(os.path.dirname(pathName), line)
                        def importmIRC(canvas, pathName):
                            rc, error = canvas.importStore.importTextFile(pathName)
                            return (rc, error, canvas.importStore.outMap, pathName, canvas.importStore.inSize)
                        rc, error, canvas, newMap, newPathName, newSize = self._import(importmIRC, line)
                        if rc:
                            self.currentIndex = self.listView.GetItemCount()
                            self.canvasList[self.currentIndex] = [canvas, newPathName]
                            self.listView.InsertItem(self.currentIndex, "")
                            idx = -1
                            while True:
                                idx = self.listView.GetNextSelected(idx)
                                if idx != -1:
                                    self.listView.Select(idx, on=0)
                                else:
                                    break
                            self.listView.Select(self.currentIndex, on=1)
                            self.listView.SetFocus()
                            [self.listView.SetItem(self.currentIndex, col, label) for col, label in zip((0, 1), (os.path.basename(newPathName), "{}x{}".format(*newSize)))]
                            [self.listView.SetColumnWidth(col, wx.LIST_AUTOSIZE) for col in (0, 1)]
                        else:
                            with wx.MessageDialog(self, "Error: {}".format(error), "", wx.CANCEL | wx.OK | wx.OK_DEFAULT) as dialog:
                                dialogChoice = dialog.ShowModal()
                                if dialogChoice == wx.ID_CANCEL:
                                    self.SetCursor(wx.Cursor(wx.NullCursor)); break;
                except:
                    self.SetCursor(wx.Cursor(wx.NullCursor))
                    with wx.MessageDialog(self, "Error: {}".format(str(sys.exc_info()[1])), "", wx.OK | wx.OK_DEFAULT) as dialog:
                        dialogChoice = dialog.ShowModal()
        except FileNotFoundError as e:
            self.SetCursor(wx.Cursor(wx.NullCursor))
            with wx.MessageDialog(self, "Error: {}".format(str(e)), "", wx.OK | wx.OK_DEFAULT) as dialog:
                dialogChoice = dialog.ShowModal()

    def _loadLastDir(self):
        localConfFileName = getLocalConfPathName("RecentAssetsDir.txt")
        if os.path.exists(localConfFileName):
            with open(localConfFileName, "r", encoding="utf-8") as inFile:
                self.lastDir = inFile.read().rstrip("\r\n")

    def _removeAsset(self, idx):
        del self.canvasList[idx]; self.listView.DeleteItem(idx);
        itemCount = self.listView.GetItemCount()
        if itemCount > 0:
            self.listView.Select(self.currentIndex, on=0)
            for numCanvas in [n for n in sorted(self.canvasList.keys()) if n >= idx]:
                self.canvasList[numCanvas - 1] = self.canvasList[numCanvas]; del self.canvasList[numCanvas];
            [self.listView.SetColumnWidth(col, wx.LIST_AUTOSIZE) for col in (0, 1)]
            if (idx == 0) or (idx >= itemCount):
                idx = 0 if itemCount > 0 else None
            else:
                idx = idx if idx < itemCount else None
            self.currentIndex = idx
            if self.currentIndex != None:
                self.listView.Select(self.currentIndex, on=1)
                self.drawCanvas(self.canvasList[self.currentIndex][0])
        else:
            self.currentIndex = None
            [self.listView.SetColumnWidth(col, wx.LIST_AUTOSIZE_USEHEADER) for col in (0, 1)]
            self.drawCanvas(Canvas((0, 0)))
        return self.currentIndex

    def _storeLastDir(self, pathName):
        localConfFileName = getLocalConfPathName("RecentAssetsDir.txt")
        with open(localConfFileName, "w", encoding="utf-8") as outFile:
            print(pathName, file=outFile)

    def _updateScrollBars(self):
        clientSize = self.panelCanvas.GetClientSize()
        if self.currentIndex != None:
            panelSize = [a * b for a, b in zip(self.canvasList[self.currentIndex][0].size, self.backend.cellSize)]
        elif self.panelCanvas.size != None:
            panelSize = list(self.panelCanvas.size)
        else:
            return
        if (panelSize[0] > clientSize[0]) or (panelSize[1] > clientSize[1]):
            self.scrollFlag = True; super(wx.ScrolledWindow, self.panelCanvas).SetVirtualSize(panelSize);
        elif self.scrollFlag    \
        and  ((panelSize[0] <= clientSize[0]) or (panelSize[1] <= clientSize[1])):
            self.scrollFlag = False; super(wx.ScrolledWindow, self.panelCanvas).SetVirtualSize((0, 0));

    def drawCanvas(self, canvas):
        panelSize = [a * b for a, b in zip(canvas.size, self.backend.cellSize)]
        self.panelCanvas.SetMinSize(panelSize); self.panelCanvas.SetSize(wx.DefaultCoord, wx.DefaultCoord, *panelSize);
        curWindow = self.panelCanvas
        while curWindow != None:
            curWindow.Layout(); curWindow = curWindow.GetParent();
        self.backend.resize(canvas.size)
        eventDc = self.backend.getDeviceContext(self.panelCanvas.GetClientSize(), self.panelCanvas)
        eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
        patches = []
        for numRow in range(canvas.size[1]):
            for numCol in range(canvas.size[0]):
                patches += [[numCol, numRow, *canvas.map[numRow][numCol]]]
        self.backend.drawPatches(canvas, eventDc, patches, isCursor=False)
        eventDc.SetDeviceOrigin(*eventDcOrigin)

    def onPaint(self, event):
        self.backend.onPaint(self.panelCanvas.GetClientSize(), self.panelCanvas, self.panelCanvas.GetViewStart())

    def onPanelLeftDown(self, event):
        self.panelCanvas.SetFocus()
        if (self.currentIndex != None):
            dataText = json.dumps((self.canvasList[self.currentIndex][0].map, self.canvasList[self.currentIndex][0].size,))
            textDataObject = wx.TextDataObject(dataText)
            dropSource = wx.DropSource(event.GetEventObject())
            dropSource.SetData(textDataObject)
            result = dropSource.DoDragDrop(True)
        event.Skip()

    def onPanelPaint(self, event):
        self.backend.onPaint(self.panelCanvas.GetClientSize(), self.panelCanvas, self.panelCanvas.GetViewStart())

    def onPanelSize(self, event):
        self._updateScrollBars(); event.Skip();

    def resize(self, canvas, newSize):
        oldSize = [0, 0] if canvas.map == None else canvas.size
        deltaSize = [b - a for a, b in zip(oldSize, newSize)]
        if canvas.resize((1, 1,), newSize, False):
            panelSize = [a * b for a, b in zip(canvas.size, self.backend.cellSize)]
            self.panelCanvas.SetMinSize(panelSize); self.panelCanvas.SetSize(wx.DefaultCoord, wx.DefaultCoord, *panelSize);
            curWindow = self.panelCanvas
            while curWindow != None:
                curWindow.Layout(); curWindow = curWindow.GetParent();
            self.backend.resize(newSize)
            eventDc = self.backend.getDeviceContext(self.panelCanvas.GetClientSize(), self.panelCanvas)
            eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
            patches = []
            if deltaSize[0] > 0:
                for numRow in range(oldSize[1]):
                    for numNewCol in range(oldSize[0], newSize[0]):
                        patches += [[numNewCol, numRow, 1, 1, 0, " "]]
            if deltaSize[1] > 1:
                for numNewRow in range(oldSize[1], newSize[1]):
                    for numNewCol in range(newSize[0]):
                        patches += [[numNewCol, numNewRow, 1, 1, 0, " "]]
            self.backend.drawPatches(canvas, eventDc, patches, isCursor=False)
            eventDc.SetDeviceOrigin(*eventDcOrigin)

    def update(self, canvas, newSize, newCanvas=None):
        self.resize(canvas, newSize);
        canvas.update(newSize, newCanvas);
        eventDc = self.backend.getDeviceContext(self.panelCanvas.GetClientSize(), self.panelCanvas)
        eventDcOrigin = eventDc.GetDeviceOrigin(); eventDc.SetDeviceOrigin(0, 0);
        patches = []
        for numRow in range(canvas.size[1]):
            for numCol in range(canvas.size[0]):
                patches += [[numCol, numRow, *canvas.map[numRow][numCol]]]
        self.backend.drawPatches(canvas, eventDc, patches, isCursor=False)
        eventDc.SetDeviceOrigin(*eventDcOrigin)

    def onImportAnsi(self, event):
        event.Skip()

    def onImportFromClipboard(self, event):
        event.Skip()

    def onImportSauce(self, event):
        event.Skip()

    def onChar(self, event):
        if  (event.GetModifiers() == wx.MOD_NONE)   \
        and (event.GetKeyCode() in (wx.WXK_DOWN, wx.WXK_UP)):
            self.listView.SetFocus()
            return wx.PostEvent(self.listView, event)
        else:
            event.Skip()

    def onClearList(self, event):
        while len(self.canvasList):
            self._removeAsset(list(self.canvasList.keys())[0])

    def onListViewChar(self, event):
        keyCode = event.GetKeyCode()
        if  (event.GetModifiers() == wx.MOD_NONE)   \
        and (keyCode in (wx.WXK_DOWN, wx.WXK_UP))   \
        and (self.currentIndex != None):
            self.listView.Select(self.currentIndex, on=0)
            id = +1 if keyCode == wx.WXK_DOWN else -1
            self.currentIndex = (self.currentIndex + id) % len(self.canvasList)
            self.listView.Select(self.currentIndex, on=1)
            self.listView.EnsureVisible(self.currentIndex)
        else:
            index, rc = self.listView.GetFirstSelected(), False
            if index != -1:
                keyChar, keyModifiers = event.GetKeyCode(), event.GetModifiers()
                if (keyChar, keyModifiers) == (wx.WXK_DELETE, wx.MOD_NONE):
                    self.currentIndex, rc = index, True; self.onRemove(None);
            if not rc:
                event.Skip()

    def onListViewItemSelected(self, event):
        self.currentIndex = event.GetItem().GetId()
        item = [self.listView.GetItem(self.currentIndex, col).GetText() for col in (0, 1)]
        self.drawCanvas(self.canvasList[self.currentIndex][0])

    def onListViewRightDown(self, event):
        eventPoint = event.GetPosition()
        if self.currentIndex == None:
            index, flags = self.listView.HitTest(eventPoint)
            if index != wx.NOT_FOUND:
                self.currentIndex = index
        if self.currentIndex == None:
            self.contextMenuItems[4].Enable(False)
        else:
            self.contextMenuItems[4].Enable(True)
        if len(self.canvasList) == 0:
            self.contextMenuItems[7].Enable(False)
        else:
            self.contextMenuItems[7].Enable(True)
        self.PopupMenu(self.contextMenu, eventPoint)

    def onLoad(self, event):
        def importmIRC(canvas, pathName):
            rc, error = canvas.importStore.importTextFile(pathName)
            return (rc, error, canvas.importStore.outMap, pathName, canvas.importStore.inSize)
        for rc, error, canvas, newMap, newPathName, newSize in self._importFiles(importmIRC, "mIRC art files (*.txt)|*.txt|All Files (*.*)|*.*"):
            if rc == True:
                self.currentIndex = self.listView.GetItemCount()
                self.canvasList[self.currentIndex] = [canvas, newPathName]
                self.listView.InsertItem(self.currentIndex, "")
                idx = -1
                while True:
                    idx = self.listView.GetNextSelected(idx)
                    if idx != -1:
                        self.listView.Select(idx, on=0)
                    else:
                        break
                self.listView.Select(self.currentIndex, on=1)
                self.listView.SetFocus()
                [self.listView.SetItem(self.currentIndex, col, label) for col, label in zip((0, 1), (os.path.basename(newPathName), "{}x{}".format(*newSize)))]
                [self.listView.SetColumnWidth(col, wx.LIST_AUTOSIZE) for col in (0, 1)]
            elif rc == False:
                with wx.MessageDialog(self, "Error: {}".format(error), "", wx.CANCEL | wx.OK | wx.OK_DEFAULT) as dialog:
                    dialogChoice = dialog.ShowModal()
                    if dialogChoice == wx.ID_CANCEL:
                        break

    def onLoadList(self, event):
        rc = True
        with wx.FileDialog(self, "Load from list...", os.getcwd(), "", "List files (*.lst)|*.lst|Text files (*.txt)|*.txt|All Files (*.*)|*.*", wx.FD_OPEN) as dialog:
            if self.lastDir != None:
                dialog.SetDirectory(self.lastDir)
            if dialog.ShowModal() != wx.ID_CANCEL:
                pathName = dialog.GetPath()
                self.lastDir = os.path.dirname(pathName); self._storeLastDir(self.lastDir);
                self._load_list(pathName)

    def onRemove(self, event):
        items = [self.listView.GetFirstSelected()]
        while True:
            item = self.listView.GetNextSelected(items[-1])
            if item != -1:
                items += [item]
            else:
                break
        while len(items):
            self._removeAsset(items[0]); del items[0]; items = [i - 1 for i in items];
        if self.currentIndex != None:
            self.listView.EnsureVisible(self.currentIndex)

    def onSaveList(self, event):
        rc = True
        if len(self.canvasList):
            with wx.FileDialog(self, "Save as list...", os.getcwd(), "", "List files (*.lst)|*.lst|Text files (*.txt)|*.txt|All Files (*.*)|*.*", wx.FD_SAVE) as dialog:
                if self.lastDir != None:
                    dialog.SetDirectory(self.lastDir)
                if dialog.ShowModal() != wx.ID_CANCEL:
                    pathName = dialog.GetPath()
                    self.lastDir = os.path.dirname(pathName); self._storeLastDir(self.lastDir);
                    with open(pathName, "w") as fileObject:
                        for pathName in [self.canvasList[k][1] for k in self.canvasList.keys()]:
                            print(pathName, file=fileObject)
                        rc = True
        else:
            rc, error = False, "no assets currently loaded"
        if not rc:
            with wx.MessageDialog(self, "Error: {}".format(error), "", wx.OK | wx.OK_DEFAULT) as dialog:
                dialogChoice = dialog.ShowModal()

    def __init__(self, backend, parent, pos=None, size=(400, 400), title="Assets"):
        if pos == None:
            parentRect = parent.GetScreenRect(); pos = (parentRect.x + parentRect.width, parentRect.y);
        super().__init__(parent, size, title, pos=pos)
        self.backend, self.canvasList, self.lastDir = backend((0, 0)), {}, None
        self.currentIndex, self.leftDown, self.parent, self.scrollFlag = None, False, parent, False
        self.Bind(wx.EVT_CHAR, self.onChar)
        self._loadLastDir()

        self.contextMenu, self.contextMenuItems = wx.Menu(), []
        for text, f in (
                ("&Load...", self.onLoad),
                ("Import &ANSI...", self.onImportAnsi),
                ("Import &SAUCE...", self.onImportSauce),
                ("Import from &clipboard", self.onImportFromClipboard),
                ("&Remove", self.onRemove),
                (None, None),
                ("Load from l&ist...", self.onLoadList),
                ("Sa&ve as list...", self.onSaveList),
                (None, None),
                ("Cl&ear list", self.onClearList),):
            if (text, f) == (None, None):
                self.contextMenu.AppendSeparator()
            else:
                self.contextMenuItems += [wx.MenuItem(self.contextMenu, wx.NewId(), text)]
                self.Bind(wx.EVT_MENU, f, self.contextMenuItems[-1])
                self.contextMenu.Append(self.contextMenuItems[-1])

        self.listView = wx.ListView(self, -1, size=([int(m / n) for m, n in zip(size, (2, 4))]), style=wx.BORDER_SUNKEN | wx.LC_REPORT)
        [self.listView.InsertColumn(col, heading) for col, heading in ((0, "Name"), (1, "Size"))]
        self.listView.Bind(wx.EVT_CHAR, self.onListViewChar)
        self.listView.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onListViewItemSelected)
        self.listView.Bind(wx.EVT_RIGHT_DOWN, self.onListViewRightDown)

        self.panelCanvas = GuiWindow(self, (0, 0), wx.BORDER_SUNKEN)
        self.panelCanvas.Bind(wx.EVT_CHAR, self.onChar)
        self.panelCanvas.Bind(wx.EVT_LEFT_DOWN, self.onPanelLeftDown)
        self.panelCanvas.Bind(wx.EVT_PAINT, self.onPanelPaint)
        self.panelCanvas.Bind(wx.EVT_SIZE, self.onPanelSize)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.AddMany(((self.listView, 0, wx.ALL | wx.EXPAND, 4), (self.panelCanvas, 1, wx.ALL | wx.EXPAND, 4),))
        self.panelCanvas.SetMinSize((int(size[0] / 2), int(size[1] / 2)))
        self.SetSizerAndFit(self.sizer)
        self._updateScrollBars()
        self.Show(True)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
