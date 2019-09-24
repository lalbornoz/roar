#!/usr/bin/env python3
#
# GuiWindow.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import wx

class GuiWindow(wx.ScrolledWindow):
    def _updateScrollBars(self):
        if self.size != None:
            clientSize = self.GetClientSize()
            if (self.size[0] > clientSize[0]) or (self.size[1] > clientSize[1]):
                self.scrollFlag = True; super().SetVirtualSize(self.size);
            elif self.scrollFlag    \
            and  ((self.size[0] <= clientSize[0]) or (self.size[1] <= clientSize[1])):
                self.scrollFlag = False; super().SetVirtualSize((0, 0));

    def onClose(self, event):
        self.Destroy()

    def onEnterWindow(self, event):
        event.Skip()

    def onKeyboardInput(self, event):
        return False

    def onLeaveWindow(self, event):
        event.Skip()

    def onMouseInput(self, event):
        return False

    def onPaint(self, event):
        event.Skip()

    def onScroll(self, event):
        event.Skip()

    def onSize(self, event):
        self._updateScrollBars(); event.Skip();

    def resize(self, newSize):
        self.size = newSize; self._updateScrollBars();
        self.SetMinSize(self.size); self.SetSize(wx.DefaultCoord, wx.DefaultCoord, *self.size);
        self.SetMinSize(self.parent.GetSize()); self.SetSize(wx.DefaultCoord, wx.DefaultCoord, *self.parent.GetSize())
        curWindow = self
        while curWindow != None:
            curWindow.Layout(); curWindow = curWindow.GetParent();

    def __init__(self, parent, pos, scrollStep, style=0):
        super().__init__(parent, pos=pos, style=style) if style != 0 else super().__init__(parent, pos=pos)
        self.parent = parent
        self.pos, self.scrollFlag, self.scrollStep, self.size = pos, False, scrollStep, None
        for eventType, f in (
                (wx.EVT_CHAR, self.onKeyboardInput), (wx.EVT_CLOSE, self.onClose), (wx.EVT_ENTER_WINDOW, self.onEnterWindow),
                (wx.EVT_LEAVE_WINDOW, self.onLeaveWindow), (wx.EVT_LEFT_DOWN, self.onMouseInput), (wx.EVT_MOTION, self.onMouseInput),
                (wx.EVT_PAINT, self.onPaint), (wx.EVT_RIGHT_DOWN, self.onMouseInput), (wx.EVT_SCROLLWIN_LINEDOWN, self.onScroll),
                (wx.EVT_SCROLLWIN_LINEUP, self.onScroll), (wx.EVT_SIZE, self.onSize)):
            self.Bind(eventType, f)
        self.SetScrollRate(*self.scrollStep); self._updateScrollBars();

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
