#!/usr/bin/env python3
#
# RoarCanvasCommandsOperators.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from OperatorFlipHorizontal import OperatorFlipHorizontal
from OperatorFlipVertical import OperatorFlipVertical
from OperatorInvert import OperatorInvert
from OperatorRotate import OperatorRotate
from OperatorTile import OperatorTile
from GuiFrame import GuiCommandListDecorator
from ToolObject import ToolObject
import copy, wx

class RoarCanvasCommandsOperators():
    # {{{ canvasOperator(self, f, idx)
    @GuiCommandListDecorator(0, "Flip", "&Flip", None, None, None)
    @GuiCommandListDecorator(1, "Flip horizontally", "Flip &horizontally", None, None, None)
    @GuiCommandListDecorator(2, "Invert", "&Invert", None, None, None)
    @GuiCommandListDecorator(3, "Rotate", "&Rotate", None, None, None)
    @GuiCommandListDecorator(4, "Tile", "&Tile", None, None, None)
    def canvasOperator(self, f, idx):
        def canvasOperator_(event):
            self.currentOperator = [OperatorFlipVertical, OperatorFlipHorizontal, OperatorInvert, OperatorRotate, OperatorTile][idx]()
            self.operatorState = None
            self.parentCanvas.applyOperator(self.currentTool, self.parentCanvas.brushPos, None, False, self.currentOperator, self.parentCanvas.GetViewStart())
        setattr(canvasOperator_, "attrDict", f.attrList[idx])
        return canvasOperator_
    # }}}

    #
    # __init__(self)
    def __init__(self):
        self.menus = (
            ("&Operators",
                self.canvasOperator(self.canvasOperator, 0), self.canvasOperator(self.canvasOperator, 1), self.canvasOperator(self.canvasOperator, 2), self.canvasOperator(self.canvasOperator, 3), self.canvasOperator(self.canvasOperator, 4),
            ),
        )
        self.toolBars = ()
        self.currentOperator, self.operatorState = None, None

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=0
