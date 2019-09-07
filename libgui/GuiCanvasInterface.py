#!/usr/bin/env python3
#
# GuiCanvasInterface.py -- XXX
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from ToolCircle import ToolCircle
from ToolFill import ToolFill
from ToolLine import ToolLine
from ToolSelectClone import ToolSelectClone
from ToolSelectMove import ToolSelectMove
from ToolRect import ToolRect
from ToolText import ToolText

from glob import glob
from GuiCanvasInterfaceAbout import GuiCanvasInterfaceAbout
from ImgurApiKey import ImgurApiKey
import io, os, random, sys, wx, wx.adv

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

    # {{{ canvasAbout(self, event): XXX
    def canvasAbout(self, event):
        GuiCanvasInterfaceAbout(self.parentFrame)
    # }}}
    # {{{ canvasBrushSolid(self, event): XXX
    def canvasBrushSolid(self, event):
        pass
    # }}}
    # {{{ canvasColour(self, event, numColour): XXX
    def canvasColour(self, event, numColour):
        if event.GetEventType() == wx.wxEVT_TOOL:
            self.parentCanvas.brushColours[0] = numColour
        elif event.GetEventType() == wx.wxEVT_TOOL_RCLICKED:
            self.parentCanvas.brushColours[1] = numColour
        self.parentFrame.update(colours=self.parentCanvas.brushColours)
    # }}}
    # {{{ canvasCopy(self, event): XXX
    def canvasCopy(self, event):
        pass
    # }}}
    # {{{ canvasCut(self, event): XXX
    def canvasCut(self, event):
        pass
    # }}}
    # {{{ canvasDelete(self, event): XXX
    def canvasDelete(self, event):
        pass
    # }}}
    # {{{ canvasExit(self, event): XXX
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
        self.parentFrame.update(pathName="", undoLevel=-1)
    # }}}
    # {{{ canvasOpen(self, event): XXX
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
                    self.parentFrame.update(pathName=self.canvasPathName, undoLevel=-1)
                    return True
                else:
                    print("error: {}".format(error), file=sys.stderr)
                    return False
    # }}}
    # {{{ canvasPaste(self, event): XXX
    def canvasPaste(self, event):
        pass
    # }}}
    # {{{ canvasRedo(self, event): XXX
    def canvasRedo(self, event):
        self.parentCanvas.dispatchDeltaPatches(self.parentCanvas.canvas.journal.popRedo())
        self.parentFrame.update(size=self.parentCanvas.canvas.size, undoLevel=self.parentCanvas.canvas.journal.patchesUndoLevel)
    # }}}
    # {{{ canvasSave(self, event): XXX
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
    def canvasSaveAs(self, event):
        with wx.FileDialog(self.parentCanvas, "Save As", os.getcwd(), "", "mIRC art files (*.txt)|*.txt|All Files (*.*)|*.*", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                self.canvasPathName = dialog.GetPath()
                return self.canvasSave(event)
    # }}}
    # {{{ canvasUndo(self, event): XXX
    def canvasUndo(self, event):
        self.parentCanvas.dispatchDeltaPatches(self.parentCanvas.canvas.journal.popUndo())
        self.parentFrame.update(size=self.parentCanvas.canvas.size, undoLevel=self.parentCanvas.canvas.journal.patchesUndoLevel)
    # }}}

    # {{{ canvasDecrBrushHeight(self, event): XXX
    def canvasDecrBrushHeight(self, event):
        if  self.parentCanvas.brushSize[1] > 1:
            self.parentCanvas.brushSize[1] -= 1
            self.parentFrame.update(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasDecrBrushHeightWidth(self, event): XXX
    def canvasDecrBrushHeightWidth(self, event):
        self.canvasDecrBrushHeight(event)
        self.canvasDecrBrushWidth(event)
    # }}}
    # {{{ canvasDecrBrushWidth(self, event): XXX
    def canvasDecrBrushWidth(self, event):
        if  self.parentCanvas.brushSize[0] > 1:
            self.parentCanvas.brushSize[0] -= 1
            self.parentFrame.update(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasDecrCanvasHeight(self, event): XXX
    def canvasDecrCanvasHeight(self, event):
        if self.parentCanvas.canvas.size[1] > 1:
            self.parentCanvas.resize([self.parentCanvas.canvas.size[0], self.parentCanvas.canvas.size[1] - 1])
    # }}}
    # {{{ canvasDecrCanvasHeightWidth(self, event): XXX
    def canvasDecrCanvasHeightWidth(self, event):
        self.canvasDecrCanvasHeight(event)
        self.canvasDecrCanvasWidth(event)
    # }}}
    # {{{ canvasDecrCanvasWidth(self, event): XXX
    def canvasDecrCanvasWidth(self, event):
        if self.parentCanvas.canvas.size[0] > 1:
            self.parentCanvas.resize([self.parentCanvas.canvas.size[0] - 1, self.parentCanvas.canvas.size[1]])
    # }}}
    # {{{ canvasIncrBrushHeight(self, event): XXX
    def canvasIncrBrushHeight(self, event):
        self.parentCanvas.brushSize[1] += 1
        self.parentFrame.update(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasIncrBrushHeightWidth(self, event): XXX
    def canvasIncrBrushHeightWidth(self, event):
        self.canvasIncrBrushHeight(event)
        self.canvasIncrBrushWidth(event)
    # }}}
    # {{{ canvasIncrBrushWidth(self, event): XXX
    def canvasIncrBrushWidth(self, event):
        self.parentCanvas.brushSize[0] += 1
        self.parentFrame.update(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasIncrCanvasHeight(self, event): XXX
    def canvasIncrCanvasHeight(self, event):
        self.parentCanvas.resize([self.parentCanvas.canvas.size[0], self.parentCanvas.canvas.size[1] + 1])
    # }}}
    # {{{ canvasIncrCanvasHeightWidth(self, event): XXX
    def canvasIncrCanvasHeightWidth(self, event):
        self.canvasIncrCanvasHeight(event)
        self.canvasIncrCanvasWidth(event)
    # }}}
    # {{{ canvasIncrCanvasWidth(self, event): XXX
    def canvasIncrCanvasWidth(self, event):
        self.parentCanvas.resize([self.parentCanvas.canvas.size[0] + 1, self.parentCanvas.canvas.size[1]])
    # }}}

    # {{{ canvasExportAsAnsi(self, event): XXX
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
    def canvasExportAsPng(self, event):
        with wx.FileDialog(self.parentFrame, "Save As...", os.getcwd(), "", "PNG (*.png)|*.png|All Files (*.*)|*.*", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                outPathName = dialog.GetPath()
                self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                self.parentCanvas.canvas.exportStore.exportBitmapToPngFile(          \
                    self.parentCanvas.canvasBackend.canvasBitmap, outPathName, wx.BITMAP_TYPE_PNG)
                self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
                return True
    # }}}
    # {{{ canvasExportImgur(self, event): XXX
    def canvasExportImgur(self, event):
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        rc, status, result = self.parentCanvas.canvas.exportStore.exportBitmapToImgur(   \
                self.imgurApiKey, self.parentCanvas.canvasBackend.canvasBitmap, "", "", wx.BITMAP_TYPE_PNG)
        self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
        if rc:
            if not wx.TheClipboard.IsOpened():
                wx.TheClipboard.Open(); wx.TheClipboard.SetData(wx.TextDataObject(result)); wx.TheClipboard.Close();
            wx.MessageBox("Exported to Imgur: {}".format(result), "Export to Imgur", wx.ICON_INFORMATION | wx.OK)
        else:
            wx.MessageBox("Failed to export to Imgur: {}".format(result), "Export to Imgur", wx.ICON_EXCLAMATION | wx.OK)
    # }}}
    # {{{ canvasExportPastebin(self, event): XXX
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
                    self.parentFrame.update(pathName="(Imported)", undoLevel=-1)
                    return True
                else:
                    print("error: {}".format(error), file=sys.stderr)
                    return False
    # }}}
    # {{{ canvasImportFromClipboard(self, event): XXX
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
                    self.parentFrame.update(pathName="(Clipboard)", undoLevel=-1)
                else:
                    print("error: {}".format(error), file=sys.stderr)
            wx.TheClipboard.Close()
        if not rc:
            with wx.MessageDialog(self.parentCanvas, "Clipboard does not contain text data and/or cannot be opened", "", wx.ICON_QUESTION | wx.OK | wx.OK_DEFAULT) as dialog:
                dialog.ShowModal()
    # }}}
    # {{{ canvasImportSauce(self, event): XXX
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
                    self.parentFrame.update(pathName="(Imported)", undoLevel=-1)
                    return True
                else:
                    print("error: {}".format(error), file=sys.stderr)
                    return False
    # }}}

    # {{{ canvasToolCircle(self, event): XXX
    def canvasToolCircle(self, event):
        self.canvasTool = ToolCircle(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_CIRCLE[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_CIRCLE[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_CIRCLE[0], True)
        self.parentFrame.update(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolFill(self, event): XXX
    def canvasToolFill(self, event):
        self.canvasTool = ToolFill(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_FILL[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_FILL[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_FILL[0], True)
        self.parentFrame.update(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolLine(self, event): XXX
    def canvasToolLine(self, event):
        self.canvasTool = ToolLine(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_LINE[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_LINE[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_LINE[0], True)
        self.parentFrame.update(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolSelectClone(self, event): XXX
    def canvasToolSelectClone(self, event):
        self.canvasTool = ToolSelectClone(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_CLONE_SELECT[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_CLONE_SELECT[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_CLONE_SELECT[0], True)
        self.parentFrame.update(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolSelectMove(self, event): XXX
    def canvasToolSelectMove(self, event):
        self.canvasTool = ToolSelectMove(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_MOVE_SELECT[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_MOVE_SELECT[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_MOVE_SELECT[0], True)
        self.parentFrame.update(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolRect(self, event): XXX
    def canvasToolRect(self, event):
        self.canvasTool = ToolRect(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_RECT[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_RECT[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_RECT[0], True)
        self.parentFrame.update(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolText(self, event): XXX
    def canvasToolText(self, event):
        self.canvasTool = ToolText(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_TEXT[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_TEXT[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_TEXT[0], True)
        self.parentFrame.update(toolName=self.canvasTool.name)
    # }}}

    #
    # __init__(self, parentCanvas, parentFrame):
    def __init__(self, parentCanvas, parentFrame):
        self.canvasPathName, self.imgurApiKey = None, ImgurApiKey.imgurApiKey
        self.parentCanvas, self.parentFrame = parentCanvas, parentFrame
        self.canvasToolRect(None)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
