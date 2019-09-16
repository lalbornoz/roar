#!/usr/bin/env python3
#
# Tool.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

class Tool(object):
    # {{{ onKeyboardEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyChar, keyCode, keyModifiers, mapPoint, viewRect)
    def onKeyboardEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyChar, keyCode, keyModifiers, mapPoint, viewRect):
        return False, False
    # }}}
    # {{{ onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, dispatchFn, eventDc, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        return False, False
    # }}}

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
