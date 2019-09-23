#!/usr/bin/env python3
#
# CanvasJournal.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

class CanvasJournal():
    def begin(self):
        deltaItem = [[], []]; self.patchesUndo.insert(self.patchesUndoLevel, deltaItem);

    def end(self):
        if self.patchesUndo[self.patchesUndoLevel] == [[], []]:
            del self.patchesUndo[self.patchesUndoLevel]
        else:
            if self.patchesUndoLevel > 0:
                del self.patchesUndo[:self.patchesUndoLevel]; self.patchesUndoLevel = 0;

    def popCursor(self):
        if len(self.patchesCursor):
            patchesCursor = self.patchesCursor; self.patchesCursor = [];
            return patchesCursor
        else:
            return []

    def popRedo(self):
        if self.patchesUndoLevel > 0:
            self.patchesUndoLevel -= 1; patches = self.patchesUndo[self.patchesUndoLevel];
            return patches[1]
        else:
            return []

    def popUndo(self):
        if self.patchesUndo[self.patchesUndoLevel] != None:
            patches = self.patchesUndo[self.patchesUndoLevel]; self.patchesUndoLevel += 1;
            return patches[0]
        else:
            return []

    def pushCursor(self, patches):
        self.patchesCursor.append(patches)

    def resetCursor(self):
        if self.patchesCursor != None:
            self.patchesCursor.clear()
        self.patchesCursor = []

    def resetUndo(self):
        if self.patchesUndo != None:
            self.patchesUndo.clear()
        self.patchesUndo = [None]; self.patchesUndoLevel = 0;

    def updateCurrentDeltas(self, redoPatches, undoPatches):
        self.patchesUndo[self.patchesUndoLevel][0].append(undoPatches)
        self.patchesUndo[self.patchesUndoLevel][1].append(redoPatches)

    def __del__(self):
        self.resetCursor(); self.resetUndo();

    #
    # __init__(self): initialisation method
    def __init__(self):
        self.patchesCursor, self.patchesUndo, self. patchesUndoLevel = None, None, None
        self.resetCursor(); self.resetUndo();

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
