#!/usr/bin/env python3
#
# Rtl.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

import statistics, time

timeState = [None, None, 0, []]

def flatten(l):
    return [li for l_ in l for li in l_]

def timePrint(pfx):
    timeState[0] = time.time() if timeState[0] == None else timeState[0]
    t1 = time.time(); td = t1 - timeState[0]
    if td > 0:
        timeState[1] = td if timeState[1] == None else min(td, timeState[1])
        timeState[2] = max(td, timeState[2])
        timeState[3] += [td]
        print("{} took {:.4f} ms (min: {:.4f} max: {:.4f} avg: {:.4f})".format(pfx, td * 1000, timeState[1] * 1000, timeState[2] * 1000, statistics.mean(timeState[3]) * 1000))

def timeReset():
    timeState = [None, None, 0, []]

def timeStart():
    timeState[0] = time.time()

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
