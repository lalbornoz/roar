#!/bin/sh
#

PACKAGE_NAME="MiRCART-nw";
RELEASE_DEPS="cpio find gunzip rm sed tar unzip wget zip";
NWJS_MANIFEST_FNAME="nwjs.manifest";
NWJS_PLATFORMS="linux-ia32 linux-x64 win-ia32 win-x64";
NWJS_VERSION="0.34.5";
NWJS_SUBDIR="nwjs-v${NWJS_VERSION}-%NWJS_PLATFORM%";
NWJS_URL_linux="https://dl.nwjs.io/v${NWJS_VERSION}/nwjs-v${NWJS_VERSION}-%NWJS_PLATFORM%.tar.gz";
NWJS_URL_win="https://dl.nwjs.io/v${NWJS_VERSION}/nwjs-v${NWJS_VERSION}-%NWJS_PLATFORM%.zip";
RELEASES_DNAME="releases";

extract() {
	local _fname="${1}" _dest_dname="${2}";
	if [ -n "${_fname}" -a -z "${_fname##*.tar.gz}" ]; then
		tar -C "${_dest_dname}" -xpf "${_fname}";
	elif [ -n "${_fname}" -a -z "${_fname##*.zip}" ]; then
		unzip -d "${_dest_dname}" "${_fname}";
	else
		echo "error: file \`${_fname}' is of unknown archive type" >&2; exit 1;
	fi;
};

msgf() {
	local _fmt="${1}"; shift;
	printf "%s >>> ${_fmt}\n" "$(date +"%d-%^b-%Y %H:%M:%S")" "${@}";
};

subst() {
	local _string="${1}" _search="${2}" _replace="${3}" _string_="";
	_string_="${_string%${_search}*}";
	_string_="${_string_}${_replace}"
	_string_="${_string_}${_string#*${_search}}";
	echo "${_string_}";
};

deploy() {
	local _platform="${1}" _vflag="${2}" _nwjs_fname="" _nwjs_subdir="" _nwjs_url=""	\
		_release_fname="" _release_dname="" _release_version="";

	_nwjs_subdir="$(subst "${NWJS_SUBDIR}" "%NWJS_PLATFORM%" "${_platform}")";
	_nwjs_url="$(subst "$(eval echo \"\${NWJS_URL_${_platform%%-*}}\")" "%NWJS_PLATFORM%" "${_platform}")";
	_nwjs_fname="${RELEASES_DNAME}/${_nwjs_url##*/}";
	_release_version="$(sed -n '/^\s*"version":/s/^.*:\s*"\([0-9.]\+\)",\?\s*$/\1/p' package.json)";
	_release_dname="${RELEASES_DNAME}/${PACKAGE_NAME}-release-${_platform}-${_release_version}";
	_release_fname="${_release_dname}.zip";

	trap "rm -fr ${_release_dname}" EXIT HUP INT QUIT PIPE TERM USR1 USR2;
	if [ "${_vflag:-0}" -eq 0 ]; then
		wget -cqO "${_nwjs_fname}" "${_nwjs_url}";
	else
		wget -cO "${_nwjs_fname}" "${_nwjs_url}";
	fi;
	if ! sha256sum --ignore-missing -c --status "${NWJS_MANIFEST_FNAME}"; then
		echo "error: SHA256 sum mismatch for \`${_nwjs_fname}'" >&2; return 1;
	fi;
	rm -rf "${_release_dname}"; mkdir -p "${_release_dname}"; extract "${_nwjs_fname}" "${_release_dname}";

	cd "${_release_dname}/${_nwjs_subdir}";
	find .						\
		-mindepth 1				|\
			cpio --quiet -dmp ..;
	cd "${OLDPWD}";
	rm -fr "${_release_dname}/${_nwjs_subdir}";
	find -L .					\
		-mindepth 1				\
		-not -path "./${RELEASES_DNAME}/*"	\
		-not -path "./${RELEASES_DNAME}"	\
		-not -name '*.sw*'			\
		-not -name "${0##*/}"			\
		-not -name "${NWJS_MANIFEST_FNAME}"	|\
			cpio --quiet -dLmp "${_release_dname}";
	cd "${RELEASES_DNAME}";
	if [ "${_vflag:-0}" -eq 0 ]; then
		zip -9 -r "${_release_fname##${RELEASES_DNAME}/}" "${_release_dname##${RELEASES_DNAME}/}" >/dev/null;
	else
		zip -9 -r "${_release_fname##${RELEASES_DNAME}/}" "${_release_dname##${RELEASES_DNAME}/}";
	fi;
	cd "${OLDPWD}"; rm -fr "${_release_dname}";
	trap - EXIT HUP INT QUIT PIPE TERM USR1 USR2;
};

usage() {
	echo "usage: ${0} [-h] [-v] [platform...]" >&2;
	echo "       -h.........: show this screen" >&2;
	echo "       -v.........: be verbose" >&2;
	echo "       platform...: one of: \`${NWJS_PLATFORMS}'" >&2;
};

main() {
	local _cmd="" _opt="" _platform="" _platforms="" _vflag=0;
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
	_platforms="${@}"; mkdir -p "${RELEASES_DNAME}";
	for _platform in ${_platforms:-${NWJS_PLATFORMS}}; do
		msgf "Building ${_platform} release...";
		if [ "${_vflag:-0}" -eq 0 ]; then
			deploy "${_platform}" "${_vflag}" >/dev/null;
		else
			deploy "${_platform}" "${_vflag}";
		fi;
		msgf "Built ${_platform} release.";
	done;
};

set -o errexit -o noglob;
main "${@}";

# vim:foldmethod=marker sw=8 ts=8 tw=120
