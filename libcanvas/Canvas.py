#!/usr/bin/env python3
#
# Canvas.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from CanvasExportStore import CanvasExportStore
from CanvasImportStore import CanvasImportStore

class Canvas():
    def _commitPatch(self, patch):
        self.map[patch[1]][patch[0]] = patch[2:]

    def applyPatch(self, patch, commitUndo=True):
        if (patch[0] >= self.size[0]) or (patch[1] >= self.size[1]):
            return False
        else:
            patchDeltaCell = self.map[patch[1]][patch[0]]; patchDelta = [*patch[0:2], *patchDeltaCell];
            if commitUndo:
                self.updateCurrentDeltas(patch, patchDelta)
            self._commitPatch(patch)
            return True

    def begin(self):
        deltaItem = [[], []]; self.patchesUndo.insert(self.patchesUndoLevel, deltaItem);

    def end(self):
        if self.patchesUndo[self.patchesUndoLevel] == [[], []]:
            del self.patchesUndo[self.patchesUndoLevel]
        else:
            if self.patchesUndoLevel > 0:
                del self.patchesUndo[:self.patchesUndoLevel]; self.patchesUndoLevel = 0;

    def popCursor(self, reset=True):
        patchesCursor = []
        if len(self.patchesCursor):
            patchesCursor = self.patchesCursor
            if reset:
                self.resetCursor()
        return patchesCursor

    def popUndo(self, redo=False):
        patches = []
        if not redo:
            if self.patchesUndo[self.patchesUndoLevel] != None:
                patches = self.patchesUndo[self.patchesUndoLevel][0]; self.patchesUndoLevel += 1;
        else:
            if self.patchesUndoLevel > 0:
                self.patchesUndoLevel -= 1; patches = self.patchesUndo[self.patchesUndoLevel][1];
        return patches

    def pushCursor(self, patches):
        self.patchesCursor = patches

    def resetCursor(self):
        self.patchesCursor = []

    def resetUndo(self):
        if self.patchesUndo != None:
            self.patchesUndo.clear()
        self.patchesUndo = [None]; self.patchesUndoLevel = 0;

    def resize(self, brushColours, newSize, commitUndo=True):
        newCells = []
        if newSize != self.size:
            if self.map == None:
                self.map, oldSize = [], [0, 0]
            else:
                oldSize = self.size
            deltaSize = [b - a for a, b in zip(oldSize, newSize)]
            if commitUndo:
                self.begin()
                undoPatches, redoPatches = ["resize", *oldSize], ["resize", *newSize]
                self.updateCurrentDeltas(redoPatches, undoPatches)
            if deltaSize[0] < 0:
                for numRow in range(oldSize[1]):
                    if commitUndo:
                        for numCol in range((oldSize[0] + deltaSize[0]), oldSize[0]):
                            self.updateCurrentDeltas(None, [numCol, numRow, *self.map[numRow][numCol]])
                    del self.map[numRow][-1:(deltaSize[0]-1):-1]
            else:
                for numRow in range(oldSize[1]):
                    self.map[numRow].extend([[*brushColours, 0, " "]] * deltaSize[0])
                    for numNewCol in range(oldSize[0], newSize[0]):
                        if commitUndo:
                            self.updateCurrentDeltas([numNewCol, numRow, *brushColours, 0, " "], None)
                        newCells += [[numNewCol, numRow, *brushColours, 0, " "]]
                        self.applyPatch([numNewCol, numRow, *brushColours, 0, " "], False)
            if deltaSize[1] < 0:
                if commitUndo:
                    for numRow in range((oldSize[1] + deltaSize[1]), oldSize[1]):
                        for numCol in range(oldSize[0] + deltaSize[0]):
                            self.updateCurrentDeltas(None, [numCol, numRow, *self.map[numRow][numCol]])
                del self.map[-1:(deltaSize[1]-1):-1]
            else:
                for numNewRow in range(oldSize[1], newSize[1]):
                    self.map.extend([[[*brushColours, 0, " "]] * newSize[0]])
                    for numNewCol in range(newSize[0]):
                        if commitUndo:
                            self.updateCurrentDeltas([numNewCol, numNewRow, *brushColours, 0, " "], None)
                        newCells += [[numNewCol, numNewRow, *brushColours, 0, " "]]
                        self.applyPatch([numNewCol, numNewRow, *brushColours, 0, " "], False)
            self.size = newSize
            if commitUndo:
                self.end()
            return True, newCells
        else:
            return False, newCells

    def update(self, newSize, newCanvas=None):
        for numRow in range(self.size[1]):
            for numCol in range(self.size[0]):
                if  (newCanvas != None) \
                and (numRow < len(newCanvas)) and (numCol < len(newCanvas[numRow])):
                    self._commitPatch([numCol, numRow, *newCanvas[numRow][numCol]])

    def updateCurrentDeltas(self, redoPatches, undoPatches):
        self.patchesUndo[self.patchesUndoLevel][0].append(undoPatches)
        self.patchesUndo[self.patchesUndoLevel][1].append(redoPatches)

    def __del__(self):
        self.resetCursor(); self.resetUndo();

    def __init__(self, size):
        self.exportStore, self.importStore, self.map, self.size = CanvasExportStore(), CanvasImportStore(), None, size
        self.patchesCursor, self.patchesUndo, self.patchesUndoLevel = [], [None], 0

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
