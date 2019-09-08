#!/usr/bin/env python3
#
# GuiCanvasInterface.py 
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

try:
    import base64, json, requests, urllib.request
    haveUrllib = True
except ImportError:
    haveUrllib = False

from ToolCircle import ToolCircle
from ToolFill import ToolFill
from ToolLine import ToolLine
from ToolRect import ToolRect
from ToolSelectClone import ToolSelectClone
from ToolSelectMove import ToolSelectMove
from ToolText import ToolText

from GuiCanvasColours import Colours
from GuiCanvasInterfaceAbout import GuiCanvasInterfaceAbout
from GuiFrame import NID_MENU_SEP, NID_TOOLBAR_HSEP
from ImgurApiKey import ImgurApiKey
import io, os, sys, wx

def GuiCanvasCommandDecorator(caption, label, icon, accel, initialState):
    # {{{ GuiCanvasCommandDecoratorOuter(targetObject)
    def GuiCanvasCommandDecoratorOuter(targetObject):
        if callable(targetObject):
            if not hasattr(targetObject, "attrDict"):
                setattr(targetObject, "attrDict", [])
            targetObject.attrDict = {"caption": caption, "label": label, "icon": icon, "accel": accel, "initialState": initialState, "id": None}
            return targetObject
    return GuiCanvasCommandDecoratorOuter
    # }}}

def GuiCanvasSelectDecorator(idx, caption, label, icon, accel, initialState):
    # {{{ GuiCanvasSelectDecoratorOuter(targetObject)
    def GuiCanvasSelectDecoratorOuter(targetObject):
        if callable(targetObject):
            if not hasattr(targetObject, "attrList"):
                setattr(targetObject, "attrList", [])
            setattr(targetObject, "isSelect", True)
            targetObject.attrList.insert(0, {"caption": caption, "label": label, "icon": icon, "accel": accel, "initialState": initialState, "id": None, "idx": idx})
            return targetObject
    return GuiCanvasSelectDecoratorOuter
    # }}}

class GuiCanvasInterface():
    # {{{ _import(self, f, newDirty, pathName)
    def _import(self, f, newDirty, pathName):
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        rc, error, newMap, newPathName, newSize = f(pathName)
        if rc:
            self.parentCanvas.dirty = newDirty
            self.parentCanvas.update(newSize, False, newMap)
            self.canvasPathName = newPathName
            self.update(dirty=self.parentCanvas.dirty, pathName=self.canvasPathName, undoLevel=-1)
        else:
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
    # {{{ _initColourBitmaps(self)
    def _initColourBitmaps(self):
        for numColour in range(len(self.canvasColour.attrList)):
            if numColour < len(Colours):
                toolBitmapColour = Colours[numColour][0:4]
                toolBitmap = wx.Bitmap((16, 16))
                toolBitmapDc = wx.MemoryDC(); toolBitmapDc.SelectObject(toolBitmap);
                toolBitmapBrush = wx.Brush(wx.Colour(toolBitmapColour), wx.BRUSHSTYLE_SOLID)
                toolBitmapDc.SetBrush(toolBitmapBrush)
                toolBitmapDc.SetBackground(toolBitmapBrush)
                toolBitmapDc.SetPen(wx.Pen(wx.Colour(toolBitmapColour), 1))
                toolBitmapDc.DrawRectangle(0, 0, 16, 16)
            self.canvasColour.attrList[numColour]["icon"] = ["", None, toolBitmap]
        toolBitmapColours = ((0, 0, 0, 255), (255, 255, 255, 255))
        toolBitmap = wx.Bitmap((16, 16))
        toolBitmapDc = wx.MemoryDC(); toolBitmapDc.SelectObject(toolBitmap);
        toolBitmapBrush = [wx.Brush(wx.Colour(c), wx.BRUSHSTYLE_SOLID) for c in toolBitmapColours]
        toolBitmapDc.SetBrush(toolBitmapBrush[1])
        toolBitmapDc.SetBackground(toolBitmapBrush[1])
        toolBitmapDc.SetPen(wx.Pen(wx.Colour(toolBitmapColours[1]), 1))
        toolBitmapDc.DrawRectangle(0, 0, 8, 8)
        toolBitmapDc.DrawRectangle(8, 8, 16, 16)
        self.canvasColourAlpha.attrList[0]["icon"] = ["", None, toolBitmap]
    # }}}
    # {{{ _promptSaveChanges(self)
    def _promptSaveChanges(self):
        if self.parentCanvas.dirty:
           with wx.MessageDialog(self.parentCanvas,                                                                                    \
                        "Do you want to save changes to {}?".format(self.canvasPathName if self.canvasPathName != None else "(Untitled)"),  \
                        "", wx.CANCEL|wx.CANCEL_DEFAULT|wx.ICON_QUESTION|wx.YES_NO) as dialog:
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

    # {{{ canvasAbout(self, event)
    @GuiCanvasCommandDecorator("About", "&About", None, None, True)
    def canvasAbout(self, event):
        GuiCanvasInterfaceAbout(self.parentFrame)
    # }}}
    # {{{ canvasBrush(self, f, idx)
    @GuiCanvasSelectDecorator(0, "Solid brush", "Solid brush", None, None, True)
    def canvasBrush(self, f, idx):
        def canvasBrush_(self, event):
            pass
        setattr(canvasBrush_, "attrDict", f.attrList[idx])
        setattr(canvasBrush_, "isSelect", True)
        return canvasBrush_
    # }}}
    # {{{ canvasColour(self, f, idx)
    @GuiCanvasSelectDecorator(0, "Colour #00", "Colour #00 (Bright White)", None, None, False)
    @GuiCanvasSelectDecorator(1, "Colour #01", "Colour #01 (Black)", None, None, False)
    @GuiCanvasSelectDecorator(2, "Colour #02", "Colour #02 (Blue)", None, None, False)
    @GuiCanvasSelectDecorator(3, "Colour #03", "Colour #03 (Green)", None, None, False)
    @GuiCanvasSelectDecorator(4, "Colour #04", "Colour #04 (Red)", None, None, False)
    @GuiCanvasSelectDecorator(5, "Colour #05", "Colour #05 (Light Red)", None, None, False)
    @GuiCanvasSelectDecorator(6, "Colour #06", "Colour #06 (Pink)", None, None, False)
    @GuiCanvasSelectDecorator(7, "Colour #07", "Colour #07 (Yellow)", None, None, False)
    @GuiCanvasSelectDecorator(8, "Colour #08", "Colour #08 (Light Yellow)", None, None, False)
    @GuiCanvasSelectDecorator(9, "Colour #09", "Colour #09 (Light Green)", None, None, False)
    @GuiCanvasSelectDecorator(10, "Colour #10", "Colour #10 (Cyan)", None, None, False)
    @GuiCanvasSelectDecorator(11, "Colour #11", "Colour #11 (Light Cyan)", None, None, False)
    @GuiCanvasSelectDecorator(12, "Colour #12", "Colour #12 (Light Blue)", None, None, False)
    @GuiCanvasSelectDecorator(13, "Colour #13", "Colour #13 (Light Pink)", None, None, False)
    @GuiCanvasSelectDecorator(14, "Colour #14", "Colour #14 (Grey)", None, None, False)
    @GuiCanvasSelectDecorator(15, "Colour #15", "Colour #15 (Light Grey)", None, None, False)
    def canvasColour(self, f, idx):
        def canvasColour_(self, event):
            if event.GetEventType() == wx.wxEVT_TOOL:
                self.parentCanvas.brushColours[0] = idx
            elif event.GetEventType() == wx.wxEVT_TOOL_RCLICKED:
                self.parentCanvas.brushColours[1] = idx
            self.update(colours=self.parentCanvas.brushColours)
        setattr(canvasColour_, "attrDict", f.attrList[idx])
        setattr(canvasColour_, "isSelect", True)
        return canvasColour_
    # }}}
    # {{{ canvasColourAlpha(self, f, idx)
    @GuiCanvasSelectDecorator(0, "Transparent colour", "Transparent colour", None, None, False)
    def canvasColourAlpha(self, f, idx):
        def canvasColourAlpha_(self, event):
            if event.GetEventType() == wx.wxEVT_TOOL:
                self.parentCanvas.brushColours[0] = -1
            elif event.GetEventType() == wx.wxEVT_TOOL_RCLICKED:
                self.parentCanvas.brushColours[1] = -1
            self.update(colours=self.parentCanvas.brushColours)
        setattr(canvasColourAlpha_, "attrDict", f.attrList[idx])
        setattr(canvasColourAlpha_, "isSelect", True)
        return canvasColourAlpha_
    # }}}
    # {{{ canvasCopy(self, event)
    @GuiCanvasCommandDecorator("Copy", "&Copy", ["", wx.ART_COPY], None, False)
    def canvasCopy(self, event):
        pass
    # }}}
    # {{{ canvasCut(self, event)
    @GuiCanvasCommandDecorator("Cut", "Cu&t", ["", wx.ART_CUT], None, False)
    def canvasCut(self, event):
        pass
    # }}}
    # {{{ canvasDelete(self, event)
    @GuiCanvasCommandDecorator("Delete", "De&lete", ["", wx.ART_DELETE], None, False)
    def canvasDelete(self, event):
        pass
    # }}}
    # {{{ canvasExit(self, event)
    @GuiCanvasCommandDecorator("Exit", "E&xit", None, [wx.ACCEL_CTRL, ord("X")], None)
    def canvasExit(self, event):
        if self._promptSaveChanges():
            self.parentFrame.Close(True)
    # }}}
    # {{{ canvasNew(self, event, newCanvasSize=None)
    @GuiCanvasCommandDecorator("New", "&New", ["", wx.ART_NEW], [wx.ACCEL_CTRL, ord("N")], None)
    def canvasNew(self, event, newCanvasSize=None):
        def canvasImportEmpty(pathName):
            nonlocal newCanvasSize
            if newCanvasSize == None:
                newCanvasSize = list(self.parentCanvas.defaultCanvasSize)
            newMap = [[[1, 1, 0, " "] for x in range(newCanvasSize[0])] for y in range(newCanvasSize[1])]
            return (True, "", newMap, None, newCanvasSize)
        if self._promptSaveChanges():
            self._import(canvasImportEmpty, False, None)
    # }}}
    # {{{ canvasOpen(self, event)
    @GuiCanvasCommandDecorator("Open", "&Open", ["", wx.ART_FILE_OPEN], [wx.ACCEL_CTRL, ord("O")], None)
    def canvasOpen(self, event):
        def canvasImportmIRC(pathName):
            rc, error = self.parentCanvas.canvas.importStore.importTextFile(pathName)
            return (rc, error, self.parentCanvas.canvas.importStore.outMap, pathName, self.parentCanvas.canvas.importStore.inSize)
        self._importFile(canvasImportmIRC, False, "mIRC art files (*.txt)|*.txt|All Files (*.*)|*.*")
    # }}}
    # {{{ canvasPaste(self, event)
    @GuiCanvasCommandDecorator("Paste", "&Paste", ["", wx.ART_PASTE], None, False)
    def canvasPaste(self, event):
        pass
    # }}}
    # {{{ canvasRedo(self, event)
    @GuiCanvasCommandDecorator("Redo", "&Redo", ["", wx.ART_REDO], [wx.ACCEL_CTRL, ord("Y")], False)
    def canvasRedo(self, event):
        self.parentCanvas.dispatchDeltaPatches(self.parentCanvas.canvas.journal.popRedo())
        self.update(size=self.parentCanvas.canvas.size, undoLevel=self.parentCanvas.canvas.journal.patchesUndoLevel)
    # }}}
    # {{{ canvasSave(self, event)
    @GuiCanvasCommandDecorator("Save", "&Save", ["", wx.ART_FILE_SAVE], [wx.ACCEL_CTRL, ord("S")], None)
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
    @GuiCanvasCommandDecorator("Save As...", "Save &As...", ["", wx.ART_FILE_SAVE_AS], None, None)
    def canvasSaveAs(self, event):
        with wx.FileDialog(self.parentCanvas, "Save As", os.getcwd(), "", "mIRC art files (*.txt)|*.txt|All Files (*.*)|*.*", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                self.canvasPathName = dialog.GetPath()
                return self.canvasSave(event)
    # }}}
    # {{{ canvasUndo(self, event)
    @GuiCanvasCommandDecorator("Undo", "&Undo", ["", wx.ART_UNDO], [wx.ACCEL_CTRL, ord("Z")], False)
    def canvasUndo(self, event):
        self.parentCanvas.dispatchDeltaPatches(self.parentCanvas.canvas.journal.popUndo())
        self.update(size=self.parentCanvas.canvas.size, undoLevel=self.parentCanvas.canvas.journal.patchesUndoLevel)
    # }}}

    # {{{ canvasDecrBrushHeight(self, event)
    @GuiCanvasCommandDecorator("Decrease brush height", "Decrease brush height", ["toolDecrBrushH.png"], None, None)
    def canvasDecrBrushHeight(self, event):
        if  self.parentCanvas.brushSize[1] > 1:
            self.parentCanvas.brushSize[1] -= 1
            self.update(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasDecrBrushHeightWidth(self, event)
    @GuiCanvasCommandDecorator("Decrease brush size", "Decrease brush size", ["toolDecrBrushHW.png"], None, None)
    def canvasDecrBrushHeightWidth(self, event):
        self.canvasDecrBrushHeight(event)
        self.canvasDecrBrushWidth(event)
    # }}}
    # {{{ canvasDecrBrushWidth(self, event)
    @GuiCanvasCommandDecorator("Decrease brush width", "Decrease brush width", ["toolDecrBrushW.png"], None, None)
    def canvasDecrBrushWidth(self, event):
        if  self.parentCanvas.brushSize[0] > 1:
            self.parentCanvas.brushSize[0] -= 1
            self.update(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasDecrCanvasHeight(self, event)
    @GuiCanvasCommandDecorator("Decrease canvas height", "Decrease canvas height", ["toolDecrCanvasH.png"], None, None)
    def canvasDecrCanvasHeight(self, event):
        if self.parentCanvas.canvas.size[1] > 1:
            self.parentCanvas.resize([self.parentCanvas.canvas.size[0], self.parentCanvas.canvas.size[1] - 1])
    # }}}
    # {{{ canvasDecrCanvasHeightWidth(self, event)
    @GuiCanvasCommandDecorator("Decrease canvas size", "Decrease canvas size", ["toolDecrCanvasHW.png"], None, None)
    def canvasDecrCanvasHeightWidth(self, event):
        self.canvasDecrCanvasHeight(event)
        self.canvasDecrCanvasWidth(event)
    # }}}
    # {{{ canvasDecrCanvasWidth(self, event)
    @GuiCanvasCommandDecorator("Decrease canvas width", "Decrease canvas width", ["toolDecrCanvasW.png"], None, None)
    def canvasDecrCanvasWidth(self, event):
        if self.parentCanvas.canvas.size[0] > 1:
            self.parentCanvas.resize([self.parentCanvas.canvas.size[0] - 1, self.parentCanvas.canvas.size[1]])
    # }}}
    # {{{ canvasIncrBrushHeight(self, event)
    @GuiCanvasCommandDecorator("Increase brush height", "Increase brush height", ["toolIncrBrushH.png"], None, None)
    def canvasIncrBrushHeight(self, event):
        self.parentCanvas.brushSize[1] += 1
        self.update(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasIncrBrushHeightWidth(self, event)
    @GuiCanvasCommandDecorator("Increase brush size", "Increase brush size", ["toolIncrBrushHW.png"], None, None)
    def canvasIncrBrushHeightWidth(self, event):
        self.canvasIncrBrushHeight(event)
        self.canvasIncrBrushWidth(event)
    # }}}
    # {{{ canvasIncrBrushWidth(self, event)
    @GuiCanvasCommandDecorator("Increase brush width", "Increase brush width", ["toolIncrBrushW.png"], None, None)
    def canvasIncrBrushWidth(self, event):
        self.parentCanvas.brushSize[0] += 1
        self.update(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasIncrCanvasHeight(self, event)
    @GuiCanvasCommandDecorator("Increase canvas height", "Increase canvas height", ["toolIncrCanvasH.png"], None, None)
    def canvasIncrCanvasHeight(self, event):
        self.parentCanvas.resize([self.parentCanvas.canvas.size[0], self.parentCanvas.canvas.size[1] + 1])
    # }}}
    # {{{ canvasIncrCanvasHeightWidth(self, event)
    @GuiCanvasCommandDecorator("Increase canvas size", "Increase canvas size", ["toolIncrCanvasHW.png"], None, None)
    def canvasIncrCanvasHeightWidth(self, event):
        self.canvasIncrCanvasHeight(event)
        self.canvasIncrCanvasWidth(event)
    # }}}
    # {{{ canvasIncrCanvasWidth(self, event)
    @GuiCanvasCommandDecorator("Increase canvas width", "Increase canvas width", ["toolIncrCanvasW.png"], None, None)
    def canvasIncrCanvasWidth(self, event):
        self.parentCanvas.resize([self.parentCanvas.canvas.size[0] + 1, self.parentCanvas.canvas.size[1]])
    # }}}
    # {{{ canvasTool(self, f, idx)
    @GuiCanvasSelectDecorator(0, "Circle", "&Circle", ["toolCircle.png"], [wx.ACCEL_CTRL, ord("C")], False)
    @GuiCanvasSelectDecorator(1, "Clone", "Cl&one", ["toolClone.png"], [wx.ACCEL_CTRL, ord("E")], False)
    @GuiCanvasSelectDecorator(2, "Fill", "&Fill", ["toolFill.png"], [wx.ACCEL_CTRL, ord("F")], False)
    @GuiCanvasSelectDecorator(3, "Line", "&Line", ["toolLine.png"], [wx.ACCEL_CTRL, ord("L")], False)
    @GuiCanvasSelectDecorator(4, "Move", "&Move", ["toolMove.png"], [wx.ACCEL_CTRL, ord("M")], False)
    @GuiCanvasSelectDecorator(5, "Rectangle", "&Rectangle", ["toolRect.png"], [wx.ACCEL_CTRL, ord("R")], True)
    @GuiCanvasSelectDecorator(6, "Text", "&Text", ["toolText.png"], [wx.ACCEL_CTRL, ord("T")], False)
    def canvasTool(self, f, idx):
        def canvasTool_(self, event):
            self.currentTool = [ToolCircle, ToolSelectClone, ToolFill, ToolLine, ToolSelectMove, ToolRect, ToolText][idx](self.parentCanvas)
            self.parentFrame.menuItemsById[self.canvasTool.attrList[idx]["id"]].Check(True)
            toolBar = self.parentFrame.toolBarItemsById[self.canvasTool.attrList[idx]["id"]].GetToolBar()
            toolBar.ToggleTool(self.canvasTool.attrList[idx]["id"], True)
            self.update(toolName=self.currentTool.name)
        setattr(canvasTool_, "attrDict", f.attrList[idx])
        setattr(canvasTool_, "isSelect", True)
        return canvasTool_
    # }}}

    # {{{ canvasExportAsAnsi(self, event)
    @GuiCanvasCommandDecorator("Export as ANSI...", "Export as ANSI...", None, None, None)
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
    @GuiCanvasCommandDecorator("Export as PNG...", "Export as PN&G...", None, None, None)
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
    @GuiCanvasCommandDecorator("Export to Imgur...", "Export to I&mgur...", None, None, haveUrllib)
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
    @GuiCanvasCommandDecorator("Export to Pastebin...", "Export to Pasteb&in...", None, None, haveUrllib)
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
    @GuiCanvasCommandDecorator("Export to clipboard", "&Export to clipboard", None, None, None)
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
    @GuiCanvasCommandDecorator("Import ANSI...", "Import ANSI...", None, None, None)
    def canvasImportAnsi(self, event):
        def canvasImportAnsi_(pathName):
            rc, error = self.parentCanvas.canvas.importStore.importAnsiFile(pathName)
            return (rc, error, self.parentCanvas.canvas.importStore.outMap, pathName, self.parentCanvas.canvas.importStore.inSize)
        self._importFile(canvasImportAnsi_, True, "ANSI files (*.ans;*.txt)|*.ans;*.txt|All Files (*.*)|*.*")
    # }}}
    # {{{ canvasImportFromClipboard(self, event)
    @GuiCanvasCommandDecorator("Import from clipboard", "&Import from clipboard", None, None, None)
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
    @GuiCanvasCommandDecorator("Import SAUCE...", "Import SAUCE...", None, None, None)
    def canvasImportSauce(self, event):
        def canvasImportSauce_(pathName):
            rc, error = self.parentCanvas.canvas.importStore.importSauceFile(pathName)
            return (rc, error, self.parentCanvas.canvas.importStore.outMap, pathName, self.parentCanvas.canvas.importStore.inSize)
        self._importFile(canvasImportSauce_, True, "SAUCE files (*.ans;*.txt)|*.ans;*.txt|All Files (*.*)|*.*")
    # }}}

    # {{{ update(self, **kwargs)
    def update(self, **kwargs):
        self.lastPanelState.update(kwargs); textItems = [];
        if "cellPos" in self.lastPanelState:
            textItems.append("X: {:03d} Y: {:03d}".format(*self.lastPanelState["cellPos"]))
        if "size" in self.lastPanelState:
            textItems.append("W: {:03d} H: {:03d}".format(*self.lastPanelState["size"]))
        if "brushSize" in self.lastPanelState:
            textItems.append("Brush: {:02d}x{:02d}".format(*self.lastPanelState["brushSize"]))
        if "colours" in self.lastPanelState:
            textItems.append("FG: {:02d}, BG: {:02d}".format(*self.lastPanelState["colours"]))
            textItems.append("{} on {}".format(
                Colours[self.lastPanelState["colours"][0]][4] if self.lastPanelState["colours"][0] != -1 else "Transparent",
                Colours[self.lastPanelState["colours"][1]][4] if self.lastPanelState["colours"][1] != -1 else "Transparent"))
        if "pathName" in self.lastPanelState:
            if self.lastPanelState["pathName"] != None:
                basePathName = os.path.basename(self.lastPanelState["pathName"])
                textItems.append("Current file: {}".format(basePathName))
                self.parentFrame.SetTitle("{} - roar".format(basePathName))
            else:
                self.parentFrame.SetTitle("roar")
        if "toolName" in self.lastPanelState:
            textItems.append("Current tool: {}".format(self.lastPanelState["toolName"]))
        if  "dirty" in self.lastPanelState  \
        and self.lastPanelState["dirty"]:
            textItems.append("*")
        self.parentFrame.statusBar.SetStatusText(" | ".join(textItems))
        if "undoLevel" in self.lastPanelState:
            if self.lastPanelState["undoLevel"] >= 0:
                self.parentFrame.menuItemsById[self.canvasUndo.attrDict["id"]].Enable(True)
                toolBar = self.parentFrame.toolBarItemsById[self.canvasUndo.attrDict["id"]].GetToolBar()
                toolBar.EnableTool(self.canvasUndo.attrDict["id"], True)
            else:
                self.parentFrame.menuItemsById[self.canvasUndo.attrDict["id"]].Enable(False)
                toolBar = self.parentFrame.toolBarItemsById[self.canvasUndo.attrDict["id"]].GetToolBar()
                toolBar.EnableTool(self.canvasUndo.attrDict["id"], False)
            if self.lastPanelState["undoLevel"] > 0:
                self.parentFrame.menuItemsById[self.canvasRedo.attrDict["id"]].Enable(True)
                toolBar = self.parentFrame.toolBarItemsById[self.canvasRedo.attrDict["id"]].GetToolBar()
                toolBar.EnableTool(self.canvasRedo.attrDict["id"], True)
            else:
                self.parentFrame.menuItemsById[self.canvasRedo.attrDict["id"]].Enable(False)
                toolBar = self.parentFrame.toolBarItemsById[self.canvasRedo.attrDict["id"]].GetToolBar()
                toolBar.EnableTool(self.canvasRedo.attrDict["id"], False)
    # }}}

    # {{{ accels
    accels = (
        canvasNew, canvasOpen, canvasSave, canvasExit, canvasUndo, canvasRedo,
        canvasTool(None, canvasTool, 5), canvasTool(None, canvasTool, 0), canvasTool(None, canvasTool, 2), canvasTool(None, canvasTool, 3), canvasTool(None, canvasTool, 6), canvasTool(None, canvasTool, 1), canvasTool(None, canvasTool, 4),
    )
    # }}}
    # {{{ menus
    menus = (
        ("&File",
            canvasNew, canvasOpen, canvasSave, canvasSaveAs, NID_MENU_SEP,
            canvasExportAsAnsi, canvasExportToClipboard, canvasExportImgur, canvasExportPastebin, canvasExportAsPng, NID_MENU_SEP,
            canvasImportAnsi, canvasImportFromClipboard, canvasImportSauce, NID_MENU_SEP,
            canvasExit,
        ),
        ("&Edit",
            canvasUndo, canvasRedo, NID_MENU_SEP,
            canvasCut, canvasCopy, canvasPaste,
            canvasDelete, NID_MENU_SEP,
            canvasIncrCanvasWidth, canvasDecrCanvasWidth, canvasIncrCanvasHeight, canvasDecrCanvasHeight, NID_MENU_SEP,
            canvasIncrCanvasHeightWidth, canvasDecrBrushHeightWidth, NID_MENU_SEP,
            canvasIncrBrushWidth, canvasDecrBrushWidth, canvasIncrBrushHeight, canvasDecrBrushHeight, NID_MENU_SEP,
            canvasIncrBrushHeightWidth, canvasDecrBrushHeightWidth, NID_MENU_SEP,
            canvasBrush(None, canvasBrush, 0),
        ),
        ("&Tools",
            canvasTool(None, canvasTool, 5), canvasTool(None, canvasTool, 0), canvasTool(None, canvasTool, 2), canvasTool(None, canvasTool, 3), canvasTool(None, canvasTool, 6), canvasTool(None, canvasTool, 1), canvasTool(None, canvasTool, 4),),
        ("&Help",
            canvasAbout,),
    )
    # }}}
    # {{{ toolBars
    toolBars = (
        (canvasNew, canvasOpen, canvasSave, canvasSaveAs, NID_TOOLBAR_HSEP,
         canvasUndo, canvasRedo, NID_TOOLBAR_HSEP,
         canvasCut, canvasCopy, canvasPaste, canvasDelete, NID_TOOLBAR_HSEP,
         canvasIncrCanvasWidth, canvasDecrCanvasWidth, canvasIncrCanvasHeight, canvasDecrCanvasHeight, NID_TOOLBAR_HSEP,
         canvasIncrCanvasHeightWidth, canvasDecrCanvasHeightWidth, NID_TOOLBAR_HSEP,
         canvasTool(None, canvasTool, 5), canvasTool(None, canvasTool, 0), canvasTool(None, canvasTool, 2), canvasTool(None, canvasTool, 3), canvasTool(None, canvasTool, 6), canvasTool(None, canvasTool, 1), canvasTool(None, canvasTool, 4),
        ),
        (canvasColour(None, canvasColour, 0), canvasColour(None, canvasColour, 1), canvasColour(None, canvasColour, 2), canvasColour(None, canvasColour, 3),
         canvasColour(None, canvasColour, 4), canvasColour(None, canvasColour, 5), canvasColour(None, canvasColour, 6), canvasColour(None, canvasColour, 7),
         canvasColour(None, canvasColour, 8), canvasColour(None, canvasColour, 9), canvasColour(None, canvasColour, 10), canvasColour(None, canvasColour, 11),
         canvasColour(None, canvasColour, 12), canvasColour(None, canvasColour, 13), canvasColour(None, canvasColour, 14), canvasColour(None, canvasColour, 15),
         canvasColourAlpha(None, canvasColourAlpha, 0), NID_TOOLBAR_HSEP,
         canvasIncrBrushWidth, canvasDecrBrushWidth, canvasIncrBrushHeight, canvasDecrBrushHeight, NID_TOOLBAR_HSEP,
         canvasIncrBrushHeightWidth, canvasDecrBrushHeightWidth,
        ),
    )
    # }}}

    #
    # __init__(self, parentCanvas, parentFrame):
    def __init__(self, parentCanvas, parentFrame):
        self.canvasPathName, self.imgurApiKey, self.lastPanelState, self.parentCanvas, self.parentFrame = None, ImgurApiKey.imgurApiKey, {}, parentCanvas, parentFrame
        self._initColourBitmaps()

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
