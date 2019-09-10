#!/usr/bin/env python3
#
# RoarClient.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Canvas import Canvas
from GuiCanvasInterface import GuiCanvasInterface
from GuiCanvasWxBackend import GuiCanvasWxBackend
from GuiFrame import GuiFrame, NID_TOOLBAR_HSEP
from RoarCanvasWindow import RoarCanvasWindow

from glob import glob
import os, random, sys

class RoarClient(GuiFrame):
    # {{{ _getIconPathName(self)
    def _getIconPathName(self):
        iconPathNames = glob(os.path.join("assets", "images", "logo*.bmp"))
        return iconPathNames[random.randint(0, len(iconPathNames) - 1)]
    # }}}
    # {{{ _initToolBitmaps(self, toolBars)
    def _initToolBitmaps(self, toolBars):
        basePathName = os.path.join(os.path.dirname(sys.argv[0]), "assets", "images")
        for toolBar in toolBars:
            for toolBarItem in [i for i in toolBar if i != NID_TOOLBAR_HSEP]:
                toolBarItem.attrDict["icon"] = self.loadBitmap(basePathName, toolBarItem.attrDict["icon"])
    # }}}

    # {{{ onChar(self, event)
    def onChar(self, event):
        self.canvasPanel.onKeyboardInput(event)
    # }}}
    # {{{ onMenu(self, event)
    def onMenu(self, event):
        eventId = event.GetId(); self.itemsById[eventId](self.canvasPanel.interface, event);
    # }}}
    # {{{ onMouseWheel(self, event)
    def onMouseWheel(self, event):
        self.canvasPanel.GetEventHandler().ProcessEvent(event)
    # }}}

    #
    # __init__(self, parent, defaultCanvasPos=(0, 75), defaultCanvasSize=(100, 30), defaultCellSize=(7, 14), size=(840, 630), title=""): initialisation method
    def __init__(self, parent, defaultCanvasPos=(0, 75), defaultCanvasSize=(100, 30), defaultCellSize=(7, 14), size=(840, 630), title=""):
        super().__init__(self._getIconPathName(), size, parent, title)
        self.canvas = Canvas(defaultCanvasSize)
        self.canvasPanel = RoarCanvasWindow(GuiCanvasWxBackend, self.canvas, defaultCellSize, GuiCanvasInterface, self.panelSkin, self, defaultCanvasPos, defaultCellSize, defaultCanvasSize)
        self.loadAccels(self.canvasPanel.interface.accels)
        self.loadMenus(self.canvasPanel.interface.menus)
        self._initToolBitmaps(self.canvasPanel.interface.toolBars)
        self.loadToolBars(self.canvasPanel.interface.toolBars)

        self.canvasPanel.interface.canvasNew(None)
        self.canvasPanel.interface.canvasTool(self.canvasPanel.interface.canvasTool, 5)(self.canvasPanel.interface, None)
        self.canvasPanel.interface.update(brushSize=self.canvasPanel.brushSize, colours=self.canvasPanel.brushColours)
        self.addWindow(self.canvasPanel, expand=True)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
