#!/bin/sh
#
# MiRCARTToPngFiles.sh -- convert ASCII(s) w/ mIRC control codes to monospaced PNG(s) (for EFnet #MiRCART)
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

for FNAME in "${@}"; do
    ./MiRCARTToPngFile.py "${FNAME}" "${FNAME%.txt}.png";
done;

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
