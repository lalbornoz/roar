#!/usr/bin/env python3
#
# OperatorFlipHorizontal.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from Operator import Operator

class OperatorFlipHorizontal(Operator):
    name = "Flip horizontally"

    def apply(self, region):
        region.reverse(); return region;

    def __init__(self, *args):
        pass

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
