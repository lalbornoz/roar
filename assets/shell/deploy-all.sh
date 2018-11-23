#!/bin/sh
#

msgf() {
	local _fmt="${1}"; shift;
	printf "%s >>> ${_fmt}\n" "$(date +"%d-%^b-%Y %H:%M:%S")" "${@}";
};

usage() {
	echo "usage: ${0} [-h] [-v]" >&2;
	echo "       -h.........: show this screen" >&2;
	echo "       -v.........: be verbose" >&2;
};

main() {
	local _cmd="" _build="" _opt="" _vflag=0;
	while getopts hv _opt; do
	case "${_opt}" in
	h) usage; exit 0; ;;
	v) _vflag=1; ;;
	*) usage; exit 1; ;;
	esac; done;
	shift $((${OPTIND}-1));
	for _build in cordoba nwjs www; do
		msgf "Deploying ${_build}...";
		if [ "${_vflag:-0}" -eq 0 ]; then
			./assets/shell/deploy-${_build}.sh "${@}";
		else
			./assets/shell/deploy-${_build}.sh -v "${@}";
		fi;
		msgf "Deployed ${_build}.";
	done;
};

set -o errexit -o noglob;
main "${@}";

# vim:foldmethod=marker sw=8 ts=8 tw=120
