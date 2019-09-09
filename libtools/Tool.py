#!/usr/bin/env python3
#
# Tool.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

class Tool():
    parentCanvas = None

    # {{{ onKeyboardEvent(self, brushColours, brushSize, dispatchFn, eventDc, keyChar, keyModifiers, mapPoint, viewRect):
    def onKeyboardEvent(self, brushColours, brushSize, dispatchFn, eventDc, keyChar, keyModifiers, mapPoint, viewRect):
        pass
    # }}}
    # {{{ onMouseEvent(self, brushColours, brushSize, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def onMouseEvent(self, brushColours, brushSize, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        pass
    # }}}

    #
    # __init__(self, parentCanvas): initialisation method
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
