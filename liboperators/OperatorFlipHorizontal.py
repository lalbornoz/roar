#!/usr/bin/env python3
#
# OperatorFlipHorizontal.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Operator import Operator

# TODO <https://en.wikipedia.org/wiki/Box_Drawing_(Unicode_block)>

class OperatorFlipHorizontal(Operator):
    name = "Flip horizontally"
    flipPairs = {
        "/":"\\", "╱":"╲",
        "▀":"▄", "▁":"▔", "▖":"▘", "▗":"▝",
        "▙":"▛", "▚":"▞", "▜":"▟",
    }

    def apply(self, region):
        region.reverse()
        for numRow in range(len(region)):
            for numCol in range(len(region[numRow])):
                if region[numRow][numCol][3] in self.flipPairs:
                    region[numRow][numCol][3] = self.flipPairs[region[numRow][numCol][3]]
        return region

    def __init__(self, *args):
        for flipPairKey in list(self.flipPairs.keys()):
            self.flipPairs[self.flipPairs[flipPairKey]] = flipPairKey

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
