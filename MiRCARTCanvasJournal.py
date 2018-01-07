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
    # {{{ _pushTmp(self, atPoint, patch): XXX
    def _pushTmp(self, absMapPoint):
        self.patchesTmp.append([absMapPoint, None, None, None])
    # }}}
    # {{{ _pushUndo(self, atPoint, patchUndo, patchRedo): XXX
    def _pushUndo(self, atPoint, patchUndo, patchRedo):
        if self.patchesUndoLevel > 0:
            del self.patchesUndo[0:self.patchesUndoLevel]
            self.patchesUndoLevel = 0
        absMapPoint = self._relMapPointToAbsMapPoint(patchUndo[0], atPoint)
        self.patchesUndo.insert(0, [    \
            [absMapPoint, *patchUndo[1:]], [absMapPoint, *patchRedo[1:]]])
    # }}}
    # {{{ _relMapPointToAbsMapPoint(self, relMapPoint, atPoint): XXX
    def _relMapPointToAbsMapPoint(self, relMapPoint, atPoint):
        return [a+b for a,b in zip(atPoint, relMapPoint)]
    # }}}
    # {{{ merge(self, mapPatches, eventDc, tmpDc, atPoint): XXX
    def merge(self, mapPatches, eventDc, tmpDc, atPoint):
        for mapPatch in mapPatches:
            mapPatchTmp = mapPatch[0]
            if mapPatchTmp:
                self._popTmp(eventDc, tmpDc)
            for patch in mapPatch[1]:
                absMapPoint = self._relMapPointToAbsMapPoint(patch[0], atPoint)
                if absMapPoint[0] >= self.parentCanvas.canvasSize[0]    \
                or absMapPoint[1] >= self.parentCanvas.canvasSize[1]:
                    continue
                elif mapPatchTmp:
                    self._pushTmp(absMapPoint)
                    self.parentCanvas.onJournalUpdate(mapPatchTmp,      \
                        absMapPoint, patch, eventDc, tmpDc, atPoint)
                else:
                    patchUndo =                                         \
                    self.parentCanvas.onJournalUpdate(mapPatchTmp,      \
                        absMapPoint, patch, eventDc, tmpDc, atPoint, True)
                    self._pushUndo(atPoint, patchUndo, patch)
    # }}}
    # {{{ redo(self): XXX
    def redo(self):
        if self.patchesUndoLevel > 0:
            self.patchesUndoLevel -= 1
            redoPatch = self.patchesUndo[self.patchesUndoLevel][1]
            self.parentCanvas.onJournalUpdate(False,    \
                redoPatch[0], redoPatch, None, None, (0, 0))
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
            undoPatch = self.patchesUndo[self.patchesUndoLevel][0]
            self.patchesUndoLevel += 1
            self.parentCanvas.onJournalUpdate(False,    \
                undoPatch[0], undoPatch, None, None, (0, 0))
            return True
        else:
            return False
    # }}}

    #
    # __init__(self, parentCanvas): initialisation method
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas; self.reset();

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
