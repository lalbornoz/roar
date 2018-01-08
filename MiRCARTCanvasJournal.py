#!/usr/bin/env python3
#
# MiRCARTCanvasJournal.py -- XXX
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

class MiRCARTCanvasJournal():
    """XXX"""
    parentCanvas = None
    patchesTmp = patchesUndo = patchesUndoLevel = None

    # {{{ _popTmp(self, eventDc, tmpDc): XXX
    def _popTmp(self, eventDc, tmpDc):
        if self.patchesTmp:
            for patch in self.patchesTmp:
                self.parentCanvas.onJournalUpdate(True,             \
                    patch[0], patch, eventDc, tmpDc, (0, 0), True)
            self.patchesTmp = []
    # }}}
    # {{{ _pushTmp(self, atPoint): XXX
    def _pushTmp(self, atPoint):
        self.patchesTmp.append([atPoint, None, None, None])
    # }}}
    # {{{ _pushUndo(self, atPoint, patches): XXX
    def _pushUndo(self, atPoint, patches):
        if self.patchesUndoLevel > 0:
            del self.patchesUndo[0:self.patchesUndoLevel]
            self.patchesUndoLevel = 0
        patchesUndo = []
        for patch in patches:
            patchesUndo.append([            \
                [patch[0], *patch[0][1:]],  \
                [patch[0], *patch[1][1:]]])
        if len(patchesUndo) > 0:
            self.patchesUndo.insert(0, patchesUndo)
    # }}}
    # {{{ merge(self, mapPatches, eventDc, tmpDc, atPoint): XXX
    def merge(self, mapPatches, eventDc, tmpDc, atPoint):
        patchesUndo = []
        for mapPatch in mapPatches:
            mapPatchTmp = mapPatch[0]
            if mapPatchTmp:
                self._popTmp(eventDc, tmpDc)
            for patch in mapPatch[1]:
                if patch[0][0] >= self.parentCanvas.canvasSize[0]   \
                or patch[0][1] >= self.parentCanvas.canvasSize[1]:
                    continue
                elif mapPatchTmp:
                    self._pushTmp(patch[0])
                    self.parentCanvas.onJournalUpdate(mapPatchTmp,  \
                        patch[0], patch, eventDc, tmpDc, (0, 0))
                else:
                    patchUndo =                                     \
                    self.parentCanvas.onJournalUpdate(mapPatchTmp,  \
                        patch[0], patch, eventDc, tmpDc, (0, 0), True)
                    patchesUndo.append([patchUndo, patch])
        if len(patchesUndo) > 0:
            self._pushUndo(atPoint, patchesUndo)
    # }}}
    # {{{ redo(self): XXX
    def redo(self):
        if self.patchesUndoLevel > 0:
            self.patchesUndoLevel -= 1
            for patch in self.patchesUndo[self.patchesUndoLevel]:
                self.parentCanvas.onJournalUpdate(False,    \
                    patch[1][0], patch[1], None, None, (0, 0))
            return True
        else:
            return False
    # }}}
    # {{{ reset(self): XXX
    def reset(self):
        self.patchesTmp = []; self.patchesUndo = [None]; self.patchesUndoLevel = 0;
    # }}}
    # {{{ resetCursor(self, eventDc, tmpDc): XXX
    def resetCursor(self, eventDc, tmpDc):
        if len(self.patchesTmp):
            self._popTmp(eventDc, tmpDc)
            self.patchesTmp = []
    # }}}
    # {{{ undo(self): XXX
    def undo(self):
        if self.patchesUndo[self.patchesUndoLevel] != None:
            patches = self.patchesUndo[self.patchesUndoLevel]
            self.patchesUndoLevel += 1
            for patch in patches:
                self.parentCanvas.onJournalUpdate(False,    \
                    patch[0][0], patch[0], None, None, (0, 0))
            return True
        else:
            return False
    # }}}

    #
    # __init__(self, parentCanvas): initialisation method
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas; self.reset();

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
