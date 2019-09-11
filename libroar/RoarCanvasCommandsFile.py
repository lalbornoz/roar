#!/usr/bin/env python3
#
# RoarCanvasCommandsFile.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

try:
    from ImgurApiKey import ImgurApiKey
    haveImgurApiKey = True
except ImportError:
    haveImgurApiKey = False

try:
    import base64, json, requests, urllib.request
    haveUrllib = True
except ImportError:
    haveUrllib = False

from GuiFrame import GuiCommandDecorator, NID_MENU_SEP
import io, os, wx

class RoarCanvasCommandsFile():
    # {{{ _import(self, f, newDirty, pathName)
    def _import(self, f, newDirty, pathName):
        rc = False
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        try:
            rc, error, newMap, newPathName, newSize = f(pathName)
            if rc:
                self.parentCanvas.dirty = newDirty
                self.parentCanvas.update(newSize, False, newMap)
                self.canvasPathName = newPathName
                self.update(dirty=self.parentCanvas.dirty, pathName=self.canvasPathName, undoLevel=-1)
                self.parentCanvas.canvas.journal.resetCursor()
                self.parentCanvas.canvas.journal.resetUndo()
        except FileNotFoundError as e:
            rc, error, newMap, newPathName, newSize = False, str(e), None, None, None
        if not rc:
            with wx.MessageDialog(self.parentCanvas, "Error: {}".format(error), "", wx.OK | wx.OK_DEFAULT) as dialog:
                dialogChoice = dialog.ShowModal()
        self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
        return rc
    # }}}
    # {{{ _importFile(self, f, newDirty, wildcard)
    def _importFile(self, f, newDirty, wildcard):
        with wx.FileDialog(self.parentCanvas, "Open", os.getcwd(), "", wildcard, wx.FD_OPEN) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            elif self._promptSaveChanges():
                return self._import(f, newDirty, dialog.GetPath())
    # }}}
    # {{{ _promptSaveChanges(self)
    def _promptSaveChanges(self):
        if self.parentCanvas.dirty:
            message = "Do you want to save changes to {}?".format(self.canvasPathName if self.canvasPathName != None else "(Untitled)")
            with wx.MessageDialog(self.parentCanvas, message, "", wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_QUESTION | wx.YES_NO) as dialog:
                dialogChoice = dialog.ShowModal()
                if dialogChoice == wx.ID_CANCEL:
                    return False
                elif dialogChoice == wx.ID_NO:
                    return True
                elif dialogChoice == wx.ID_YES:
                    return self.canvasSaveAs(None) if self.canvasPathName == None else self.canvasSave(None)
                else:
                    return False
        else:
            return True
    # }}}

    # {{{ canvasExit(self, event)
    @GuiCommandDecorator("Exit", "E&xit", None, [wx.ACCEL_CTRL, ord("X")], None)
    def canvasExit(self, event):
        if self._promptSaveChanges():
            self.parentFrame.Close(True)
    # }}}
    # {{{ canvasExportAsAnsi(self, event)
    @GuiCommandDecorator("Export as ANSI...", "Export as ANSI...", None, None, None)
    def canvasExportAsAnsi(self, event):
        with wx.FileDialog(self.parentFrame, "Save As...", os.getcwd(), "", "ANSI files (*.ans;*.txt)|*.ans;*.txt|All Files (*.*)|*.*", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                outPathName = dialog.GetPath()
                self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                with open(outPathName, "w", encoding="utf-8") as outFile:
                    self.parentCanvas.canvas.exportStore.exportAnsiFile(self.parentCanvas.canvas.map, self.parentCanvas.canvas.size, outFile)
                self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
                return True
    # }}}
    # {{{ canvasExportAsPng(self, event)
    @GuiCommandDecorator("Export as PNG...", "Export as PN&G...", None, None, None)
    def canvasExportAsPng(self, event):
        with wx.FileDialog(self.parentFrame, "Save As...", os.getcwd(), "", "PNG (*.png)|*.png|All Files (*.*)|*.*", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                outPathName = dialog.GetPath()
                self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                self.parentCanvas.canvas.exportStore.exportBitmapToPngFile(self.parentCanvas.backend.canvasBitmap, outPathName, wx.BITMAP_TYPE_PNG)
                self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
                return True
    # }}}
    # {{{ canvasExportImgur(self, event)
    @GuiCommandDecorator("Export to Imgur...", "Export to I&mgur...", None, None, haveImgurApiKey and haveUrllib)
    def canvasExportImgur(self, event):
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        rc, status, result = self.parentCanvas.canvas.exportStore.exportBitmapToImgur(self.imgurApiKey, self.parentCanvas.backend.canvasBitmap, "", "", wx.BITMAP_TYPE_PNG)
        self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
        if rc:
            if not wx.TheClipboard.IsOpened():
                wx.TheClipboard.Open(); wx.TheClipboard.SetData(wx.TextDataObject(result)); wx.TheClipboard.Close();
            wx.MessageBox("Exported to Imgur: {}".format(result), "Export to Imgur", wx.ICON_INFORMATION | wx.OK)
        else:
            wx.MessageBox("Failed to export to Imgur: {}".format(result), "Export to Imgur", wx.ICON_EXCLAMATION | wx.OK)
    # }}}
    # {{{ canvasExportPastebin(self, event)
    @GuiCommandDecorator("Export to Pastebin...", "Export to Pasteb&in...", None, None, haveUrllib)
    def canvasExportPastebin(self, event):
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        pasteStatus, pasteResult = self.parentCanvas.canvas.exportStore.exportPastebin("253ce2f0a45140ee0a44ca99aa49260", self.parentCanvas.canvas.map, self.parentCanvas.canvas.size)
        self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
        if pasteStatus:
            if not wx.TheClipboard.IsOpened():
                wx.TheClipboard.Open()
                wx.TheClipboard.SetData(wx.TextDataObject(pasteResult))
                wx.TheClipboard.Close()
            wx.MessageBox("Exported to Pastebin: " + pasteResult, "Export to Pastebin", wx.OK|wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Failed to export to Pastebin: " + pasteResult, "Export to Pastebin", wx.OK|wx.ICON_EXCLAMATION)
    # }}}
    # {{{ canvasExportToClipboard(self, event)
    @GuiCommandDecorator("Export to clipboard", "&Export to clipboard", None, None, None)
    def canvasExportToClipboard(self, event):
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        rc, outBuffer = self.parentCanvas.canvas.exportStore.exportTextBuffer(self.parentCanvas.canvas.map, self.parentCanvas.canvas.size)
        if rc and wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(outBuffer))
            wx.TheClipboard.Close()
        self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
        return True
    # }}}
    # {{{ canvasImportAnsi(self, event)
    @GuiCommandDecorator("Import ANSI...", "Import ANSI...", None, None, None)
    def canvasImportAnsi(self, event):
        def canvasImportAnsi_(pathName):
            rc, error = self.parentCanvas.canvas.importStore.importAnsiFile(pathName)
            return (rc, error, self.parentCanvas.canvas.importStore.outMap, pathName, self.parentCanvas.canvas.importStore.inSize)
        self._importFile(canvasImportAnsi_, True, "ANSI files (*.ans;*.txt)|*.ans;*.txt|All Files (*.*)|*.*")
    # }}}
    # {{{ canvasImportFromClipboard(self, event)
    @GuiCommandDecorator("Import from clipboard", "&Import from clipboard", None, None, None)
    def canvasImportFromClipboard(self, event):
        def canvasImportFromClipboard_(pathName):
            if  wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT))  \
            and wx.TheClipboard.Open():
                inBuffer = wx.TextDataObject()
                if wx.TheClipboard.GetData(inBuffer):
                    if self._promptSaveChanges():
                        rc, error = self.parentCanvas.canvas.importStore.importTextBuffer(io.StringIO(inBuffer.GetText()))
                wx.TheClipboard.Close()
            else:
                rc, error = False, "Clipboard does not contain text data and/or cannot be opened"
            return (rc, error, self.parentCanvas.canvas.importStore.outMap, None, self.parentCanvas.canvas.importStore.inSize)
        if self._promptSaveChanges():
            self._import(canvasImportFromClipboard_, True, None)
    # }}}
    # {{{ canvasImportSauce(self, event)
    @GuiCommandDecorator("Import SAUCE...", "Import SAUCE...", None, None, None)
    def canvasImportSauce(self, event):
        def canvasImportSauce_(pathName):
            rc, error = self.parentCanvas.canvas.importStore.importSauceFile(pathName)
            return (rc, error, self.parentCanvas.canvas.importStore.outMap, pathName, self.parentCanvas.canvas.importStore.inSize)
        self._importFile(canvasImportSauce_, True, "SAUCE files (*.ans;*.txt)|*.ans;*.txt|All Files (*.*)|*.*")
    # }}}
    # {{{ canvasNew(self, event, newCanvasSize=None)
    @GuiCommandDecorator("New", "&New", ["", wx.ART_NEW], [wx.ACCEL_CTRL, ord("N")], None)
    def canvasNew(self, event, newCanvasSize=None):
        def canvasImportEmpty(pathName):
            nonlocal newCanvasSize
            if newCanvasSize == None:
                newCanvasSize = list(self.parentCanvas.canvas.size)
            newMap = [[[1, 1, 0, " "] for x in range(newCanvasSize[0])] for y in range(newCanvasSize[1])]
            return (True, "", newMap, None, newCanvasSize)
        if self._promptSaveChanges():
            self._import(canvasImportEmpty, False, None)
    # }}}
    # {{{ canvasOpen(self, event)
    @GuiCommandDecorator("Open", "&Open", ["", wx.ART_FILE_OPEN], [wx.ACCEL_CTRL, ord("O")], None)
    def canvasOpen(self, event):
        def canvasImportmIRC(pathName):
            rc, error = self.parentCanvas.canvas.importStore.importTextFile(pathName)
            return (rc, error, self.parentCanvas.canvas.importStore.outMap, pathName, self.parentCanvas.canvas.importStore.inSize)
        self._importFile(canvasImportmIRC, False, "mIRC art files (*.txt)|*.txt|All Files (*.*)|*.*")
    # }}}
    # {{{ canvasSave(self, event)
    @GuiCommandDecorator("Save", "&Save", ["", wx.ART_FILE_SAVE], [wx.ACCEL_CTRL, ord("S")], None)
    def canvasSave(self, event):
        if self.canvasPathName == None:
            if self.canvasSaveAs(event) == False:
                return False
        try:
            with open(self.canvasPathName, "w", encoding="utf-8") as outFile:
                self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                self.parentCanvas.canvas.exportStore.exportTextFile(self.parentCanvas.canvas.map, self.parentCanvas.canvas.size, outFile)
                self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
                self.parentCanvas.dirty = False
                self.update(dirty=self.parentCanvas.dirty)
            return True
        except IOError as error:
            return False
    # }}}
    # {{{ canvasSaveAs(self, event)
    @GuiCommandDecorator("Save As...", "Save &As...", ["", wx.ART_FILE_SAVE_AS], None, None)
    def canvasSaveAs(self, event):
        with wx.FileDialog(self.parentCanvas, "Save As", os.getcwd(), "", "mIRC art files (*.txt)|*.txt|All Files (*.*)|*.*", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                self.canvasPathName = dialog.GetPath()
                return self.canvasSave(event)
    # }}}

    #
    # __init__(self)
    def __init__(self):
        self.imgurApiKey = ImgurApiKey.imgurApiKey if haveImgurApiKey else None
        self.menus = (
            ("&File",
                self.canvasNew, self.canvasOpen, self.canvasSave, self.canvasSaveAs, NID_MENU_SEP,
                self.canvasExportAsAnsi, self.canvasExportToClipboard, self.canvasExportImgur, self.canvasExportPastebin, self.canvasExportAsPng, NID_MENU_SEP,
                self.canvasImportAnsi, self.canvasImportFromClipboard, self.canvasImportSauce, NID_MENU_SEP,
                self.canvasExit,
            ),
        )
        self.toolBars = ()

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
