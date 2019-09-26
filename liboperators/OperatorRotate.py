#!/usr/bin/env python3
#
# OperatorRotate.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Operator import Operator
import math

class OperatorRotate(Operator):
    name = "Rotate"

    def apply2(self, mapPoint, mousePoint, regionOld, region):
        if self.originPoint == None:
            self.originPoint = list(mousePoint)
        delta = [b - a for a, b in zip(self.originPoint, mousePoint)]
        radius = math.sqrt(math.pow(delta[0], 2) + math.pow(delta[1], 2))
        if radius >= 10:
            regionSize = (len(region[0]), len(region))
            theta = math.atan2(-delta[1], delta[0]); cos, sin = math.cos(theta), math.sin(theta);
            for numCol in range(regionSize[0]):
                for numRow in range(regionSize[1]):
                    numRow_, numCol_ = (numRow / regionSize[1]) * 2 - 1, (numCol / regionSize[0]) * 2 - 1
                    b, a = (numCol_ * sin) + (numRow_ * cos), (numCol_ * cos) - (numRow_ * sin)
                    numRow_, numCol_ = int((b + 1) / 2 * regionSize[1]), int((a + 1) / 2 * regionSize[0])
                    if (numRow_ < regionSize[1]) and (numCol_ < regionSize[0]):
                        region[numRow][numCol] = list(regionOld[numRow_][numCol_])
            return region
        else:
            return region

    def __init__(self, *args):
        self.originPoint = None

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
