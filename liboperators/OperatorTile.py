#!/usr/bin/env python3
#
# OperatorTile.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Operator import Operator
import copy

class OperatorTile(Operator):
    name = "Tile"

    def apply2(self, mapPoint, mousePoint, regionOld, region):
        if self.lastPoint == None:
            self.lastPoint = list(mapPoint)
        if self.tileObject == None:
            self.tileObject = copy.deepcopy(region)
        delta = [b - a for a, b in zip(self.lastPoint, mapPoint)]
        if delta[1] > 0:
            for numNewRow in range(delta[1]):
                newRow = copy.deepcopy(self.tileObject[len(region) % len(self.tileObject)])
                if len(newRow) < len(region[0]):
                    for numNewCol in range(len(newRow), len(region[0])):
                        newRow += [list(self.tileObject[len(region) % len(self.tileObject)][numNewCol % len(self.tileObject[len(region) % len(self.tileObject)])])]
                region += [newRow]
        if delta[0] > 0:
            for numRow in range(len(region)):
                for numNewCol in range(len(region[numRow]), len(region[numRow]) + delta[0]):
                    region[numRow] += [list(self.tileObject[numRow % len(self.tileObject)][numNewCol % len(self.tileObject[numRow % len(self.tileObject)])])]
        self.lastPoint = list(mapPoint)
        return region

    def __init__(self, *args):
        self.lastPoint, self.tileObject = None, None

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
