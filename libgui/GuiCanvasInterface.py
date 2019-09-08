#!/usr/bin/env python3
#
# GuiCanvasInterface.py -- XXX
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
    """XXX"""
    # {{{ GuiCanvasCommandDecoratorOuter(targetObject): XXX
    def GuiCanvasCommandDecoratorOuter(targetObject):
        if callable(targetObject):
            if not hasattr(targetObject, "attrDict"):
                setattr(targetObject, "attrDict", [])
            targetObject.attrDict = {"caption": caption, "label": label, "icon": icon, "accel": accel, "initialState": initialState, "id": None}
            return targetObject
    return GuiCanvasCommandDecoratorOuter
    # }}}

def GuiCanvasSelectDecorator(idx, caption, label, icon, accel, initialState):
    """XXX"""
    # {{{ GuiCanvasSelectDecoratorOuter(targetObject): XXX
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
    """XXX"""

    # {{{ _dialogSaveChanges(self): XXX
    def _dialogSaveChanges(self):
        with wx.MessageDialog(self.parentCanvas,                                    \
                "Do you want to save changes to {}?".format(self.canvasPathName),   \
                "", wx.CANCEL|wx.CANCEL_DEFAULT|wx.ICON_QUESTION|wx.YES_NO) as dialog:
            dialogChoice = dialog.ShowModal()
            return dialogChoice
    # }}}
    # {{{ _initColourBitmaps(self): XXX
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

    # {{{ canvasAbout(self, event): XXX
    @GuiCanvasCommandDecorator("About", "&About", None, None, True)
    def canvasAbout(self, event):
        GuiCanvasInterfaceAbout(self.parentFrame)
    # }}}
    # {{{ canvasBrush(self, f, idx): XXX
    @GuiCanvasSelectDecorator(0, "Solid brush", "Solid brush", None, None, True)
    def canvasBrush(self, f, idx):
        def canvasBrush_(self, event):
            pass
        setattr(canvasBrush_, "attrDict", f.attrList[idx])
        setattr(canvasBrush_, "isSelect", True)
        return canvasBrush_
    # }}}
    # {{{ canvasColour(self, f, idx): XXX
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
    # {{{ canvasColourAlpha(self, f, idx): XXX
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
    # {{{ canvasCopy(self, event): XXX
    @GuiCanvasCommandDecorator("Copy", "&Copy", ["", wx.ART_COPY], None, False)
    def canvasCopy(self, event):
        pass
    # }}}
    # {{{ canvasCut(self, event): XXX
    @GuiCanvasCommandDecorator("Cut", "Cu&t", ["", wx.ART_CUT], None, False)
    def canvasCut(self, event):
        pass
    # }}}
    # {{{ canvasDelete(self, event): XXX
    @GuiCanvasCommandDecorator("Delete", "De&lete", ["", wx.ART_DELETE], None, False)
    def canvasDelete(self, event):
        pass
    # }}}
    # {{{ canvasExit(self, event): XXX
    @GuiCanvasCommandDecorator("Exit", "E&xit", None, [wx.ACCEL_CTRL, ord("X")], None)
    def canvasExit(self, event):
        if self.canvasPathName != None:
            saveChanges = self._dialogSaveChanges()
            if saveChanges == wx.ID_CANCEL:
                return
            elif saveChanges == wx.ID_NO:
                pass
            elif saveChanges == wx.ID_YES:
                self.canvasSave(event)
        self.parentFrame.Close(True)
    # }}}
    # {{{ canvasNew(self, event, newCanvasSize=None): XXX
    @GuiCanvasCommandDecorator("New", "&New", ["", wx.ART_NEW], [wx.ACCEL_CTRL, ord("N")], None)
    def canvasNew(self, event, newCanvasSize=None):
        if self.canvasPathName != None:
            saveChanges = self._dialogSaveChanges()
            if saveChanges == wx.ID_CANCEL:
                return
            elif saveChanges == wx.ID_NO:
                pass
            elif saveChanges == wx.ID_YES:
                self.canvasSave(event)
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        if newCanvasSize == None:
            newCanvasSize = list(self.parentCanvas.defaultCanvasSize)
        newMap = [[[1, 1, 0, " "] for x in range(newCanvasSize[0])] for y in range(newCanvasSize[1])]
        self.parentCanvas.update(newCanvasSize, False, newMap)
        self.canvasPathName = None
        self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
        self.update(pathName="", undoLevel=-1)
    # }}}
    # {{{ canvasOpen(self, event): XXX
    @GuiCanvasCommandDecorator("Open", "&Open", ["", wx.ART_FILE_OPEN], [wx.ACCEL_CTRL, ord("O")], None)
    def canvasOpen(self, event):
        if self.canvasPathName != None:
            saveChanges = self._dialogSaveChanges()
            if saveChanges == wx.ID_CANCEL:
                return
            elif saveChanges == wx.ID_NO:
                pass
            elif saveChanges == wx.ID_YES:
                self.canvasSave(event)
        with wx.FileDialog(self.parentCanvas, "Open", os.getcwd(), "", "mIRC art files (*.txt)|*.txt|All Files (*.*)|*.*", wx.FD_OPEN) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                self.canvasPathName = dialog.GetPath()
                self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                rc, error = self.parentCanvas.canvas.importStore.importTextFile(self.canvasPathName)
                if rc:
                    self.parentCanvas.update(self.parentCanvas.canvas.importStore.inSize, False, self.parentCanvas.canvas.importStore.outMap)
                    self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
                    self.update(pathName=self.canvasPathName, undoLevel=-1)
                    return True
                else:
                    print("error: {}".format(error), file=sys.stderr)
                    return False
    # }}}
    # {{{ canvasPaste(self, event): XXX
    @GuiCanvasCommandDecorator("Paste", "&Paste", ["", wx.ART_PASTE], None, False)
    def canvasPaste(self, event):
        pass
    # }}}
    # {{{ canvasRedo(self, event): XXX
    @GuiCanvasCommandDecorator("Redo", "&Redo", ["", wx.ART_REDO], [wx.ACCEL_CTRL, ord("Y")], False)
    def canvasRedo(self, event):
        self.parentCanvas.dispatchDeltaPatches(self.parentCanvas.canvas.journal.popRedo())
        self.update(size=self.parentCanvas.canvas.size, undoLevel=self.parentCanvas.canvas.journal.patchesUndoLevel)
    # }}}
    # {{{ canvasSave(self, event): XXX
    @GuiCanvasCommandDecorator("Save", "&Save", ["", wx.ART_FILE_SAVE], [wx.ACCEL_CTRL, ord("S")], None)
    def canvasSave(self, event):
        if self.canvasPathName == None:
            if self.canvasSaveAs(event) == False:
                return
        try:
            with open(self.canvasPathName, "w", encoding="utf-8") as outFile:
                self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                self.parentCanvas.canvas.exportStore.exportTextFile(                 \
                    self.parentCanvas.canvas.map, self.parentCanvas.canvas.size, outFile)
                self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
                return True
        except IOError as error:
            return False
    # }}}
    # {{{ canvasSaveAs(self, event): XXX
    @GuiCanvasCommandDecorator("Save As...", "Save &As...", ["", wx.ART_FILE_SAVE_AS], None, None)
    def canvasSaveAs(self, event):
        with wx.FileDialog(self.parentCanvas, "Save As", os.getcwd(), "", "mIRC art files (*.txt)|*.txt|All Files (*.*)|*.*", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                self.canvasPathName = dialog.GetPath()
                return self.canvasSave(event)
    # }}}
    # {{{ canvasUndo(self, event): XXX
    @GuiCanvasCommandDecorator("Undo", "&Undo", ["", wx.ART_UNDO], [wx.ACCEL_CTRL, ord("Z")], False)
    def canvasUndo(self, event):
        self.parentCanvas.dispatchDeltaPatches(self.parentCanvas.canvas.journal.popUndo())
        self.update(size=self.parentCanvas.canvas.size, undoLevel=self.parentCanvas.canvas.journal.patchesUndoLevel)
    # }}}

    # {{{ canvasDecrBrushHeight(self, event): XXX
    @GuiCanvasCommandDecorator("Decrease brush height", "Decrease brush height", ["toolDecrBrushH.png"], None, None)
    def canvasDecrBrushHeight(self, event):
        if  self.parentCanvas.brushSize[1] > 1:
            self.parentCanvas.brushSize[1] -= 1
            self.update(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasDecrBrushHeightWidth(self, event): XXX
    @GuiCanvasCommandDecorator("Decrease brush size", "Decrease brush size", ["toolDecrBrushHW.png"], None, None)
    def canvasDecrBrushHeightWidth(self, event):
        self.canvasDecrBrushHeight(event)
        self.canvasDecrBrushWidth(event)
    # }}}
    # {{{ canvasDecrBrushWidth(self, event): XXX
    @GuiCanvasCommandDecorator("Decrease brush width", "Decrease brush width", ["toolDecrBrushW.png"], None, None)
    def canvasDecrBrushWidth(self, event):
        if  self.parentCanvas.brushSize[0] > 1:
            self.parentCanvas.brushSize[0] -= 1
            self.update(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasDecrCanvasHeight(self, event): XXX
    @GuiCanvasCommandDecorator("Decrease canvas height", "Decrease canvas height", ["toolDecrCanvasH.png"], None, None)
    def canvasDecrCanvasHeight(self, event):
        if self.parentCanvas.canvas.size[1] > 1:
            self.parentCanvas.resize([self.parentCanvas.canvas.size[0], self.parentCanvas.canvas.size[1] - 1])
    # }}}
    # {{{ canvasDecrCanvasHeightWidth(self, event): XXX
    @GuiCanvasCommandDecorator("Decrease canvas size", "Decrease canvas size", ["toolDecrCanvasHW.png"], None, None)
    def canvasDecrCanvasHeightWidth(self, event):
        self.canvasDecrCanvasHeight(event)
        self.canvasDecrCanvasWidth(event)
    # }}}
    # {{{ canvasDecrCanvasWidth(self, event): XXX
    @GuiCanvasCommandDecorator("Decrease canvas width", "Decrease canvas width", ["toolDecrCanvasW.png"], None, None)
    def canvasDecrCanvasWidth(self, event):
        if self.parentCanvas.canvas.size[0] > 1:
            self.parentCanvas.resize([self.parentCanvas.canvas.size[0] - 1, self.parentCanvas.canvas.size[1]])
    # }}}
    # {{{ canvasIncrBrushHeight(self, event): XXX
    @GuiCanvasCommandDecorator("Increase brush height", "Increase brush height", ["toolIncrBrushH.png"], None, None)
    def canvasIncrBrushHeight(self, event):
        self.parentCanvas.brushSize[1] += 1
        self.update(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasIncrBrushHeightWidth(self, event): XXX
    @GuiCanvasCommandDecorator("Increase brush size", "Increase brush size", ["toolIncrBrushHW.png"], None, None)
    def canvasIncrBrushHeightWidth(self, event):
        self.canvasIncrBrushHeight(event)
        self.canvasIncrBrushWidth(event)
    # }}}
    # {{{ canvasIncrBrushWidth(self, event): XXX
    @GuiCanvasCommandDecorator("Increase brush width", "Increase brush width", ["toolIncrBrushW.png"], None, None)
    def canvasIncrBrushWidth(self, event):
        self.parentCanvas.brushSize[0] += 1
        self.update(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasIncrCanvasHeight(self, event): XXX
    @GuiCanvasCommandDecorator("Increase canvas height", "Increase canvas height", ["toolIncrCanvasH.png"], None, None)
    def canvasIncrCanvasHeight(self, event):
        self.parentCanvas.resize([self.parentCanvas.canvas.size[0], self.parentCanvas.canvas.size[1] + 1])
    # }}}
    # {{{ canvasIncrCanvasHeightWidth(self, event): XXX
    @GuiCanvasCommandDecorator("Increase canvas size", "Increase canvas size", ["toolIncrCanvasHW.png"], None, None)
    def canvasIncrCanvasHeightWidth(self, event):
        self.canvasIncrCanvasHeight(event)
        self.canvasIncrCanvasWidth(event)
    # }}}
    # {{{ canvasIncrCanvasWidth(self, event): XXX
    @GuiCanvasCommandDecorator("Increase canvas width", "Increase canvas width", ["toolIncrCanvasW.png"], None, None)
    def canvasIncrCanvasWidth(self, event):
        self.parentCanvas.resize([self.parentCanvas.canvas.size[0] + 1, self.parentCanvas.canvas.size[1]])
    # }}}
    # {{{ canvasTool(self, f, idx): XXX
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

    # {{{ canvasExportAsAnsi(self, event): XXX
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
    # {{{ canvasExportAsPng(self, event): XXX
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
    # {{{ canvasExportImgur(self, event): XXX
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
    # {{{ canvasExportPastebin(self, event): XXX
    @GuiCanvasCommandDecorator("Export to Pastebin...", "Export to Pasteb&in...", None, None, haveUrllib)
    def canvasExportPastebin(self, event):
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        pasteStatus, pasteResult = self.parentCanvas.canvas.exportStore.exportPastebin("", self.parentCanvas.canvas.map, self.parentCanvas.canvas.size)
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
    # {{{ canvasExportToClipboard(self, event): XXX
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
    # {{{ canvasImportAnsi(self, event): XXX
    @GuiCanvasCommandDecorator("Import ANSI...", "Import ANSI...", None, None, None)
    def canvasImportAnsi(self, event):
        if self.canvasPathName != None:
            saveChanges = self._dialogSaveChanges()
            if saveChanges == wx.ID_CANCEL:
                return
            elif saveChanges == wx.ID_NO:
                pass
            elif saveChanges == wx.ID_YES:
                self.canvasSave(event)
        with wx.FileDialog(self.parentCanvas, "Open", os.getcwd(), "", "ANSI files (*.ans;*.txt)|*.ans;*.txt|All Files (*.*)|*.*", wx.FD_OPEN) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                self.canvasPathName = dialog.GetPath()
                self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                rc, error = self.parentCanvas.canvas.importStore.importAnsiFile(self.canvasPathName)
                if rc:
                    self.parentCanvas.update(self.parentCanvas.canvas.importStore.inSize, False, self.parentCanvas.canvas.importStore.outMap)
                    self.canvasPathName = "(Imported)"
                    self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
                    self.update(pathName="(Imported)", undoLevel=-1)
                    return True
                else:
                    print("error: {}".format(error), file=sys.stderr)
                    return False
    # }}}
    # {{{ canvasImportFromClipboard(self, event): XXX
    @GuiCanvasCommandDecorator("Import from clipboard", "&Import from clipboard", None, None, None)
    def canvasImportFromClipboard(self, event):
        rc = False
        if  wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT))                  \
        and wx.TheClipboard.Open():
            inBuffer = wx.TextDataObject()
            if wx.TheClipboard.GetData(inBuffer):
                if self.canvasPathName != None:
                    saveChanges = self._dialogSaveChanges()
                    if saveChanges == wx.ID_CANCEL:
                        return
                    elif saveChanges == wx.ID_NO:
                        pass
                    elif saveChanges == wx.ID_YES:
                        self.canvasSave(event)
                self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                rc, error = self.parentCanvas.canvas.importStore.importTextBuffer(io.StringIO(inBuffer.GetText()))
                if rc:
                    self.parentCanvas.update(self.parentCanvas.canvas.importStore.inSize, False, self.parentCanvas.canvas.importStore.outMap)
                    self.canvasPathName = "(Clipboard)"
                    self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
                    self.update(pathName="(Clipboard)", undoLevel=-1)
                else:
                    print("error: {}".format(error), file=sys.stderr)
            wx.TheClipboard.Close()
        if not rc:
            with wx.MessageDialog(self.parentCanvas, "Clipboard does not contain text data and/or cannot be opened", "", wx.ICON_QUESTION | wx.OK | wx.OK_DEFAULT) as dialog:
                dialog.ShowModal()
    # }}}
    # {{{ canvasImportSauce(self, event): XXX
    @GuiCanvasCommandDecorator("Import SAUCE...", "Import SAUCE...", None, None, None)
    def canvasImportSauce(self, event):
        if self.canvasPathName != None:
            saveChanges = self._dialogSaveChanges()
            if saveChanges == wx.ID_CANCEL:
                return
            elif saveChanges == wx.ID_NO:
                pass
            elif saveChanges == wx.ID_YES:
                self.canvasSave(event)
        with wx.FileDialog(self.parentCanvas, "Open", os.getcwd(), "", "SAUCE files (*.ans;*.txt)|*.ans;*.txt|All Files (*.*)|*.*", wx.FD_OPEN) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                self.canvasPathName = dialog.GetPath()
                self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                rc, error = self.parentCanvas.canvas.importStore.importSauceFile(self.canvasPathName)
                if rc:
                    self.parentCanvas.update(self.parentCanvas.canvas.importStore.inSize, False, self.parentCanvas.canvas.importStore.outMap)
                    self.canvasPathName = "(Imported)"
                    self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
                    self.update(pathName="(Imported)", undoLevel=-1)
                    return True
                else:
                    print("error: {}".format(error), file=sys.stderr)
                    return False
    # }}}

    # {{{ update(self, **kwargs): XXX
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
            if self.lastPanelState["pathName"] != "":
                basePathName = os.path.basename(self.lastPanelState["pathName"])
                textItems.append("Current file: {}".format(basePathName))
                self.parentFrame.SetTitle("{} - roar".format(basePathName))
            else:
                self.parentFrame.SetTitle("roar")
        if "toolName" in self.lastPanelState:
            textItems.append("Current tool: {}".format(self.lastPanelState["toolName"]))
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
