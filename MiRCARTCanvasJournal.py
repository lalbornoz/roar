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
                patch[2:] = self.parentCanvas._getMapCell([patch[0], patch[1]])
                self.parentCanvas.onJournalUpdate(True,  \
                    (patch[0:2]), patch, eventDc, tmpDc, (0, 0))
            self.patchesTmp = []
    # }}}
    # {{{ _pushTmp(self, atPoint, patch): XXX
    def _pushTmp(self, absMapPoint):
        self.patchesTmp.append([*absMapPoint, None, None, None])
    # }}}
    # {{{ _pushUndo(self, atPoint, patch): XXX
    def _pushUndo(self, atPoint, patch, mapItem):
        if self.patchesUndoLevel > 0:
            del self.patchesUndo[0:self.patchesUndoLevel]
            self.patchesUndoLevel = 0
        absMapPoint = self._relMapPointToAbsMapPoint((patch[0], patch[1]), atPoint)
        self.patchesUndo.insert(0, (                                                \
            (absMapPoint[0], absMapPoint[1], mapItem[0], mapItem[1], mapItem[2]),   \
            (absMapPoint[0], absMapPoint[1], patch[2], patch[3], patch[4])))
    # }}}
    # {{{ _relMapPointToAbsMapPoint(self, relMapPoint, atPoint): XXX
    def _relMapPointToAbsMapPoint(self, relMapPoint, atPoint):
        return (atPoint[0] + relMapPoint[0], atPoint[1] + relMapPoint[1])
    # }}}
    # {{{ merge(self, mapPatches, eventDc, tmpDc, atPoint): XXX
    def merge(self, mapPatches, eventDc, tmpDc, atPoint):
        for mapPatch in mapPatches:
            mapPatchTmp = mapPatch[0]
            if mapPatchTmp:
                self._popTmp(eventDc, tmpDc)
            for patch in mapPatch[1]:
                absMapPoint = self._relMapPointToAbsMapPoint(patch[0:2], atPoint)
                mapItem = self.parentCanvas._getMapCell(absMapPoint)
                if mapPatchTmp:
                    self._pushTmp(absMapPoint)
                    self.parentCanvas.onJournalUpdate(mapPatchTmp,  \
                        absMapPoint, patch, eventDc, tmpDc, atPoint)
                elif mapItem != patch[2:5]:
                    self._pushUndo(atPoint, patch, mapItem)
                    self.parentCanvas.onJournalUpdate(mapPatchTmp,  \
                        absMapPoint, patch, eventDc, tmpDc, atPoint)
    # }}}
    # {{{ redo(self): XXX
    def redo(self):
        if self.patchesUndoLevel > 0:
            self.patchesUndoLevel -= 1
            redoPatch = self.patchesUndo[self.patchesUndoLevel][1]
            self.parentCanvas.onJournalUpdate(False,        \
                (redoPatch[0:2]), redoPatch, None, None, (0, 0))
            return True
        else:
            return False
    # }}}
    # {{{ undo(self): XXX
    def undo(self):
        if self.patchesUndo[self.patchesUndoLevel] != None:
            undoPatch = self.patchesUndo[self.patchesUndoLevel][0]
            self.patchesUndoLevel += 1
            self.parentCanvas.onJournalUpdate(False,        \
                (undoPatch[0:2]), undoPatch, None, None, (0, 0))
            return True
        else:
            return False
    # }}}

    #
    # __init__(self, parentCanvas): initialisation method
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas
        self.patchesTmp = []
        self.patchesUndo = [None]; self.patchesUndoLevel = 0;

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
