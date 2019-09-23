#!/usr/bin/env python3
#
# RtlPlatform.py
# Copyright (c) 2018, 2019 Lucía Andrea Illanes Albornoz <lucia@luciaillanes.de>
# This project is licensed under the terms of the MIT licence.
#

import os, platform

def getLocalConfPathName(*args):
    vname = "LOCALAPPDATA" if platform.system() == "Windows" else "HOME"
    return os.path.join(os.getenv(vname), "roar", *args)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
