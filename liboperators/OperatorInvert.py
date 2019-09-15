#!/usr/bin/env python3
#
# OperatorInvert.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Operator import Operator

class OperatorInvert(Operator):
    name = "Invert colours"

    #
    # apply(self, region)
    def apply(self, region):
        for numRow in range(len(region)):
            for numCol in range(len(region[numRow])):
                region[numRow][numCol][0:2] = [(~r & (16 - 1) if r > 0 else r) for r in region[numRow][numCol][0:2]]
        return region

    # __init__(self, *args): initialisation method
    def __init__(self, *args):
        pass

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
