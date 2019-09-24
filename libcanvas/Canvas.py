#!/usr/bin/env python3
#
# Canvas.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from CanvasExportStore import CanvasExportStore
from CanvasImportStore import CanvasImportStore
from CanvasJournal import CanvasJournal

class Canvas():
    def _commitPatch(self, patch):
        self.map[patch[1]][patch[0]] = patch[2:]

    def dispatchPatch(self, isCursor, patch, commitUndo=True):
        if (patch[0] >= self.size[0]) or (patch[1] >= self.size[1]):
            return False
        else:
            patchDeltaCell = self.map[patch[1]][patch[0]]; patchDelta = [*patch[0:2], *patchDeltaCell];
            if isCursor:
                self.journal.pushCursor(patchDelta)
            else:
                if commitUndo:
                    self.journal.begin(); self.journal.updateCurrentDeltas(patch, patchDelta); self.journal.end();
                self._commitPatch(patch)
            return True

    def dispatchPatchSingle(self, isCursor, patch, commitUndo=True):
        if (patch[0] >= self.size[0]) or (patch[1] >= self.size[1]):
            return False
        else:
            patchDeltaCell = self.map[patch[1]][patch[0]]; patchDelta = [*patch[0:2], *patchDeltaCell];
            if isCursor:
                self.journal.pushCursor(patchDelta)
            else:
                if commitUndo:
                    self.journal.updateCurrentDeltas(patch, patchDelta)
                self._commitPatch(patch)
            return True

    def resize(self, newSize, commitUndo=True):
        if newSize != self.size:
            if self.map == None:
                self.map, oldSize = [], [0, 0]
            else:
                oldSize = self.size
            deltaSize = [b - a for a, b in zip(oldSize, newSize)]
            self.journal.resetCursor()
            if commitUndo:
                self.journal.begin()
                undoPatches, redoPatches = ["resize", *oldSize], ["resize", *newSize]
                self.journal.updateCurrentDeltas(redoPatches, undoPatches)
            if deltaSize[0] < 0:
                for numRow in range(oldSize[1]):
                    if commitUndo:
                        for numCol in range((oldSize[0] + deltaSize[0]), oldSize[0]):
                            self.journal.updateCurrentDeltas(None, [numCol, numRow, *self.map[numRow][numCol]])
                    del self.map[numRow][-1:(deltaSize[0]-1):-1]
            else:
                for numRow in range(oldSize[1]):
                    self.map[numRow].extend([[1, 1, 0, " "]] * deltaSize[0])
                    for numNewCol in range(oldSize[0], newSize[0]):
                        if commitUndo:
                            self.journal.updateCurrentDeltas([numNewCol, numRow, 1, 1, 0, " "], None)
                        self.dispatchPatch(False, [numNewCol, numRow, 1, 1, 0, " "], False)
            if deltaSize[1] < 0:
                if commitUndo:
                    for numRow in range((oldSize[1] + deltaSize[1]), oldSize[1]):
                        for numCol in range(oldSize[0] + deltaSize[0]):
                            self.journal.updateCurrentDeltas(None, [numCol, numRow, *self.map[numRow][numCol]])
                del self.map[-1:(deltaSize[1]-1):-1]
            else:
                for numNewRow in range(oldSize[1], newSize[1]):
                    self.map.extend([[[1, 1, 0, " "]] * newSize[0]])
                    for numNewCol in range(newSize[0]):
                        if commitUndo:
                            self.journal.updateCurrentDeltas([numNewCol, numNewRow, 1, 1, 0, " "], None)
                        self.dispatchPatch(False, [numNewCol, numNewRow, 1, 1, 0, " "], False)
            self.size = newSize
            if commitUndo:
                self.journal.end()
            return True
        else:
            return False

    def update(self, newSize, newCanvas=None):
        for numRow in range(self.size[1]):
            for numCol in range(self.size[0]):
                if  (newCanvas != None)         \
                and (numRow < len(newCanvas))   \
                and (numCol < len(newCanvas[numRow])):
                    self._commitPatch([numCol, numRow, *newCanvas[numRow][numCol]])

    def __init__(self, size):
        self.dirtyCursor, self.map, self.size = False, None, size
        self.exportStore, self.importStore, self.journal = CanvasExportStore(), CanvasImportStore(), CanvasJournal()

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
