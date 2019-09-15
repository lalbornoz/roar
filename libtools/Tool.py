#!/usr/bin/env python3
#
# Tool.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

class Tool(object):
    # {{{ onKeyboardEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, keyChar, keyModifiers, mapPoint, viewRect)
    def onKeyboardEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, keyChar, keyModifiers, mapPoint, viewRect):
        return False, False
    # }}}
    # {{{ onMouseEvent(self, brushColours, brushSize, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def onMouseEvent(self, brushColours, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        return False, False
    # }}}

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
