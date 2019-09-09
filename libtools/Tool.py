#!/usr/bin/env python3
#
# Tool.py 
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

class Tool():
    parentCanvas = None

    # {{{ onKeyboardEvent(self, event, atPoint, brushColours, brushSize, keyChar, dispatchFn, eventDc, viewRect):
    def onKeyboardEvent(self, event, atPoint, brushColours, brushSize, keyChar, dispatchFn, eventDc, viewRect):
        return True
    # }}}
    # {{{ onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc, viewRect)
    def onMouseEvent(self, event, atPoint, brushColours, brushSize, isDragging, isLeftDown, isRightDown, dispatchFn, eventDc, viewRect):
        return ()
    # }}}

    #
    # __init__(self, parentCanvas): initialisation method
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
