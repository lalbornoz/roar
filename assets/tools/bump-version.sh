#!/bin/sh
#

RELEASE_DEPS="rsync sed";

rc() {
	local _cmd="${1}"; shift;
	printf "%s >>> %s %s\n" "$(date +"%d-%^b-%Y %H:%M:%S")" "${_cmd}" "${*}";
	"${_cmd}" "${@}";
};

usage() {
	echo "usage: ${0} [-h] old_version new_version" >&2;
	echo "       -h.........: show this screen" >&2;
};

main() {
	local _opt="" _version_new="" _version_new_code="" _version_old="";
	while getopts hv _opt; do
	case "${_opt}" in
	h) usage; exit 0; ;;
	*) usage; exit 1; ;;
	esac; done;
	shift $((${OPTIND}-1));
	if [ -z "${1}" ]; then
		echo "error: empty or missing old version number argument" >&2; usage; exit 1;
	elif [ -z "${2}" ]; then
		echo "error: empty or missing new version number argument" >&2; usage; exit 1;
	else
		_version_old="${1}"; _version_new="${2}";
		_version_new_code="$(echo "${_version_new}" | sed -e 's,\.,,g' -e 's/^[0-9]/&00/')";
	fi;
	for _cmd in ${RELEASE_DEPS_CMD}; do
		if ! which "${_cmd}" >/dev/null; then
			echo "error: missing prerequisite command \`${_cmd}'";
			exit 1;
		fi;
	done;
	rc sed -i"" '/"version":/s/\("version":\s*\)"'"${_version_old}"'"/\1"'"${_version_new}"'"/'		\
		MiRCART-nw/package.json										\
		MiRCART-nw/package-lock.json;
	rc sed -i"" '/<title>[^<]\+ v/s/\(<title>[^<]\+ v\)'"${_version_old}"'\(.*<\)/\1'"${_version_new}"'\2/'	\
		assets/html/help.html assets/html/index.html;
	rc git commit -avm "Bump to v${_version_new}.";
};

set -o errexit -o noglob;
main "${@}";

# vim:foldmethod=marker sw=8 ts=8 tw=120
