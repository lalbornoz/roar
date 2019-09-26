#!/usr/bin/env python3
#
# ToolText.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Tool import Tool
import re, string, wx

class ToolText(Tool):
    name = "Text"
    arabicCombiningRegEx = r'^[\u064B-\u065F\uFE70-\uFE72\uFE74\uFE76-\uFE7F]+$'
    arabicRegEx = r'^[\u0621-\u063A\u0640-\u064A]+$'
    rtlRegEx = r'^[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]+$'

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

    def _processKeyChar(self, brushColours, brushPos, canvas, keyChar, keyModifiers):
        patches, rc = [], False
        if   (ord(keyChar) != wx.WXK_NONE)                          \
        and  (not keyChar in set("\t\n\v\f\r"))                     \
        and  ((ord(keyChar) >= 32) if ord(keyChar) < 127 else True):
            patches += [[*brushPos, *brushColours, 0, keyChar]]
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
            rc = True
        return rc, patches

    def onKeyboardEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, keyChar, keyCode, keyModifiers, mapPoint):
        patches, patchesCursor, rc = [], [], False
        if re.match(self.arabicCombiningRegEx, keyChar):
            rc = True
        elif keyCode == wx.WXK_CONTROL_V:
            rc = True
            if  wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT))  \
            and wx.TheClipboard.Open():
                inBuffer = wx.TextDataObject()
                if wx.TheClipboard.GetData(inBuffer):
                    for inBufferChar in list(inBuffer.GetText()):
                        if not re.match(self.arabicCombiningRegEx, inBufferChar):
                            rc_, patches_ = self._processKeyChar(brushColours, brushPos, canvas, inBufferChar, 0)
                            patches += patches_
                            rc = True if rc_ else rc
                    if rc:
                        patchesCursor += [[*brushPos, *brushColours, 0, "_"]]
                wx.TheClipboard.Close()
            else:
                rc, error = False, "Clipboard does not contain text data and/or cannot be opened"
        elif keyCode == wx.WXK_BACK:
            if ((brushPos[0] + 1) >= canvas.size[0]):
                lastBrushPos = [0, brushPos[1] - 1] if brushPos[1] > 0 else [0, 0]
            else:
                lastBrushPos = [brushPos[0] + 1, brushPos[1]]
            if not self._checkRtl(canvas, lastBrushPos, None):
                patches += [[*brushPos, *brushColours, 0, " "]]
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
            rc = True; patchesCursor += [[*brushPos, *brushColours, 0, "_"]];
        elif keyCode == wx.WXK_RETURN:
            if brushPos[1] < (canvas.size[1] - 1):
                brushPos[0], brushPos[1] = 0, brushPos[1] + 1
            else:
                brushPos[0], brushPos[1] = 0, 0
            rc = True; patchesCursor += [[*brushPos, *brushColours, 0, "_"]];
        else:
            rc, patches_ = self._processKeyChar(brushColours, brushPos, canvas, keyChar, keyModifiers)
            patches += patches_
            if rc:
                patchesCursor += [[*brushPos, *brushColours, 0, "_"]]
        return rc, patches, patchesCursor

    def onMouseEvent(self, atPoint, brushColours, brushPos, brushSize, canvas, keyModifiers, mapPoint, mouseDragging, mouseLeftDown, mouseRightDown):
        if mouseLeftDown or mouseRightDown:
            brushPos[0], brushPos[1] = atPoint[0], atPoint[1]
        return True, None, [[*brushPos, *brushColours, 0, "_"]]

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
