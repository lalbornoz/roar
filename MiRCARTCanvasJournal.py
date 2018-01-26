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
    patchesCursor = patchesUndo = patchesUndoLevel = None

    # {{{ popCursor(self): XXX
    def popCursor(self):
        if len(self.patchesCursor):
            patchesCursor = self.patchesCursor
            self.patchesCursor = []
            return patchesCursor
        else:
            return []
    # }}}
    # {{{ popRedo(self): XXX
    def popRedo(self):
        if self.patchesUndoLevel > 0:
            self.patchesUndoLevel -= 1
            patches = self.patchesUndo[self.patchesUndoLevel]
            return patches[1]
        else:
            return []
    # }}}
    # {{{ popUndo(self): XXX
    def popUndo(self):
        if self.patchesUndo[self.patchesUndoLevel] != None:
            patches = self.patchesUndo[self.patchesUndoLevel]
            self.patchesUndoLevel += 1
            return patches[0]
        else:
            return []
    # }}}
    # {{{ pushCursor(self, patches): XXX
    def pushCursor(self, patches):
        self.patchesCursor.append(patches)
    # }}}
    # {{{ pushDeltas(self, undoPatches, redoPatches): XXX
    def pushDeltas(self, undoPatches, redoPatches):
        if self.patchesUndoLevel > 0:
            del self.patchesUndo[0:self.patchesUndoLevel]
            self.patchesUndoLevel = 0
        deltaItem = [undoPatches, redoPatches]
        self.patchesUndo.insert(0, deltaItem)
        return deltaItem
    # }}}
    # {{{ resetCursor(self): XXX
    def resetCursor(self):
        if self.patchesCursor != None:
            self.patchesCursor.clear()
        self.patchesCursor = []
    # }}}
    # {{{ resetUndo(self): XXX
    def resetUndo(self):
        if self.patchesUndo != None:
            self.patchesUndo.clear()
        self.patchesUndo = [None]; self.patchesUndoLevel = 0;
    # }}}
    # {{{ updateCurrentDeltas(self, undoPatches, redoPatches): XXX
    def updateCurrentDeltas(self, undoPatches, redoPatches):
        self.patchesUndo[0][0].append(undoPatches)
        self.patchesUndo[0][1].append(redoPatches)
    # }}}

    # {{{ __del__(self): destructor method
    def __del__(self):
        self.resetCursor(); self.resetUndo();
    # }}}

    #
    # __init__(self): initialisation method
    def __init__(self):
        self.resetCursor(); self.resetUndo();

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
