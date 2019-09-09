#!/usr/bin/env python3
#
# Tool.py
# Copyright (c) 2018, 2019 Lucía Andrea Illanes Albornoz <lucia@luciaillanes.de>
#

class Tool():
    parentCanvas = None

    # {{{ onKeyboardEvent(self, brushColours, brushSize, dispatchFn, eventDc, keyChar, keyModifiers, mapPoint, viewRect)
    def onKeyboardEvent(self, brushColours, brushSize, dispatchFn, eventDc, keyChar, keyModifiers, mapPoint, viewRect):
        return False, False
    # }}}
    # {{{ onMouseEvent(self, brushColours, brushSize, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def onMouseEvent(self, brushColours, brushSize, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        return False, False
    # }}}

    #
    # __init__(self, parentCanvas): initialisation method
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
