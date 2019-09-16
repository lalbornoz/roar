#!/usr/bin/env python3
#
# OperatorFlipVertical.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Operator import Operator

class OperatorFlipVertical(Operator):
    name = "Flip"
    flipPairs = {
        "(":")", ")":"(",
        "/":"\\", "\\":"/",
        "\[":"]", "]":"\[",
        "\{":"\}", "\}":"\{",
        "<":">", ">":"<",
        "`":"'",
    }

    #
    # apply(self, region)
    def apply(self, region):
        for numRow in range(len(region)):
            region[numRow].reverse()
            for numCol in range(len(region[numRow])):
                if region[numRow][numCol][3] in self.flipPairs:
                    region[numRow][numCol][3] = self.flipPairs[region[numRow][numCol][3]]
        return region

    # __init__(self, *args): initialisation method
    def __init__(self, *args):
        pass

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
