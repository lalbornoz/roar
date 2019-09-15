#!/usr/bin/env python3
#
# OperatorFlipVertical.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Operator import Operator

class OperatorFlipVertical(Operator):
    name = "Flip"

    #
    # apply(self, region)
    def apply(self, region):
        for numRow in range(len(region)):
            region[numRow].reverse()
        return region

    # __init__(self, *args): initialisation method
    def __init__(self, *args):
        pass

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
