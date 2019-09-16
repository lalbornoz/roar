#!/usr/bin/env python3
#
# ToolText.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool
import re, string, time, wx

class ToolText(Tool):
    name = "Text"
    arabicRegEx = r'^[\u0621-\u063A\u0640-\u064A]+$'
    rtlRegEx = r'^[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]+$'

    # {{{ _checkRtl(self, canvas, brushPos, keyChar)
    def _checkRtl(self, canvas, brushPos, keyChar):
        rtlFlag = False
        if (keyChar != None) and re.match(self.rtlRegEx, keyChar):
            rtlFlag = True
        else:
            lastX, lastY = brushPos[0], brushPos[1]
            while True:
                if canvas.map[lastY][lastX][3] == " ":
                    if (lastX + 1) >= canvas.size[0]:
                        if lastY == 0:
                            break
                        else:
                            lastX, lastY = 0, lastY - 1
                    else:
                        lastX += 1
                elif re.match(self.arabicRegEx, canvas.map[lastY][lastX][3]):
                    rtlFlag = True
                    if (lastX + 1) >= canvas.size[0]:
                        if lastY == 0:
                            break
                        else:
                            lastX, lastY = 0, lastY - 1
                    else:
                        lastX += 1
                else:
                    break
        return rtlFlag
    # }}}
    # {{{ _processKeyChar(self, brushColours, brushPos, canvas, dispatchFn, eventDc, keyChar, keyModifiers, viewRect)
    def _processKeyChar(self, brushColours, brushPos, canvas, dispatchFn, eventDc, keyChar, keyModifiers, viewRect):
        if (ord(keyChar) != wx.WXK_NONE)                            \
        and  (not keyChar in set("\t\n\v\f\r"))                     \
        and  ((ord(keyChar) >= 32) if ord(keyChar) < 127 else True) \
        and  (keyModifiers in (wx.MOD_NONE, wx.MOD_SHIFT)):
            dispatchFn(eventDc, False, [*brushPos, *brushColours, 0, keyChar], viewRect);
            if not self._checkRtl(canvas, brushPos, keyChar):
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
            if ((brushPos[0] + 1) >= canvas.size[0]):
                if brushPos[1] > 0:
                    lastBrushPos = [0, brushPos[1] - 1]
                else:
                    lastBrushPos = [0, 0]
            else:
                lastBrushPos = [brushPos[0] + 1, brushPos[1]]
            if not self._checkRtl(canvas, lastBrushPos, None):
                if brushPos[0] > 0:
                    brushPos[0] -= 1
                elif brushPos[1] > 0:
                    brushPos[0], brushPos[1] = canvas.size[0] - 1, brushPos[1] - 1
                else:
                    brushPos[0], brushPos[1] = canvas.size[0] - 1, canvas.size[1] - 1
            else:
                if brushPos[0] < (canvas.size[0] - 1):
                    brushPos[0] += 1
                elif brushPos[1] > 0:
                    brushPos[0], brushPos[1] = 0, brushPos[1] - 1
                else:
                    brushPos[0], brushPos[1] = canvas.size[0] - 1, 0
            rc, dirty = True, False; dispatchFn(eventDc, False, [*brushPos, *brushColours, 0, " "], viewRect);
            dispatchFn(eventDc, True, [*brushPos, *brushColours, 0, "_"], viewRect);
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
