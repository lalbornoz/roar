#!/usr/bin/env python3
#
# CanvasJournal.py -- XXX
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

class CanvasJournal():
    """XXX"""

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
        self.patchesCursor, self.patchesUndo, self. patchesUndoLevel = None, None, None
        self.resetCursor(); self.resetUndo();

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
