/*
 * roar -- mIRC art editor for Windows & Linux
 * Copyright (C) 2018, 2019  Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include "rtldef.hpp"

#ifdef _WIN32
#include <windows.h>
#endif /* _WIN32 */

namespace Rtl {

/*
 * Public class methods
 */

tagStatus::tagStatus(
	STATUS_FACILITY	facility,
	STATUS_SEVERITY	severity
)
{
	if ((severity == SSEVERITY_ERROR) && (facility == SFACILITY_POSIX))
		this->cond = errno;
#ifdef _WIN32
	else if ((severity == SSEVERITY_ERROR) && (facility == SFACILITY_WINDOWS))
		this->cond = GetLastError();
#endif /* _WIN32 */
	this->facility = facility, this->severity = severity;
}

/*
 * Public functions
 */

bool
convert_wstring(STATUS *pstatus, const std::wstring& ws, std::string& s)
{
	int size_new;
	STATUS status = STATUS_NONE_SUCCESS;
	const wchar_t *ws_c_str;
	size_t ws_len;

#ifdef _WIN32
	if (!(size_new = WideCharToMultiByte(CP_UTF8, 0, (ws_c_str = ws.c_str()), (int)(ws_len = ws.length() + 1), NULL, 0, NULL, NULL)))
		status = STATUS_WINDOWS_GLE();
#elif defined(__linux__)
	if (!(size_new = wcstombs(NULL, (ws_c_str = ws.c_str()), (ws_len = ws.length() + 1))))
		status = STATUS_POSIX_ERRNO();
#endif /* defined(_WIN32), defined(__linux__) */
	else {
		try {
			s.resize(size_new);
#ifdef _WIN32
			if (!WideCharToMultiByte(CP_UTF8, 0, ws_c_str, (int)ws_len, &s[0], size_new, NULL, NULL))
				status = STATUS_WINDOWS_GLE();
#elif defined(__linux__)
			if (!wcstombs(&s[0], ws_c_str, ws_len))
				status = STATUS_POSIX_ERRNO();
#endif /* defined(_WIN32), defined(__linux__) */
			else
				s.resize(size_new - 1);
		}
		catch (std::bad_alloc) {
			status = STATUS_POSIX(ENOMEM);
		}
	}
	return (bool)(*pstatus = status);
}

bool
convert_cstring(STATUS *pstatus, const std::string& s, std::wstring& ws)
{
	const char *s_c_str;
	int size_new;
	size_t s_len;
	STATUS status = STATUS_NONE_SUCCESS;

#ifdef _WIN32
	if (!(size_new = MultiByteToWideChar(CP_UTF8, 0, (s_c_str = s.c_str()), (int)(s_len = s.length() + 1), NULL, 0)))
		status = STATUS_WINDOWS_GLE();
#elif defined(__linux__)
	if (!(size_new = mbstowcs(NULL, (s_c_str = s.c_str()), (s_len = s.length() + 1))))
		status = STATUS_POSIX_ERRNO();
#endif /* defined(_WIN32), defined(__linux__) */
	else {
		try {
			ws.resize(size_new);
#ifdef _WIN32
			if (!MultiByteToWideChar(CP_UTF8, 0, s_c_str, (int)s_len, &ws[0], size_new))
				status = STATUS_WINDOWS_GLE();
#elif defined(__linux__)
			if (!mbstowcs(&ws[0], s_c_str, s_len))
				status = STATUS_POSIX_ERRNO();
#endif /* defined(_WIN32), defined(__linux__) */
			else
				ws.resize(size_new - 1);
		}
		catch (std::bad_alloc) {
			status = STATUS_POSIX(ENOMEM);
		}
	}
	return (bool)(*pstatus = status);
}

#ifdef _WIN32
const std::wstring
#elif defined(__linux__)
const std::string
#endif /* defined(_WIN32), defined(__linux__) */
perror(STATUS status)
{
#ifdef _WIN32
	const wchar_t *msg;
#endif /* _WIN32 */

	if (status)
#ifdef _WIN32
		return L"success";
#elif defined(__linux__)
		return "success";
#endif /* defined(_WIN32), defined(__linux__) */
	else switch (status.facility) {
#ifdef _WIN32
	case SFACILITY_POSIX:
		return _wcserror(status.cond);
	case SFACILITY_WINDOWS:
		FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM, NULL,
			      status.cond, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), (LPWSTR)&msg, 0, NULL);
		return msg;
#elif defined(__linux__)
	case SFACILITY_POSIX:
		return strerror(status.cond);
#endif /* defined(_WIN32), defined(__linux__) */
	case SFACILITY_ROAR:
		return status.msg;
	default:
#ifdef _WIN32
		return L"(unknown facility)";
#elif defined(__linux__)
		return "(unknown facility)";
#endif /* defined(_WIN32), defined(__linux__) */
	}
}

std::chrono::high_resolution_clock::time_point
timeBegin(
)
{
	return std::chrono::high_resolution_clock::now();
}

void
timeEnd(
	const char *					pfx,
	std::chrono::high_resolution_clock::time_point	t0
)
{
	printf(pfx);
	printf(": %.2f ms\n", (float)std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - t0).count());
}

}
