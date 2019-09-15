#!/usr/bin/env python3
#
# OperatorFlipHorizontal.py
# Copyright (c) 2018, 2019 Lucía Andrea Illanes Albornoz <lucia@luciaillanes.de>
#

from Operator import Operator

class OperatorFlipHorizontal(Operator):
    name = "Flip horizontally"

    #
    # apply(self, region)
    def apply(self, region):
        region.reverse(); return region;

    # __init__(self, *args): initialisation method
    def __init__(self, *args):
        pass

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
