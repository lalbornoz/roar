#!/bin/sh
#

PACKAGE_NAME="MiRCART-www";
RELEASE_DEPS="cpio find rm sed zip";
RELEASES_DNAME="releases";

msgf() {
	local _fmt="${1}"; shift;
	printf "%s >>> ${_fmt}\n" "$(date +"%d-%^b-%Y %H:%M:%S")" "${@}";
};

deploy() {
	local _vflag="${1}" _release_fname="" _release_dname="" _release_version="";

	_release_version="$(sed -n '/^\s*<title>/s/^\s*<title>MiRCART v\([0-9.]\+\)<\/title>\s*$/\1/p' index.html)";
	_release_dname="${RELEASES_DNAME}/${PACKAGE_NAME}-${_release_version}";
	_release_fname="${_release_dname}.zip";

	find -L .					\
		-mindepth 1				\
		-not -path "./${RELEASES_DNAME}/*"	\
		-not -path "./${RELEASES_DNAME}"	\
		-not -name '*.sw*'			\
		-not -name "${0##*/}"			|\
			cpio --quiet -dLmp "${_release_dname}";
	cd "${RELEASES_DNAME}";
	if [ "${_vflag:-0}" -eq 0 ]; then
		zip -9 -r "${_release_fname##${RELEASES_DNAME}/}" "${_release_dname##${RELEASES_DNAME}/}" >/dev/null;
	else
		zip -9 -r "${_release_fname##${RELEASES_DNAME}/}" "${_release_dname##${RELEASES_DNAME}/}";
	fi;
	cd "${OLDPWD}"; rm -fr "${_release_dname}";
};

usage() {
	echo "usage: ${0} [-h] [-v]" >&2;
	echo "       -h.........: show this screen" >&2;
	echo "       -v.........: be verbose" >&2;
};

main() {
	local _cmd="" _opt="" _vflag=0;
	while getopts hv _opt; do
	case "${_opt}" in
	h) usage; exit 0; ;;
	v) _vflag=1; ;;
	*) usage; exit 1; ;;
	esac; done;
	shift $((${OPTIND}-1));
	for _cmd in ${RELEASE_DEPS}; do
		if ! which "${_cmd}" >/dev/null; then
			echo "error: missing prerequisite command \`${_cmd}'";
			exit 1;
		fi;
	done;
	msgf "Building release...";
	if [ "${_vflag:-0}" -eq 0 ]; then
		deploy "${_vflag}" >/dev/null;
	else
		deploy "${_vflag}";
	fi;
	msgf "Built release.";
};

set -o errexit -o noglob;
main "${@}";

# vim:foldmethod=marker sw=8 ts=8 tw=120
