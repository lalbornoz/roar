#!/usr/bin/env python3
#
# CanvasInterface.py -- XXX
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from ToolCircle import ToolCircle
from ToolFill  import ToolFill
from ToolLine import ToolLine
from ToolSelectClone import ToolSelectClone
from ToolSelectMove import ToolSelectMove
from ToolRect import ToolRect
from ToolText import ToolText
                
from glob import glob
import os, random, wx, wx.adv

class CanvasInterfaceAbout(wx.Dialog):
    """XXX"""

    # {{{ onButtonRoar(self, event): XXX
    def onButtonRoar(self, event):
        self.Destroy()
    # }}}
    # {{{ __init__(self, parent, size=(320, 240), title="About roar"): XXX
    def __init__(self, parent, size=(320, 240), title="About roar"):
        super(CanvasInterfaceAbout, self).__init__(parent, size=size, title=title)
        self.panel, self.sizer, self.sizerH1, self.sizerH2 = wx.Panel(self), wx.BoxSizer(wx.VERTICAL), wx.BoxSizer(wx.HORIZONTAL), wx.BoxSizer(wx.HORIZONTAL)

        logoPathNames = glob(os.path.join("assets", "images", "logo*.bmp"))
        logoPathName = logoPathNames[random.randint(0, len(logoPathNames) - 1)]
        self.logo = wx.StaticBitmap(self, -1, wx.Bitmap(logoPathName))
        self.sizerH1.Add(self.logo, 0, wx.CENTER)

        self.title = wx.StaticText(self.panel, label="roar -- mIRC art editor for Windows & Linux (Git revision __ROAR_RELEASE_GIT_SHORT_REV__)\nhttps://www.github.com/lalbornoz/roar/\nCopyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>", style=wx.ALIGN_CENTER)
        self.title.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=False))
        self.sizer.Add(self.title)

        labelsText = ["roar!", "ROAR!", "roaaaaaaar!", "ROAROARAOR", "_ROAR_"]
        labelText = labelsText[random.randint(0, len(labelsText) - 1)]
        self.buttonRoar = wx.Button(self.panel, label=labelText, pos=(75, 10))
        self.buttonRoar.Bind(wx.EVT_BUTTON, self.onButtonRoar)
        self.sizerH2.Add(self.buttonRoar, 0, wx.CENTER)

        self.sizer.Add(self.sizerH1, 0, wx.CENTER)
        self.sizer.Add(self.sizerH2, 0, wx.CENTER)
        self.SetSizer(self.sizer); self.sizer.Fit(self.panel);
        self.SetSize(size); self.SetTitle(title); self.Center();

        soundBitePathNames = glob(os.path.join("assets", "audio", "roar*.wav"))
        soundBitePathName = soundBitePathNames[random.randint(0, len(logoPathNames) - 1)]
        self.soundBite = wx.adv.Sound(soundBitePathName)
        if self.soundBite.IsOk():
            self.soundBite.Play(wx.adv.SOUND_ASYNC)

        self.ShowModal()
    # }}}

class CanvasInterface():
    """XXX"""
    imgurApiKey = None
    parentCanvas = parentFrame = canvasPathName = canvasTool = None

    # {{{ _dialogSaveChanges(self)
    def _dialogSaveChanges(self):
        with wx.MessageDialog(self.parentCanvas,                \
                "Do you want to save changes to {}?".format(    \
                    self.canvasPathName), "",            \
                wx.CANCEL|wx.CANCEL_DEFAULT|wx.ICON_QUESTION|wx.YES_NO) as dialog:
            dialogChoice = dialog.ShowModal()
            return dialogChoice
    # }}}

    # {{{ canvasAbout(self, event): XXX
    def canvasAbout(self, event):
        CanvasInterfaceAbout(self.parentFrame)
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
    # {{{ canvasDecrBrushHeight(self, event): XXX
    def canvasDecrBrushHeight(self, event):
        if  self.parentCanvas.brushSize[1] > 1:
            self.parentCanvas.brushSize[1] -= 1
            self.parentFrame.onCanvasUpdate(brushSize=self.parentCanvas.brushSize)
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
            self.parentFrame.onCanvasUpdate(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasDecrCanvasHeight(self, event): XXX
    def canvasDecrCanvasHeight(self, event):
        if self.parentCanvas.canvasSize[1] > 1:
            self.parentCanvas.resize([                  \
                    self.parentCanvas.canvasSize[0],    \
                    self.parentCanvas.canvasSize[1]-1])
    # }}}
    # {{{ canvasDecrCanvasHeightWidth(self, event): XXX
    def canvasDecrCanvasHeightWidth(self, event):
        self.canvasDecrCanvasHeight(event)
        self.canvasDecrCanvasWidth(event)
    # }}}
    # {{{ canvasDecrCanvasWidth(self, event): XXX
    def canvasDecrCanvasWidth(self, event):
        if self.parentCanvas.canvasSize[0] > 1:
            self.parentCanvas.resize([                  \
                    self.parentCanvas.canvasSize[0]-1,  \
                    self.parentCanvas.canvasSize[1]])
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
    # {{{ canvasExportAsPng(self, event): XXX
    def canvasExportAsPng(self, event):
        with wx.FileDialog(self, "Save As...", os.getcwd(), "",                 \
                "*.png", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return False
            else:
                outPathName = dialog.GetPath()
                self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                self.parentCanvas.canvasExportStore.exportBitmapToPngFile(      \
                    self.parentCanvas.canvasBackend.canvasBitmap, outPathName,  \
                        wx.BITMAP_TYPE_PNG)
                self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
                return True
    # }}}
    # {{{ canvasExportImgur(self, event): XXX
    def canvasExportImgur(self, event):
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        imgurResult = self.parentCanvas.canvasExportStore.exportBitmapToImgur(  \
            self.imgurApiKey, self.parentCanvas.canvasBackend.canvasBitmap,     \
            "", "", wx.BITMAP_TYPE_PNG)
        self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
        if imgurResult[0] == 200:
            if not wx.TheClipboard.IsOpened():
                wx.TheClipboard.Open()
                wx.TheClipboard.SetData(wx.TextDataObject(imgurResult[1]))
                wx.TheClipboard.Close()
            wx.MessageBox("Exported to Imgur: " + imgurResult[1],               \
                "Export to Imgur", wx.OK|wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Failed to export to Imgur: " + imgurResult[1],       \
                "Export to Imgur", wx.OK|wx.ICON_EXCLAMATION)
    # }}}
    # {{{ canvasExportPastebin(self, event): XXX
    def canvasExportPastebin(self, event):
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        pasteStatus, pasteResult =                                          \
            self.parentCanvas.canvasExportStore.exportPastebin(             \
                "",                          \
                self.parentCanvas.canvasMap,                                \
                self.parentCanvas.canvasSize)
        self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
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
    # {{{ canvasIncrBrushHeight(self, event): XXX
    def canvasIncrBrushHeight(self, event):
        self.parentCanvas.brushSize[1] += 1
        self.parentFrame.onCanvasUpdate(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasIncrBrushHeightWidth(self, event): XXX
    def canvasIncrBrushHeightWidth(self, event):
        self.canvasIncrBrushHeight(event)
        self.canvasIncrBrushWidth(event)
    # }}}
    # {{{ canvasIncrBrushWidth(self, event): XXX
    def canvasIncrBrushWidth(self, event):
        self.parentCanvas.brushSize[0] += 1
        self.parentFrame.onCanvasUpdate(brushSize=self.parentCanvas.brushSize)
    # }}}
    # {{{ canvasIncrCanvasHeight(self, event): XXX
    def canvasIncrCanvasHeight(self, event):
        self.parentCanvas.resize([              \
            self.parentCanvas.canvasSize[0],    \
            self.parentCanvas.canvasSize[1] + 1])
    # }}}
    # {{{ canvasIncrCanvasHeightWidth(self, event): XXX
    def canvasIncrCanvasHeightWidth(self, event):
        self.canvasIncrCanvasHeight(event)
        self.canvasIncrCanvasWidth(event)
    # }}}
    # {{{ canvasIncrCanvasWidth(self, event): XXX
    def canvasIncrCanvasWidth(self, event):
        self.parentCanvas.resize([                  \
            self.parentCanvas.canvasSize[0] + 1,    \
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
                self.canvasSave(event)
        self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        if newCanvasSize == None:
            newCanvasSize = list(self.parentCanvas.defaultCanvasSize)
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
                self.canvasSave(event)
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
                self.parentCanvas.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
                self.parentCanvas.canvasExportStore.exportTextFile(      \
                    self.parentCanvas.canvasMap,                         \
                    self.parentCanvas.canvasSize, outFile)
                self.parentCanvas.SetCursor(wx.Cursor(wx.NullCursor))
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
        self.canvasTool = ToolCircle(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_CIRCLE[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_CIRCLE[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_CIRCLE[0], True)
        self.parentFrame.onCanvasUpdate(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolFill(self, event): XXX
    def canvasToolFill(self, event):
        self.canvasTool = ToolFill(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_FILL[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_FILL[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_FILL[0], True)
        self.parentFrame.onCanvasUpdate(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolLine(self, event): XXX
    def canvasToolLine(self, event):
        self.canvasTool = ToolLine(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_LINE[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_LINE[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_LINE[0], True)
        self.parentFrame.onCanvasUpdate(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolSelectClone(self, event): XXX
    def canvasToolSelectClone(self, event):
        self.canvasTool = ToolSelectClone(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_CLONE_SELECT[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_CLONE_SELECT[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_CLONE_SELECT[0], True)
        self.parentFrame.onCanvasUpdate(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolSelectMove(self, event): XXX
    def canvasToolSelectMove(self, event):
        self.canvasTool = ToolSelectMove(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_MOVE_SELECT[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_MOVE_SELECT[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_MOVE_SELECT[0], True)
        self.parentFrame.onCanvasUpdate(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolRect(self, event): XXX
    def canvasToolRect(self, event):
        self.canvasTool = ToolRect(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_RECT[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_RECT[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_RECT[0], True)
        self.parentFrame.onCanvasUpdate(toolName=self.canvasTool.name)
    # }}}
    # {{{ canvasToolText(self, event): XXX
    def canvasToolText(self, event):
        self.canvasTool = ToolText(self.parentCanvas)
        self.parentFrame.menuItemsById[self.parentFrame.CID_TEXT[0]].Check(True)
        toolBar = self.parentFrame.toolBarItemsById[self.parentFrame.CID_TEXT[0]].GetToolBar()
        toolBar.ToggleTool(self.parentFrame.CID_TEXT[0], True)
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
