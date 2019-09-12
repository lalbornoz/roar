#!/usr/bin/env python3
#
# RoarCanvasCommandsEdit.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiFrame import GuiCommandDecorator, GuiCommandListDecorator, GuiSelectDecorator, NID_MENU_SEP
import wx

class RoarCanvasCommandsEdit():
    # {{{ canvasAssetsWindowHide(self, event)
    @GuiCommandDecorator("Hide assets window", "Hide assets window", None, None, False)
    def canvasAssetsWindowHide(self, event):
        self.parentFrame.assetsWindow.Show(False)
        self.parentFrame.menuItemsById[self.canvasAssetsWindowHide.attrDict["id"]].Enable(False)
        self.parentFrame.menuItemsById[self.canvasAssetsWindowShow.attrDict["id"]].Enable(True)
    # }}}
    # {{{ canvasAssetsWindowShow(self, event)
    @GuiCommandDecorator("Show assets window", "Show assets window", None, None, False)
    def canvasAssetsWindowShow(self, event):
        self.parentFrame.assetsWindow.Show(True)
        self.parentFrame.menuItemsById[self.canvasAssetsWindowHide.attrDict["id"]].Enable(True)
        self.parentFrame.menuItemsById[self.canvasAssetsWindowShow.attrDict["id"]].Enable(False)
    # }}}
    # {{{ canvasBrush(self, f, idx)
    @GuiSelectDecorator(0, "Solid brush", "Solid brush", None, None, True)
    def canvasBrush(self, f, idx):
        def canvasBrush_(self, event):
            pass
        setattr(canvasBrush_, "attrDict", f.attrList[idx])
        setattr(canvasBrush_, "isSelect", True)
        return canvasBrush_
    # }}}
    # {{{ canvasBrushSize(self, f, dimension, incrFlag)
    @GuiCommandListDecorator(0, "Decrease brush width", "Decrease brush width", ["toolDecrBrushW.png"], None, None)
    @GuiCommandListDecorator(1, "Decrease brush height", "Decrease brush height", ["toolDecrBrushH.png"], None, None)
    @GuiCommandListDecorator(2, "Decrease brush size", "Decrease brush size", ["toolDecrBrushHW.png"], None, None)
    @GuiCommandListDecorator(3, "Increase brush width", "Increase brush width", ["toolIncrBrushW.png"], None, None)
    @GuiCommandListDecorator(4, "Increase brush height", "Increase brush height", ["toolIncrBrushH.png"], None, None)
    @GuiCommandListDecorator(5, "Increase brush size", "Increase brush size", ["toolIncrBrushHW.png"], None, None)
    def canvasBrushSize(self, f, dimension, incrFlag):
        def canvasBrushSize_(event):
            if (dimension < 2) and not incrFlag:
                if self.parentCanvas.brushSize[dimension] > 1:
                    self.parentCanvas.brushSize[dimension] -= 1
                    self.update(brushSize=self.parentCanvas.brushSize)
            elif (dimension < 2) and incrFlag:
                self.parentCanvas.brushSize[dimension] += 1
                self.update(brushSize=self.parentCanvas.brushSize)
            elif dimension == 2:
                [self.canvasBrushSize(f, dimension_, incrFlag)(None) for dimension_ in [0, 1]]
        setattr(canvasBrushSize_, "attrDict", f.attrList[dimension + (0 if not incrFlag else 3)])
        return canvasBrushSize_
    # }}}
    # {{{ canvasCanvasSize(self, f, dimension, incrFlag)
    @GuiCommandListDecorator(0, "Decrease canvas height", "Decrease canvas height", ["toolDecrCanvasH.png"], None, None)
    @GuiCommandListDecorator(1, "Decrease canvas width", "Decrease canvas width", ["toolDecrCanvasW.png"], None, None)
    @GuiCommandListDecorator(2, "Decrease canvas size", "Decrease canvas size", ["toolDecrCanvasHW.png"], None, None)
    @GuiCommandListDecorator(3, "Increase canvas height", "Increase canvas height", ["toolIncrCanvasH.png"], None, None)
    @GuiCommandListDecorator(4, "Increase canvas width", "Increase canvas width", ["toolIncrCanvasW.png"], None, None)
    @GuiCommandListDecorator(5, "Increase canvas size", "Increase canvas size", ["toolIncrCanvasHW.png"], None, None)
    def canvasCanvasSize(self, f, dimension, incrFlag):
        def canvasCanvasSize_(event):
            if (dimension < 2) and not incrFlag:
                if dimension == 0:
                    if self.parentCanvas.canvas.size[1] > 1:
                        self.parentCanvas.resize([self.parentCanvas.canvas.size[0], self.parentCanvas.canvas.size[1] - 1])
                elif dimension == 1:
                    if self.parentCanvas.canvas.size[0] > 1:
                        self.parentCanvas.resize([self.parentCanvas.canvas.size[0] - 1, self.parentCanvas.canvas.size[1]])
            elif (dimension < 2) and incrFlag:
                if dimension == 0:
                    self.parentCanvas.resize([self.parentCanvas.canvas.size[0], self.parentCanvas.canvas.size[1] + 1])
                elif dimension == 1:
                    self.parentCanvas.resize([self.parentCanvas.canvas.size[0] + 1, self.parentCanvas.canvas.size[1]])
            elif dimension == 2:
                [self.canvasCanvasSize(f, dimension_, incrFlag)(None) for dimension_ in [0, 1]]
        setattr(canvasCanvasSize_, "attrDict", f.attrList[dimension + (0 if not incrFlag else 3)])
        return canvasCanvasSize_
    # }}}
    # {{{ canvasColour(self, f, idx)
    @GuiSelectDecorator(0, "Colour #00", "Colour #00 (Bright White)", None, None, False)
    @GuiSelectDecorator(1, "Colour #01", "Colour #01 (Black)", None, None, False)
    @GuiSelectDecorator(2, "Colour #02", "Colour #02 (Blue)", None, None, False)
    @GuiSelectDecorator(3, "Colour #03", "Colour #03 (Green)", None, None, False)
    @GuiSelectDecorator(4, "Colour #04", "Colour #04 (Red)", None, None, False)
    @GuiSelectDecorator(5, "Colour #05", "Colour #05 (Light Red)", None, None, False)
    @GuiSelectDecorator(6, "Colour #06", "Colour #06 (Pink)", None, None, False)
    @GuiSelectDecorator(7, "Colour #07", "Colour #07 (Yellow)", None, None, False)
    @GuiSelectDecorator(8, "Colour #08", "Colour #08 (Light Yellow)", None, None, False)
    @GuiSelectDecorator(9, "Colour #09", "Colour #09 (Light Green)", None, None, False)
    @GuiSelectDecorator(10, "Colour #10", "Colour #10 (Cyan)", None, None, False)
    @GuiSelectDecorator(11, "Colour #11", "Colour #11 (Light Cyan)", None, None, False)
    @GuiSelectDecorator(12, "Colour #12", "Colour #12 (Light Blue)", None, None, False)
    @GuiSelectDecorator(13, "Colour #13", "Colour #13 (Light Pink)", None, None, False)
    @GuiSelectDecorator(14, "Colour #14", "Colour #14 (Grey)", None, None, False)
    @GuiSelectDecorator(15, "Colour #15", "Colour #15 (Light Grey)", None, None, False)
    def canvasColour(self, f, idx):
        def canvasColour_(event):
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
    @GuiSelectDecorator(0, "Transparent colour", "Transparent colour", None, None, False)
    def canvasColourAlpha(self, f, idx):
        def canvasColourAlpha_(event):
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
    @GuiCommandDecorator("Copy", "&Copy", ["", wx.ART_COPY], None, False)
    def canvasCopy(self, event):
        pass
    # }}}
    # {{{ canvasCut(self, event)
    @GuiCommandDecorator("Cut", "Cu&t", ["", wx.ART_CUT], None, False)
    def canvasCut(self, event):
        pass
    # }}}
    # {{{ canvasDelete(self, event)
    @GuiCommandDecorator("Delete", "De&lete", ["", wx.ART_DELETE], None, False)
    def canvasDelete(self, event):
        pass
    # }}}
    # {{{ canvasPaste(self, event)
    @GuiCommandDecorator("Paste", "&Paste", ["", wx.ART_PASTE], None, False)
    def canvasPaste(self, event):
        pass
    # }}}
    # {{{ canvasRedo(self, event)
    @GuiCommandDecorator("Redo", "&Redo", ["", wx.ART_REDO], [wx.ACCEL_CTRL, ord("Y")], False)
    def canvasRedo(self, event):
        self.parentCanvas.dispatchDeltaPatches(self.parentCanvas.canvas.journal.popRedo())
        self.update(size=self.parentCanvas.canvas.size, undoLevel=self.parentCanvas.canvas.journal.patchesUndoLevel)
    # }}}
    # {{{ canvasUndo(self, event)
    @GuiCommandDecorator("Undo", "&Undo", ["", wx.ART_UNDO], [wx.ACCEL_CTRL, ord("Z")], False)
    def canvasUndo(self, event):
        self.parentCanvas.dispatchDeltaPatches(self.parentCanvas.canvas.journal.popUndo())
        self.update(size=self.parentCanvas.canvas.size, undoLevel=self.parentCanvas.canvas.journal.patchesUndoLevel)
    # }}}

    #
    # __init__(self)
    def __init__(self):
        self.menus = (
            ("&Edit",
                self.canvasUndo, self.canvasRedo, NID_MENU_SEP,
                self.canvasCut, self.canvasCopy, self.canvasPaste,
                self.canvasDelete, NID_MENU_SEP,
                self.canvasCanvasSize(self.canvasCanvasSize, 1, True), self.canvasCanvasSize(self.canvasCanvasSize, 1, False), self.canvasCanvasSize(self.canvasCanvasSize, 0, True), self.canvasCanvasSize(self.canvasCanvasSize, 0, False), NID_MENU_SEP,
                self.canvasCanvasSize(self.canvasCanvasSize, 2, True), self.canvasCanvasSize(self.canvasCanvasSize, 2, False), NID_MENU_SEP,
                self.canvasBrushSize(self.canvasBrushSize, 0, True), self.canvasBrushSize(self.canvasBrushSize, 0, False), self.canvasBrushSize(self.canvasBrushSize, 1, True), self.canvasBrushSize(self.canvasBrushSize, 1, False), NID_MENU_SEP,
                self.canvasBrushSize(self.canvasBrushSize, 2, True), self.canvasBrushSize(self.canvasBrushSize, 2, False), NID_MENU_SEP,
                self.canvasBrush(self.canvasBrush, 0), NID_MENU_SEP,
                self.canvasAssetsWindowHide, self.canvasAssetsWindowShow,
            ),
        )
        self.toolBars = ()

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
