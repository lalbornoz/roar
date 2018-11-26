#!/bin/sh
#

CORDOBA_PLATFORMS="android";
PACKAGE_NAME="MiRCART-cordoba";
RELEASE_DEPS_CMD="cordova cp";
RELEASE_DEPS_ENV="ANDROID_HOME JAVA_HOME";
RELEASES_DNAME_DEST="releases";
RELEASES_DNAME_SRC="platforms/%CORDOBA_PLATFORM%/app/build/outputs/apk";

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
	local _platform="${1}" _vflag="${2}" _release_dname_src="" _release_type="" _release_version="";

	_release_dname_src="$(subst "${RELEASES_DNAME_SRC}" "%CORDOBA_PLATFORM%" "${_platform}")";
	_release_version="$(sed -n '/^\s*"version":/s/^.*:\s*"\([0-9.]\+\)",\?\s*$/\1/p' package.json)";
	for _release_type in debug release; do
		cordova build "--${_release_type}" --device "${_platform}";
		cp -a	"$(find "${_release_dname_src}/${_release_type}" -name \*.apk)"	\
			"${RELEASES_DNAME_DEST}/${PACKAGE_NAME}-${_release_type}-${_release_version}.apk";
	done;
};

usage() {
	echo "usage: ${0} [-h] [-v] [platform...]" >&2;
	echo "       -h.........: show this screen" >&2;
	echo "       -v.........: be verbose" >&2;
	echo "       platform...: one of: \`${CORDOBA_PLATFORMS}'" >&2;
};

main() {
	local _cmd="" _opt="" _platform="" _platforms="" _vflag=0 _vname="";
	while getopts hv _opt; do
	case "${_opt}" in
	h) usage; exit 0; ;;
	v) _vflag=1; ;;
	*) usage; exit 1; ;;
	esac; done;
	shift $((${OPTIND}-1));
	for _cmd in ${RELEASE_DEPS_CMD}; do
		if ! which "${_cmd}" >/dev/null; then
			echo "error: missing prerequisite command \`${_cmd}'";
			exit 1;
		fi;
	done;
	for _vname in ${RELEASE_DEPS_ENV}; do
		if [ -z "$(eval echo \"\${_vname}\")" ]; then
			echo "error: missing prerequisite environment variable \`${_vname}'";
			exit 1;
		fi;
	done;
	_platforms="${@}"; mkdir -p "${RELEASES_DNAME_DEST}";
	for _platform in ${_platforms:-${CORDOBA_PLATFORMS}}; do
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
