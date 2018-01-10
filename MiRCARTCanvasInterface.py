#!/usr/bin/env python3
#
# MiRCARTCanvasInterface.py -- XXX
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

from MiRCARTToolCircle import MiRCARTToolCircle
from MiRCARTToolLine import MiRCARTToolLine
from MiRCARTToolRect import MiRCARTToolRect
from MiRCARTToolText import MiRCARTToolText
                
import os, wx

class MiRCARTCanvasInterface():
    """XXX"""
    parentCanvas = parentFrame = canvasPathName = canvasTool = None

    # {{{ _dialogSaveChanges(self)
    def _dialogSaveChanges(self):
        with wx.MessageDialog(self.parentCanvas,                \
                "Do you want to save changes to {}?".format(    \
                    self.canvasPathName), "MiRCART",            \
                wx.CANCEL|wx.CANCEL_DEFAULT|wx.ICON_QUESTION|wx.YES_NO) as dialog:
            dialogChoice = dialog.ShowModal()
            return dialogChoice
    # }}}
    # {{{ _updateCanvasSize(self, newCanvasSize): XXX
    def _updateCanvasSize(self, newCanvasSize):
        eventDc = self.parentCanvas.canvasBackend.getDeviceContext(self.parentCanvas)
        self.parentCanvas.resize(newCanvasSize)
        self.parentCanvas.canvasBackend.resize(                  \
            newCanvasSize,                                      \
            self.parentCanvas.canvasBackend.cellSize)
        for numRow in range(self.parentCanvas.canvasSize[1] - 1):
            self.parentCanvas.canvasMap.append([[1, 1], 0, " "])
        self.parentCanvas.canvasMap.append([])
        for numCol in range(self.parentCanvas.canvasSize[0]):
            self.parentCanvas.canvasMap[-1].append([[1, 1], 0, " "])
            self.parentCanvas.canvasBackend.drawPatch(eventDc,   \
                ([numCol, self.parentCanvas.canvasSize[1] - 1], *[[1, 1], 0, " "]))
        wx.SafeYield()
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
        self.parentFrame.onCanvasUpdate(colours=self.parentCanvas.brushColours)
    # }}}
    # {{{ canvasCopy(self, event): XXX
    def canvasCopy(self, event):
        pass
    # }}}
    # {{{ canvasCut(self, event): XXX
    def canvasCut(self, event):
        pass
    # }}}
    # {{{ canvasDecrBrush(self, event): XXX
    def canvasDecrBrush(self, event):
        if  self.parentCanvas.brushSize[0] > 1   \
        and self.parentCanvas.brushSize[1] > 1:
            self.parentCanvas.brushSize =        \
                [a-1 for a in self.parentCanvas.brushSize]
            self.parentFrame.onCanvasUpdate(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasDecrCanvasHeight(self, event): XXX
    def canvasDecrCanvasHeight(self, event):
        if self.parentCanvas.canvasSize[1] > 1:
            self._updateCanvasSize([                        \
                    self.parentCanvas.canvasSize[0],        \
                    self.parentCanvas.canvasSize[1]-1])
    # }}}
    # {{{ canvasDecrCanvasWidth(self, event): XXX
    def canvasDecrCanvasWidth(self, event):
        if self.parentCanvas.canvasSize[0] > 1:
            self._updateCanvasSize([                        \
                    self.parentCanvas.canvasSize[0]-1,        \
                    self.parentCanvas.canvasSize[1]])
    # }}}
    # {{{ canvasDelete(self, event): XXX
    def canvasDelete(self, event):
        pass
    # }}}
    # {{{ canvasExit(self, event): XXX
    def canvasExit(self, event):
        self.parentFrame.Close(True)
    # }}}
    # {{{ canvasExportAsPng(self, event): XXX
    def canvasExportAsPng(self, event):
        with wx.FileDialog(self, "Save As...", os.getcwd(), "",                 \
                "*.png", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                outPathName = dialog.GetPath()
                self.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                self.parentCanvas.canvasExportStore.exportBitmapToPngFile(      \
                    self.parentCanvas.canvasBackend.canvasBitmap, outPathName,  \
                        wx.BITMAP_TYPE_PNG)
                self.SetCursor(wx.Cursor(wx.NullCursor))
                return True
    # }}}
    # {{{ canvasExportImgur(self, event): XXX
    def canvasExportImgur(self, event):
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        imgurResult = self.parentCanvas.canvasExportStore.exportBitmapToImgur(   \
            "c9a6efb3d7932fd", self.parentCanvas.canvasBackend.canvasBitmap,     \
            "", "", wx.BITMAP_TYPE_PNG)
        self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
        if imgurResult[0] == 200:
            if not wx.TheClipboard.IsOpened():
                wx.TheClipboard.Open()
                wx.TheClipboard.SetData(wx.TextDataObject(imgurResult[1]))
                wx.TheClipboard.Close()
            wx.MessageBox("Exported to Imgur: " + imgurResult[1],           \
                "Export to Imgur", wx.OK|wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Failed to export to Imgur: " + imgurResult[1],   \
                "Export to Imgur", wx.OK|wx.ICON_EXCLAMATION)
    # }}}
    # {{{ canvasExportPastebin(self, event): XXX
    def canvasExportPastebin(self, event):
        self.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        pasteStatus, pasteResult =                                          \
            self.parentCanvas.canvasExportStore.exportPastebin(              \
                "",                          \
                self.parentCanvas.canvasMap,                                 \
                self.parentCanvas.canvasSize)
        self.SetCursor(wx.Cursor(wx.NullCursor))
        if pasteStatus:
            if not wx.TheClipboard.IsOpened():
                wx.TheClipboard.Open()
                wx.TheClipboard.SetData(wx.TextDataObject(pasteResult))
                wx.TheClipboard.Close()
            wx.MessageBox("Exported to Pastebin: " + pasteResult,           \
                "Export to Pastebin", wx.OK|wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Failed to export to Pastebin: " + pasteResult,   \
                "Export to Pastebin", wx.OK|wx.ICON_EXCLAMATION)
    # }}}
    # {{{ canvasIncrBrush(self, event): XXX
    def canvasIncrBrush(self, event):
        self.parentCanvas.brushSize =    \
                [a+1 for a in self.parentCanvas.brushSize]
        self.parentFrame.onCanvasUpdate(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasIncrCanvasHeight(self, event): XXX
    def canvasIncrCanvasHeight(self, event):
        self._updateCanvasSize([                \
            self.parentCanvas.canvasSize[0],    \
            self.parentCanvas.canvasSize[1]+1])
    # }}}
    # {{{ canvasIncrCanvasWidth(self, event): XXX
    def canvasIncrCanvasWidth(self, event):
        self._updateCanvasSize([                \
            self.parentCanvas.canvasSize[0]+1,  \
            self.parentCanvas.canvasSize[1]])
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
                self.canvasSave()
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        if newCanvasSize == None:
            newCanvasSize = (100, 30)
        self.parentCanvas.canvasImportStore.importNew(newCanvasSize)
        self.canvasPathName = None
        self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
        self.parentFrame.onCanvasUpdate(pathName="", undoLevel=-1)
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
                self.canvasSave()
        with wx.FileDialog(self.parentCanvas, "Open", os.getcwd(), "",  \
                "*.txt", wx.FD_OPEN) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                self.canvasPathName = dialog.GetPath()
                self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                self.parentCanvas.canvasImportStore.importTextFile(self.canvasPathName)
                self.parentCanvas.canvasImportStore.importIntoPanel()
                self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
                self.parentFrame.onCanvasUpdate(                        \
                    pathName=self.canvasPathName, undoLevel=-1)
                return True
    # }}}
    # {{{ canvasPaste(self, event): XXX
    def canvasPaste(self, event):
        pass
    # }}}
    # {{{ canvasRedo(self, event): XXX
    def canvasRedo(self, event):
        self.parentCanvas._dispatchDeltaPatches(    \
            self.parentCanvas.canvasJournal.popRedo())
    # }}}
    # {{{ canvasSave(self, event): XXX
    def canvasSave(self, event):
        if self.canvasPathName == None:
            if self.canvasSaveAs(event) == False:
                return
        try:
            with open(self.canvasPathName, "w") as outFile:
                self.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                self.parentCanvas.canvasExportStore.exportTextFile(      \
                    self.parentCanvas.canvasMap,                         \
                    self.parentCanvas.canvasSize, outFile)
                self.SetCursor(wx.Cursor(wx.NullCursor))
                return True
        except IOError as error:
            return False
    # }}}
    # {{{ canvasSaveAs(self, event): XXX
    def canvasSaveAs(self, event):
        with wx.FileDialog(self.parentCanvas, "Save As", os.getcwd(), "",   \
                "*.txt", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                self.canvasPathName = dialog.GetPath()
                return self.canvasSave(event)
    # }}}
    # {{{ canvasToolCircle(self, event): XXX
    def canvasToolCircle(self, event):
        self.canvasTool = MiRCARTToolCircle(self.parentCanvas)
        self.parentFrame.onCanvasUpdate(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolLine(self, event): XXX
    def canvasToolLine(self, event):
        self.canvasTool = MiRCARTToolLine(self.parentCanvas)
        self.parentFrame.onCanvasUpdate(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolRect(self, event): XXX
    def canvasToolRect(self, event):
        self.canvasTool = MiRCARTToolRect(self.parentCanvas)
        self.parentFrame.onCanvasUpdate(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolText(self, event): XXX
    def canvasToolText(self, event):
        self.canvasTool = MiRCARTToolText(self.parentCanvas)
        self.parentFrame.onCanvasUpdate(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasUndo(self, event): XXX
    def canvasUndo(self, event):
        self.parentCanvas._dispatchDeltaPatches(    \
            self.parentCanvas.canvasJournal.popUndo())
    # }}}

    #
    # __init__(self, parentCanvas, parentFrame):
    def __init__(self, parentCanvas, parentFrame):
        self.parentCanvas = parentCanvas; self.parentFrame = parentFrame;
        self.canvasPathName = None
        self.canvasToolRect(None)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
