#!/bin/sh
#
# MiRCARTCheckLineLengths.py -- check mIRC art line lengths
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT licence.
#

for FNAME in "${@}"; do
	FNAME_LINES="$(wc -l "${FNAME}" | awk '{print $1}')";
	for FNAME_LINE in $(seq "${FNAME_LINES}"); do
		printf "%-5d %-5d %s\n"					\
			"$(sed -n "${FNAME_LINE}p" "${FNAME}" | wc -c)"	\
			"${FNAME_LINE}" "${FNAME}";
	done;
done | sort -nk1;

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
