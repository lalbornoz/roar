#!/usr/bin/env python3
#
# RoarCanvasCommandsEdit.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from GuiFrame import GuiCommandDecorator, GuiCommandListDecorator, GuiSelectDecorator, NID_MENU_SEP
import wx

class RoarCanvasCommandsEdit():
    @GuiCommandDecorator("Hide assets window", "Hide assets window", ["toolHideAssetsWindow.png"], None, False)
    def canvasAssetsWindowHide(self, event):
        self.parentFrame.assetsWindow.Show(False)
        self.parentFrame.menuItemsById[self.canvasAssetsWindowHide.attrDict["id"]].Enable(False)
        self.parentFrame.menuItemsById[self.canvasAssetsWindowShow.attrDict["id"]].Enable(True)
        toolBar = self.parentFrame.toolBarItemsById[self.canvasAssetsWindowHide.attrDict["id"]][0]
        toolBar.EnableTool(self.canvasAssetsWindowHide.attrDict["id"], False)
        toolBar.EnableTool(self.canvasAssetsWindowShow.attrDict["id"], True)
        toolBar.Refresh()

    @GuiCommandDecorator("Show assets window", "Show assets window", ["toolShowAssetsWindow.png"], None, False)
    def canvasAssetsWindowShow(self, event):
        self.parentFrame.assetsWindow.Show(True)
        self.parentFrame.menuItemsById[self.canvasAssetsWindowHide.attrDict["id"]].Enable(True)
        self.parentFrame.menuItemsById[self.canvasAssetsWindowShow.attrDict["id"]].Enable(False)
        toolBar = self.parentFrame.toolBarItemsById[self.canvasAssetsWindowHide.attrDict["id"]][0]
        toolBar.EnableTool(self.canvasAssetsWindowHide.attrDict["id"], True)
        toolBar.EnableTool(self.canvasAssetsWindowShow.attrDict["id"], False)
        toolBar.Refresh()

    @GuiSelectDecorator(0, "Solid brush", "Solid brush", None, None, True)
    def canvasBrush(self, f, idx):
        def canvasBrush_(self, event):
            pass
        setattr(canvasBrush_, "attrDict", f.attrList[idx])
        setattr(canvasBrush_, "isSelect", True)
        return canvasBrush_

    @GuiCommandListDecorator(0, "Decrease brush width", "Decrease brush width", ["toolDecrBrushW.png"], None, None)
    @GuiCommandListDecorator(1, "Decrease brush height", "Decrease brush height", ["toolDecrBrushH.png"], None, None)
    @GuiCommandListDecorator(2, "Decrease brush size", "Decrease brush size", ["toolDecrBrushHW.png"], [wx.ACCEL_CTRL, ord("-")], None)
    @GuiCommandListDecorator(3, "Increase brush width", "Increase brush width", ["toolIncrBrushW.png"], None, None)
    @GuiCommandListDecorator(4, "Increase brush height", "Increase brush height", ["toolIncrBrushH.png"], None, None)
    @GuiCommandListDecorator(5, "Increase brush size", "Increase brush size", ["toolIncrBrushHW.png"], [wx.ACCEL_CTRL, ord("+")], None)
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
            viewRect = self.parentCanvas.GetViewStart()
            eventDc = self.parentCanvas.backend.getDeviceContext(self.parentCanvas.GetClientSize(), self.parentCanvas, viewRect)
            self.parentCanvas.applyTool(eventDc, True, None, None, None, self.parentCanvas.brushPos, False, False, False, self.currentTool, viewRect, force=True)
        setattr(canvasBrushSize_, "attrDict", f.attrList[dimension + (0 if not incrFlag else 3)])
        return canvasBrushSize_

    @GuiCommandListDecorator(0, "Decrease canvas height", "Decrease canvas height", ["toolDecrCanvasH.png"], None, None)
    @GuiCommandListDecorator(1, "Decrease canvas width", "Decrease canvas width", ["toolDecrCanvasW.png"], None, None)
    @GuiCommandListDecorator(2, "Decrease canvas size", "Decrease canvas size", ["toolDecrCanvasHW.png"], [wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("-")], None)
    @GuiCommandListDecorator(3, "Increase canvas height", "Increase canvas height", ["toolIncrCanvasH.png"], None, None)
    @GuiCommandListDecorator(4, "Increase canvas width", "Increase canvas width", ["toolIncrCanvasW.png"], None, None)
    @GuiCommandListDecorator(5, "Increase canvas size", "Increase canvas size", ["toolIncrCanvasHW.png"], [wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("+")], None)
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

    @GuiSelectDecorator(0, "Colour #00", "Colour #00 (Bright White)", None, [wx.ACCEL_CTRL, ord("0")], False)
    @GuiSelectDecorator(1, "Colour #01", "Colour #01 (Black)", None, [wx.ACCEL_CTRL, ord("1")], False)
    @GuiSelectDecorator(2, "Colour #02", "Colour #02 (Blue)", None, [wx.ACCEL_CTRL, ord("2")], False)
    @GuiSelectDecorator(3, "Colour #03", "Colour #03 (Green)", None, [wx.ACCEL_CTRL, ord("3")], False)
    @GuiSelectDecorator(4, "Colour #04", "Colour #04 (Red)", None, [wx.ACCEL_CTRL, ord("4")], False)
    @GuiSelectDecorator(5, "Colour #05", "Colour #05 (Light Red)", None, [wx.ACCEL_CTRL, ord("5")], False)
    @GuiSelectDecorator(6, "Colour #06", "Colour #06 (Pink)", None, [wx.ACCEL_CTRL, ord("6")], False)
    @GuiSelectDecorator(7, "Colour #07", "Colour #07 (Yellow)", None, [wx.ACCEL_CTRL, ord("7")], False)
    @GuiSelectDecorator(8, "Colour #08", "Colour #08 (Light Yellow)", None, [wx.ACCEL_CTRL, ord("8")], False)
    @GuiSelectDecorator(9, "Colour #09", "Colour #09 (Light Green)", None, [wx.ACCEL_CTRL, ord("9")], False)
    @GuiSelectDecorator(10, "Colour #10", "Colour #10 (Cyan)", None, [wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("0")], False)
    @GuiSelectDecorator(11, "Colour #11", "Colour #11 (Light Cyan)", None, [wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("1")], False)
    @GuiSelectDecorator(12, "Colour #12", "Colour #12 (Light Blue)", None, [wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("2")], False)
    @GuiSelectDecorator(13, "Colour #13", "Colour #13 (Light Pink)", None, [wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("3")], False)
    @GuiSelectDecorator(14, "Colour #14", "Colour #14 (Grey)", None, [wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("4")], False)
    @GuiSelectDecorator(15, "Colour #15", "Colour #15 (Light Grey)", None, [wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("5")], False)
    def canvasColour(self, f, idx):
        def canvasColour_(event):
            if event.GetEventType() == wx.wxEVT_TOOL:
                self.parentCanvas.brushColours[0] = idx
            elif event.GetEventType() == wx.wxEVT_TOOL_RCLICKED:
                self.parentCanvas.brushColours[1] = idx
            self.update(colours=self.parentCanvas.brushColours)
            viewRect = self.parentCanvas.GetViewStart()
            eventDc = self.parentCanvas.backend.getDeviceContext(self.parentCanvas.GetClientSize(), self.parentCanvas, viewRect)
            self.parentCanvas.applyTool(eventDc, True, None, None, None, self.parentCanvas.brushPos, False, False, False, self.currentTool, viewRect, force=True)
        setattr(canvasColour_, "attrDict", f.attrList[idx])
        setattr(canvasColour_, "isSelect", True)
        return canvasColour_

    @GuiSelectDecorator(0, "Transparent colour", "Transparent colour", None, [wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("6")], False)
    def canvasColourAlpha(self, f, idx):
        def canvasColourAlpha_(event):
            if event.GetEventType() == wx.wxEVT_TOOL:
                self.parentCanvas.brushColours[0] = -1
            elif event.GetEventType() == wx.wxEVT_TOOL_RCLICKED:
                self.parentCanvas.brushColours[1] = -1
            self.update(colours=self.parentCanvas.brushColours)
            viewRect = self.parentCanvas.GetViewStart()
            eventDc = self.parentCanvas.backend.getDeviceContext(self.parentCanvas.GetClientSize(), self.parentCanvas, viewRect)
            self.parentCanvas.applyTool(eventDc, True, None, None, None, self.parentCanvas.brushPos, False, False, False, self.currentTool, viewRect, force=True)
        setattr(canvasColourAlpha_, "attrDict", f.attrList[idx])
        setattr(canvasColourAlpha_, "isSelect", True)
        return canvasColourAlpha_

    @GuiSelectDecorator(0, "Transparent colour", "Transparent colour", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT | wx.ACCEL_SHIFT, ord("6")], False)
    def canvasColourAlphaBackground(self, f, idx):
        def canvasColourAlphaBackground_(event):
            self.parentCanvas.brushColours[1] = -1
            self.update(colours=self.parentCanvas.brushColours)
            viewRect = self.parentCanvas.GetViewStart()
            eventDc = self.parentCanvas.backend.getDeviceContext(self.parentCanvas.GetClientSize(), self.parentCanvas, viewRect)
            self.parentCanvas.applyTool(eventDc, True, None, None, None, self.parentCanvas.brushPos, False, False, False, self.currentTool, viewRect, force=True)
        setattr(canvasColourAlphaBackground_, "attrDict", f.attrList[idx])
        setattr(canvasColourAlphaBackground_, "isSelect", True)
        return canvasColourAlphaBackground_

    @GuiSelectDecorator(0, "Colour #00", "Colour #00 (Bright White)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT, ord("0")], False)
    @GuiSelectDecorator(1, "Colour #01", "Colour #01 (Black)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT, ord("1")], False)
    @GuiSelectDecorator(2, "Colour #02", "Colour #02 (Blue)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT, ord("2")], False)
    @GuiSelectDecorator(3, "Colour #03", "Colour #03 (Green)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT, ord("3")], False)
    @GuiSelectDecorator(4, "Colour #04", "Colour #04 (Red)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT, ord("4")], False)
    @GuiSelectDecorator(5, "Colour #05", "Colour #05 (Light Red)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT, ord("5")], False)
    @GuiSelectDecorator(6, "Colour #06", "Colour #06 (Pink)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT, ord("6")], False)
    @GuiSelectDecorator(7, "Colour #07", "Colour #07 (Yellow)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT, ord("7")], False)
    @GuiSelectDecorator(8, "Colour #08", "Colour #08 (Light Yellow)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT, ord("8")], False)
    @GuiSelectDecorator(9, "Colour #09", "Colour #09 (Light Green)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT, ord("9")], False)
    @GuiSelectDecorator(10, "Colour #10", "Colour #10 (Cyan)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT | wx.ACCEL_SHIFT, ord("0")], False)
    @GuiSelectDecorator(11, "Colour #11", "Colour #11 (Light Cyan)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT | wx.ACCEL_SHIFT, ord("1")], False)
    @GuiSelectDecorator(12, "Colour #12", "Colour #12 (Light Blue)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT | wx.ACCEL_SHIFT, ord("2")], False)
    @GuiSelectDecorator(13, "Colour #13", "Colour #13 (Light Pink)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT | wx.ACCEL_SHIFT, ord("3")], False)
    @GuiSelectDecorator(14, "Colour #14", "Colour #14 (Grey)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT | wx.ACCEL_SHIFT, ord("4")], False)
    @GuiSelectDecorator(15, "Colour #15", "Colour #15 (Light Grey)", None, [wx.ACCEL_CTRL | wx.ACCEL_ALT | wx.ACCEL_SHIFT, ord("5")], False)
    def canvasColourBackground(self, f, idx):
        def canvasColourBackground_(event):
            self.parentCanvas.brushColours[1] = idx
            self.update(colours=self.parentCanvas.brushColours)
            viewRect = self.parentCanvas.GetViewStart()
            eventDc = self.parentCanvas.backend.getDeviceContext(self.parentCanvas.GetClientSize(), self.parentCanvas, viewRect)
            self.parentCanvas.applyTool(eventDc, True, None, None, None, self.parentCanvas.brushPos, False, False, False, self.currentTool, viewRect, force=True)
        setattr(canvasColourBackground_, "attrDict", f.attrList[idx])
        setattr(canvasColourBackground_, "isSelect", True)
        return canvasColourBackground_

    @GuiCommandDecorator("Flip colours", "Flip colours", ["toolColoursFlip.png"], [wx.ACCEL_CTRL, ord("I")], True)
    def canvasColoursFlip(self, event):
        self.parentCanvas.brushColours = [self.parentCanvas.brushColours[1], self.parentCanvas.brushColours[0]]
        self.update(colours=self.parentCanvas.brushColours)
        viewRect = self.parentCanvas.GetViewStart()
        eventDc = self.parentCanvas.backend.getDeviceContext(self.parentCanvas.GetClientSize(), self.parentCanvas, viewRect)
        self.parentCanvas.applyTool(eventDc, True, None, None, None, self.parentCanvas.brushPos, False, False, False, self.currentTool, viewRect, force=True)

    @GuiCommandDecorator("Copy", "&Copy", ["", wx.ART_COPY], None, False)
    def canvasCopy(self, event):
        pass

    @GuiCommandDecorator("Cut", "Cu&t", ["", wx.ART_CUT], None, False)
    def canvasCut(self, event):
        pass

    @GuiCommandDecorator("Delete", "De&lete", ["", wx.ART_DELETE], None, False)
    def canvasDelete(self, event):
        pass

    @GuiCommandDecorator("Paste", "&Paste", ["", wx.ART_PASTE], None, False)
    def canvasPaste(self, event):
        pass

    @GuiCommandDecorator("Redo", "&Redo", ["", wx.ART_REDO], [wx.ACCEL_CTRL, ord("Y")], False)
    def canvasRedo(self, event):
        eventDc = self.parentCanvas.backend.getDeviceContext(self.parentCanvas.GetClientSize(), self.parentCanvas, self.parentCanvas.GetViewStart())
        self.parentCanvas.dispatchDeltaPatches(self.parentCanvas.canvas.journal.popRedo(), eventDc=eventDc, forceDirtyCursor=True)
        self.update(size=self.parentCanvas.canvas.size, undoLevel=self.parentCanvas.canvas.journal.patchesUndoLevel)

    @GuiCommandDecorator("Undo", "&Undo", ["", wx.ART_UNDO], [wx.ACCEL_CTRL, ord("Z")], False)
    def canvasUndo(self, event):
        eventDc = self.parentCanvas.backend.getDeviceContext(self.parentCanvas.GetClientSize(), self.parentCanvas, self.parentCanvas.GetViewStart())
        self.parentCanvas.dispatchDeltaPatches(self.parentCanvas.canvas.journal.popUndo(), eventDc=eventDc, forceDirtyCursor=True)
        self.update(size=self.parentCanvas.canvas.size, undoLevel=self.parentCanvas.canvas.journal.patchesUndoLevel)

    def __init__(self):
        self.accels = (
            (self.canvasColourBackground(self.canvasColourBackground, 0), self.canvasColourBackground(self.canvasColourBackground, 1), self.canvasColourBackground(self.canvasColourBackground, 2), self.canvasColourBackground(self.canvasColourBackground, 3), self.canvasColourBackground(self.canvasColourBackground, 4), self.canvasColourBackground(self.canvasColourBackground, 5), self.canvasColourBackground(self.canvasColourBackground, 6), self.canvasColourBackground(self.canvasColourBackground, 7), self.canvasColourBackground(self.canvasColourBackground, 8), self.canvasColourBackground(self.canvasColourBackground, 9), self.canvasColourBackground(self.canvasColourBackground, 10), self.canvasColourBackground(self.canvasColourBackground, 11), self.canvasColourBackground(self.canvasColourBackground, 12), self.canvasColourBackground(self.canvasColourBackground, 13), self.canvasColourBackground(self.canvasColourBackground, 14), self.canvasColourBackground(self.canvasColourBackground, 15), self.canvasColourAlphaBackground(self.canvasColourAlphaBackground, 0),),
        )
        self.menus = (
            ("&Edit",
                self.canvasUndo, self.canvasRedo, NID_MENU_SEP,
                self.canvasCut, self.canvasCopy, self.canvasPaste,
                self.canvasDelete, NID_MENU_SEP,
                ("Brush size", self.canvasBrushSize(self.canvasBrushSize, 0, True), self.canvasBrushSize(self.canvasBrushSize, 0, False), self.canvasBrushSize(self.canvasBrushSize, 1, True), self.canvasBrushSize(self.canvasBrushSize, 1, False), NID_MENU_SEP,
                    self.canvasBrushSize(self.canvasBrushSize, 2, True), self.canvasBrushSize(self.canvasBrushSize, 2, False),),
                ("Canvas size", self.canvasCanvasSize(self.canvasCanvasSize, 1, True), self.canvasCanvasSize(self.canvasCanvasSize, 1, False), self.canvasCanvasSize(self.canvasCanvasSize, 0, True), self.canvasCanvasSize(self.canvasCanvasSize, 0, False), NID_MENU_SEP,
                    self.canvasCanvasSize(self.canvasCanvasSize, 2, True), self.canvasCanvasSize(self.canvasCanvasSize, 2, False),),
                self.canvasColoursFlip,
                NID_MENU_SEP,
                self.canvasBrush(self.canvasBrush, 0), NID_MENU_SEP,
                self.canvasAssetsWindowHide, self.canvasAssetsWindowShow,
            ),
        )
        self.toolBars = ()

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
