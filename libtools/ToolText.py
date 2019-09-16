#!/usr/bin/env python3
#
# ToolText.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool
import re, string, wx

class ToolText(Tool):
    name = "Text"
    rtlRegEx = r'^[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]+$'

    # {{{ _processKeyChar(self, brushColours, brushPos, canvas, dispatchFn, eventDc, keyChar, keyModifiers, viewRect)
    def _processKeyChar(self, brushColours, brushPos, canvas, dispatchFn, eventDc, keyChar, keyModifiers, viewRect):
        if (ord(keyChar) != wx.WXK_NONE)                            \
        and  (not keyChar in set("\t\n\v\f\r"))                     \
        and  ((ord(keyChar) >= 32) if ord(keyChar) < 127 else True) \
        and  (keyModifiers in (wx.MOD_NONE, wx.MOD_SHIFT)):
            dispatchFn(eventDc, False, [*brushPos, *brushColours, 0, keyChar], viewRect);
            if not re.match(self.rtlRegEx, keyChar):
                if brushPos[0] < (canvas.size[0] - 1):
                    brushPos[0] += 1
                elif brushPos[1] < (canvas.size[1] - 1):
                    brushPos[0], brushPos[1] = 0, brushPos[1] + 1
                else:
                    brushPos[0], brushPos[1] = 0, 0
            else:
                if brushPos[0] > 0:
                    brushPos[0] -= 1
                elif brushPos[1] > 0:
                    brushPos[0], brushPos[1] = canvas.size[0] - 1, brushPos[1] - 1
                else:
                    brushPos[0], brushPos[1] = canvas.size[0] - 1, canvas.size[1] - 1
            rc, dirty = True, True
        else:
            rc, dirty = False, False
        return rc, dirty
    # }}}

    #
    # onKeyboardEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyChar, keyCode, keyModifiers, mapPoint, viewRect)
    def onKeyboardEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyChar, keyCode, keyModifiers, mapPoint, viewRect):
        if keyCode == wx.WXK_CONTROL_V:
            rc, dirty = True, False
            if  wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT))  \
            and wx.TheClipboard.Open():
                inBuffer = wx.TextDataObject()
                if wx.TheClipboard.GetData(inBuffer):
                    for inBufferChar in list(inBuffer.GetText()):
                        rc_, dirty_ = self._processKeyChar(brushColours, brushPos, canvas, dispatchFn, eventDc, inBufferChar, 0, viewRect)
                        rc = True if rc_ else rc; dirty = True if dirty_ else dirty;
                    if rc:
                        dispatchFn(eventDc, True, [*brushPos, *brushColours, 0, "_"], viewRect)
                wx.TheClipboard.Close()
            else:
                rc, error = False, "Clipboard does not contain text data and/or cannot be opened"
        elif keyCode == wx.WXK_BACK:
            if brushPos[0] > 0:
                brushPos[0] -= 1
            elif brushPos[1] > 0:
                brushPos[0], brushPos[1] = canvas.size[0] - 1, brushPos[1] - 1
            else:
                brushPos[0], brushPos[1] = canvas.size[0] - 1, canvas.size[1] - 1
            rc, dirty = True, False; dispatchFn(eventDc, True, [*brushPos, *brushColours, 0, "_"], viewRect);
        elif keyCode == wx.WXK_RETURN:
            if brushPos[1] < (canvas.size[1] - 1):
                brushPos[0], brushPos[1] = 0, brushPos[1] + 1
            else:
                brushPos[0], brushPos[1] = 0, 0
            rc, dirty = True, False; dispatchFn(eventDc, True, [*brushPos, *brushColours, 0, "_"], viewRect);
        else:
            rc, dirty = self._processKeyChar(brushColours, brushPos, canvas, dispatchFn, eventDc, keyChar, keyModifiers, viewRect)
            if rc:
                dispatchFn(eventDc, True, [*brushPos, *brushColours, 0, "_"], viewRect)
        return rc, dirty

    #
    # onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect)
    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, dispatchFn, eventDc, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown, viewRect):
        if mouseLeftDown or mouseRightDown:
            brushPos[0], brushPos[1] = atPoint[0], atPoint[1]
        dispatchFn(eventDc, True, [*brushPos, *brushColours, 0, "_"], viewRect)
        return True, False

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
