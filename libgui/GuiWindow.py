#!/usr/bin/env python3
#
# GuiWindow.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

import wx

class GuiWindow(wx.ScrolledWindow):
    # {{{ _updateScrollBars(self)
    def _updateScrollBars(self):
        clientSize = self.GetClientSize()
        if (self.size[0] > clientSize[0]) or (self.size[1] > clientSize[1]):
            self.scrollFlag = True; super().SetVirtualSize(self.size);
        elif self.scrollFlag    \
        and  ((self.size[0] <= clientSize[0]) or (self.size[1] <= clientSize[1])):
            self.scrollFlag = False; super().SetVirtualSize((0, 0));
    # }}}

    # {{{ onClose(self, event)
    def onClose(self, event):
        self.Destroy()
    # }}}
    # {{{ onKeyboardInput(self, event)
    def onKeyboardInput(self, event):
        return False
    # }}}
    # {{{ onLeaveWindow(self, event)
    def onLeaveWindow(self, event):
        event.Skip()
    # }}}
    # {{{ onMouseInput(self, event)
    def onMouseInput(self, event):
        return False
    # }}}
    # {{{ onPaint(self, event)
    def onPaint(self, event):
        event.Skip()
    # }}}
    # {{{ onScroll(self, event)
    def onScroll(self, event):
        event.Skip()
    # }}}
    # {{{ onSize(self, event)
    def onSize(self, event):
        self._updateScrollBars(); event.Skip();
    # }}}
    # {{{ resize(self, newSize)
    def resize(self, newSize):
        self.size = newSize; self._updateScrollBars();
        self.SetMinSize(self.size); self.SetSize(wx.DefaultCoord, wx.DefaultCoord, *self.size);
        curWindow = self
        while curWindow != None:
            curWindow.Layout(); curWindow = curWindow.GetParent();
    # }}}

    #
    # __init__(self, parent, pos, scrollStep, size, style=0): initialisation method
    def __init__(self, parent, pos, scrollStep, size, style=0):
        super().__init__(parent, pos=pos, size=size, style=style)
        self.pos, self.scrollFlag, self.scrollStep, self.size = pos, False, scrollStep, size
        for eventType, f in (
                (wx.EVT_CHAR, self.onKeyboardInput), (wx.EVT_CLOSE, self.onClose), (wx.EVT_LEAVE_WINDOW, self.onLeaveWindow),
                (wx.EVT_LEFT_DOWN, self.onMouseInput), (wx.EVT_MOTION, self.onMouseInput), (wx.EVT_PAINT, self.onPaint),
                (wx.EVT_RIGHT_DOWN, self.onMouseInput), (wx.EVT_SCROLLWIN_LINEDOWN, self.onScroll), (wx.EVT_SCROLLWIN_LINEUP, self.onScroll),
                (wx.EVT_SIZE, self.onSize)):
            self.Bind(eventType, f)
        self.SetScrollRate(*self.scrollStep); self._updateScrollBars();

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
