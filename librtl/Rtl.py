#!/usr/bin/env python3
#
# Rtl.py
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

import re

def flatten(l):
    return [li for l_ in l for li in l_]

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key=alphanum_key)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
