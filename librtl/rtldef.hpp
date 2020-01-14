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

#ifndef _RTLDEF_HPP_
#define _RTLDEF_HPP_

#ifdef _MSC_VER
#pragma warning(disable : 26812)
#endif /* _MSC_VER_ */

#include <chrono>
#include <string>
#include <utility>

namespace Rtl {

/*
 * Public Either<T1, T2> definitions
 */

template <typename T1, typename T2>
struct Either {
	T1 left; T2 right;

	Either(T1 left, T2 right) : left {left}, right {right} {};
	constexpr operator T1() const { return this->left; };
	constexpr operator T2() const { return this->right; };
};

/*
 * Public {STATUS,Status<T>} definitions
 */

typedef uint32_t STATUS_COND;

typedef enum tagSTATUS_FACILITY {
	SFACILITY_NONE		= 0,
	SFACILITY_POSIX		= 1,
#ifdef _WIN32
	SFACILITY_WINDOWS	= 2,
#endif /* _WIN32 */
	SFACILITY_ROAR		= 3,
} STATUS_FACILITY;

typedef enum tagSTATUS_SEVERITY : unsigned long {
	SSEVERITY_WARNING	= 0,
	SSEVERITY_SUCCESS	= 1,
	SSEVERITY_ERROR		= 2,
	SSEVERITY_INFO		= 3,
	SSEVERITY_SEVERE	= 4,
} STATUS_SEVERITY;

constexpr STATUS_SEVERITY operator&(STATUS_SEVERITY lhs, STATUS_SEVERITY rhs) {
	return static_cast<STATUS_SEVERITY>(static_cast<unsigned long>(lhs) & static_cast<unsigned long>(rhs));
};

typedef struct tagStatus {
	STATUS_COND		cond;
	STATUS_FACILITY		facility;
	STATUS_SEVERITY		severity;
#ifdef _WIN32
	std::wstring		msg;
#elif defined(__linux__)
	std::string		msg;
#endif /* defined(_WIN32), defined(__linux__) */

	tagStatus() : cond(0), facility(SFACILITY_NONE), severity(SSEVERITY_SUCCESS) {};
	tagStatus(STATUS_SEVERITY severity) : cond(0), facility(SFACILITY_NONE), severity(severity) {};
	tagStatus(STATUS_FACILITY facility, STATUS_SEVERITY severity);
	tagStatus(STATUS_COND cond, STATUS_FACILITY facility, STATUS_SEVERITY severity) : cond(cond), facility(facility), severity(severity) {};
#ifdef _WIN32
	tagStatus(STATUS_FACILITY facility, STATUS_SEVERITY severity, const std::wstring& msg) : cond(0), facility(facility), severity(severity), msg(msg) {};
#elif defined(__linux__)
	tagStatus(STATUS_FACILITY facility, STATUS_SEVERITY severity, const std::string& msg) : cond(0), facility(facility), severity(severity), msg(msg) {};
#endif /* defined(_WIN32), defined(__linux__) */
#ifndef __GNUC__
	constexpr explicit operator bool() const { return (this->severity & 1); };
#else
	explicit operator bool() const { return (this->severity & 1); };
#endif /* __GNUC__ */
} STATUS;

#define STATUS_BIND_LIBC(status, expr)\
				[&]() { auto tmp = (expr); if (tmp < 0) { (status) = Rtl::STATUS_POSIX_ERRNO(); return false; } else { return true; }}()
#define STATUS_BIND_ROAR(status, error, expr)\
				[&]() { auto tmp = (expr); if (!tmp) { (status) = Rtl::STATUS_ROAR(error); return false; } else { return true; }}()
#define STATUS_BIND_TRUE(expr)	[&]() { (expr); return true; }()
#define STATUS_NONE_SUCCESS	STATUS(0, Rtl::SFACILITY_NONE, Rtl::SSEVERITY_SUCCESS)
#define STATUS_POSIX(cond_)	STATUS(cond_, Rtl::SFACILITY_POSIX, Rtl::SSEVERITY_ERROR)
#define STATUS_POSIX_ERRNO()	STATUS((unsigned long)errno, Rtl::SFACILITY_POSIX, Rtl::SSEVERITY_ERROR)
#ifdef _WIN32
#define STATUS_ROAR(msg_)	STATUS(Rtl::SFACILITY_ROAR, Rtl::SSEVERITY_ERROR, L ## msg_)
#elif defined(__linux__)
#define STATUS_ROAR(msg_)	STATUS(Rtl::SFACILITY_ROAR, Rtl::SSEVERITY_ERROR, (msg_))
#endif /* defined(_WIN32), defined(__linux__) */
#ifdef _WIN32
#define STATUS_WINDOWS(cond_)	STATUS(cond_, Rtl::SFACILITY_WINDOWS, Rtl::SSEVERITY_ERROR)
#define STATUS_WINDOWS_GLE()	STATUS(GetLastError(), Rtl::SFACILITY_WINDOWS, Rtl::SSEVERITY_ERROR)
#endif /* _WIN32 */

template <typename T>
struct Status : public Either<STATUS&, T> {
	Status(STATUS& left, T right) : Either<STATUS&, T>(left, right) {};
	constexpr explicit operator bool() const { return (bool)this->left; }
	constexpr operator STATUS() const { return this->left; }

	template<typename Tr>
	constexpr Status<T>& operator=(const Status<Tr>& rhs) {
		return this->left = rhs.left, this->right = rhs.right, *this;
	}
};

template <typename T>
constexpr Status<T&> tie(STATUS& left, T& right) {
	return Status<T&>(left, right);
}

/*
 * Public macros and subroutine prototypes
 */

bool convert_wstring(STATUS *pstatus, const std::wstring& ws, std::string& s);
bool convert_cstring(STATUS *pstatus, const std::string& s, std::wstring& ws);
#ifdef _WIN32
const std::wstring perror(STATUS status);
#elif defined(__linux__)
const std::string perror(STATUS status);
#endif /* defined(_WIN32), defined(__linux__) */
#define setfillw(c, n)	std::setfill((c)) << std::setw(n)
std::chrono::high_resolution_clock::time_point timeBegin();
void timeEnd(const char *pfx, std::chrono::high_resolution_clock::time_point t0);

}

#endif /* _RTLDEF_HPP_ */
