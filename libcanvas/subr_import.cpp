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

#include <errno.h>

#include <algorithm>
#include <array>
#include <map>
#include <regex>
#include <stdexcept>
#include <string>

#include "../librtl/rtldef.hpp"
#include "Canvas.hpp"

/*
 * Private variables
 */

static std::map<unsigned, unsigned> s_ANSi_bg_map = {
	{107, 0},	// Bright White
	{40, 1},	// Black
	{44, 2},	// Blue
	{42, 3},	// Green
	{101, 4},	// Red
	{41, 5},	// Light Red
	{45, 6},	// Pink
	{43, 7},	// Yellow
	{103, 8},	// Light Yellow
	{102, 9},	// Light Green
	{46, 10},	// Cyan
	{106, 11},	// Light Cyan
	{104, 12},	// Light Blue
	{105, 13},	// Light Pink
	{100, 14},	// Grey
	{47, 15},	// Light Grey
};

static std::map<unsigned, unsigned> s_ANSi_fg_map = {
	{97, 0},	// Bright White
	{30, 1},	// Black
	{34, 2},	// Blue
	{32, 3},	// Green
	{91, 4},	// Red
	{31, 5},	// Light Red
	{35, 6},	// Pink
	{33, 7},	// Yellow
	{93, 8},	// Light Yellow
	{92, 9},	// Light Green
	{36, 10},	// Cyan
	{96, 11},	// Light Cyan
	{94, 12},	// Light Blue
	{95, 13},	// Light Pink
	{90, 14},	// Grey
	{37, 15},	// Light Grey
};

static std::map<unsigned, unsigned> s_ANSi_fg_bold_map = {
	{97, 0},	// Bright White
	{30, 14},	// Grey
	{94, 12},	// Light Blue
	{32, 9},	// Light Green
	{91, 4},	// Light Red
	{31, 4},	// Light Red
	{35, 13},	// Light Pink
	{33, 8},	// Light Yellow
	{93, 8},	// Light Yellow
	{92, 9},	// Light Green
	{36, 11},	// Light Cyan
	{96, 11},	// Light Cyan
	{94, 12},	// Light Blue
	{95, 13},	// Light Pink
	{90, 14},	// Grey
	{37, 0},	// Bright White
};

static std::wregex s_colour_regex(L"\u0003((1[0-5]|0?[0-9])?(?:,(1[0-5]|0?[0-9]))?)", std::regex_constants::ECMAScript);
static std::wregex s_escape_regex(L"\x1b\\[((?:\\d{1,3};?)+m|\\d+[ABCDEFG])", std::regex_constants::ECMAScript);

/*
 * Private subroutines
 */

static bool normaliseCanvasMap(Rtl::STATUS *pstatus, Canvas::CELL_MAP& cell_map, Canvas::SIZE& psize);

static bool
normaliseCanvasMap(
	Rtl::STATUS *		pstatus,
	Canvas::CELL_MAP&	cell_map,
	Canvas::SIZE&		psize
)
{
	Canvas::SIZE	size;
	Rtl::STATUS	status = Rtl::STATUS_NONE_SUCCESS;

	size.h = cell_map.size(), size.w = 0;
	std::for_each(cell_map.begin(), cell_map.end(), [&](auto col){size.w = std::max(size.w, col.size());});
	for (size_t y = 0; y < cell_map.size(); y++) {
		if (cell_map[y].size() != size.w) {
			for (size_t x = cell_map[y].size(); x < size.w; x++)
				cell_map[y].push_back(Canvas::CELL{Canvas::CATTR_NONE, -1, 15, {x, y}, L" "});
		}
	}
	if ((size.h == 0) && (size.w == 0))
		status = Rtl::STATUS_ROAR("empty canvas");
	if (status)
		psize = size;
	return (bool)(*pstatus = status);
}

/*
 * Public class methods
 */

bool
Canvas::importANSi(
	Rtl::STATUS&		pstatus,
	const std::wstring&	data
)
{
	unsigned long				ansiCode;
	std::wstring::size_type			ansiCode_pos, ansiCode_pos_last = 0;
	std::wstring				ansiSequence;
	Canvas::CELL_ATTRS			cell_attrs;
	bool					cell_bold_ANSi;
	COLOURS					cell_colours, cell_colours_ANSi;
	Canvas::CELL_MAP			cell_map;
	Canvas::CELL_LIST			cell_row;
	std::array<std::wstring, 2>		escape_regex_matches;
	std::match_results<const wchar_t *>	escape_regex_match_results;
	std::wstring::size_type			line_begin, line_end;
	Canvas::POINT				point = {0, 0};
	std::wstring::size_type			pos, pos_last = 0;
	Canvas::SIZE				size;
	Rtl::STATUS				status = Rtl::STATUS_NONE_SUCCESS;

	try {
		do {
			pos = data.find(L"\n", pos_last);
			cell_attrs = Canvas::CATTR_NONE, cell_colours = {-1, 15}, cell_row = Canvas::CELL_LIST(), point.x = 0;
			cell_bold_ANSi = false, cell_colours_ANSi = {30, 37};
			if (pos != std::wstring::npos)
				line_end = ((pos > 0) && (data[pos - 1] == L'\r')) ? (pos - 1) : pos;
			else
				line_end = data.length();
			for (std::wstring::size_type nch = line_begin = ((pos_last != std::wstring::npos) ? pos_last : data.length()); nch < line_end; nch++) {
				if (std::regex_search(&data[nch], escape_regex_match_results, s_escape_regex)) {
					for (std::match_results<const wchar_t *>::size_type nmatch = 0; nmatch < escape_regex_match_results.size(); nmatch++)
						escape_regex_matches[nmatch] = escape_regex_match_results[nmatch].str();
					if (escape_regex_matches[1].back() == L'C') {
						cell_row.push_back(Canvas::CELL{cell_attrs, cell_colours.bg, cell_colours.fg, point, L" "}), point.x++;
					} else if (escape_regex_matches[1].back() == L'm') {
						ansiSequence = escape_regex_matches[1].substr(0, escape_regex_matches[1].length() - 1);
						do {
							ansiCode_pos = ansiSequence.find(L";", ansiCode_pos_last);
							switch ((ansiCode = std::stoul(ansiSequence.substr(ansiCode_pos, ansiCode_pos_last - ansiCode_pos)))) {
							case 0:
								cell_bold_ANSi = false, cell_colours = {-1, 15}, cell_colours_ANSi = {30, 37}; break;
							case 1:
								cell_bold_ANSi = true, cell_colours.fg = s_ANSi_fg_bold_map.find(ansiCode)->second; break;
							case 2:
								cell_bold_ANSi = true, cell_colours.fg = s_ANSi_fg_map.find(ansiCode)->second; break;
							case 7:
								std::swap(cell_colours.bg, cell_colours.fg); std::swap(cell_colours_ANSi.bg, cell_colours_ANSi.fg); break;
							default:
								if (!cell_bold_ANSi && (s_ANSi_fg_bold_map.find(ansiCode) != s_ANSi_bg_map.end())) {
									cell_colours_ANSi.bg = ansiCode, cell_colours.bg = s_ANSi_bg_map.find(ansiCode)->second;
								} else if (cell_bold_ANSi && (s_ANSi_fg_bold_map.find(ansiCode) != s_ANSi_fg_bold_map.end())) {
									cell_colours_ANSi.fg = ansiCode, cell_colours.fg = s_ANSi_fg_bold_map.find(ansiCode)->second;
								} else if (!cell_bold_ANSi && (s_ANSi_fg_map.find(ansiCode) != s_ANSi_fg_map.end())) {
									cell_colours_ANSi.fg = ansiCode, cell_colours.fg = s_ANSi_fg_map.find(ansiCode)->second;
								} else if (cell_bold_ANSi && (s_ANSi_fg_map.find(ansiCode) != s_ANSi_fg_map.end())) {
									cell_colours_ANSi.fg = ansiCode, cell_colours.fg = s_ANSi_fg_bold_map.find(ansiCode)->second;
								}
								break;
							}
						} while (ansiCode_pos != std::wstring::npos);
					}
					nch += (escape_regex_match_results[0].length() - 1);
				} else
					cell_row.push_back(Canvas::CELL{cell_attrs, cell_colours.bg, cell_colours.fg, point, data[nch]}), point.x++; break;
			}
			cell_map.push_back(cell_row); point.y++;
			if (pos != std::wstring::npos)
				pos_last = pos + 1;
		} while ((pos != std::wstring::npos) && (pos_last < data.length()));
	}
	catch (std::bad_alloc) {
		status = Rtl::STATUS_POSIX(ENOMEM); /* XXX */
	}
	catch (std::invalid_argument) {
		status = Rtl::STATUS_POSIX(EINVAL); /* XXX */
	}
	catch (std::out_of_range) {
		status = Rtl::STATUS_POSIX(ERANGE); /* XXX */
	}
	if (status && normaliseCanvasMap(&status, cell_map, size))
		this->import(status, cell_map, size);
	return (bool)(pstatus = status);
}

bool
Canvas::importMiRC(
	Rtl::STATUS&		pstatus,
	const std::wstring&	data
)
{
	Canvas::CELL_ATTRS			cell_attrs;
	COLOURS					cell_colours;
	Canvas::CELL_MAP			cell_map;
	Canvas::CELL_LIST			cell_row;
	std::array<std::wstring, 4>		colour_regex_matches;
	std::match_results<const wchar_t *>	colour_regex_match_results;
	std::wstring::size_type			line_begin, line_end;
	Canvas::POINT				point = {0, 0};
	std::wstring::size_type			pos, pos_last = 0;
	Canvas::SIZE				size;
	Rtl::STATUS				status = Rtl::STATUS_NONE_SUCCESS;

	try {
		do {
			pos = data.find(L"\n", pos_last);
			cell_attrs = Canvas::CATTR_NONE, cell_colours = {-1, 15}, cell_row = Canvas::CELL_LIST(), point.x = 0;
			if (pos != std::wstring::npos)
				line_end = ((pos > 0) && (data[pos - 1] == L'\r')) ? (pos - 1) : pos;
			else
				line_end = data.length();
			for (std::wstring::size_type nch = line_begin = ((pos_last != std::wstring::npos) ? pos_last : data.length()); nch < line_end; nch++) {
				switch (data[nch]) {
				case '\x02':
					cell_attrs = (Canvas::CELL_ATTRS)((cell_attrs & Canvas::CATTR_BOLD) ? (cell_attrs & ~Canvas::CATTR_BOLD) : (cell_attrs | Canvas::CATTR_BOLD)); break;
				case '\x03':
					if (std::regex_search(&data[nch], colour_regex_match_results, s_colour_regex)) {
						for (std::match_results<const wchar_t *>::size_type nmatch = 0; nmatch < colour_regex_match_results.size(); nmatch++)
							colour_regex_matches[nmatch] = colour_regex_match_results[nmatch].str();
						if ((colour_regex_matches[2] != L"") && (colour_regex_matches[3] != L"")) {
							cell_colours = {(COLOUR)std::stoull(colour_regex_matches[3]), (COLOUR)std::stoull(colour_regex_matches[2])};
						} else if ((colour_regex_matches[2] != L"") && (colour_regex_matches[3] == L"")) {
							cell_colours.fg = (COLOUR)std::stoull(colour_regex_matches[2]);
						} else if ((colour_regex_matches[2] == L"") && (colour_regex_matches[3] != L"")) {
							cell_colours.bg = (COLOUR)std::stoull(colour_regex_matches[3]);
						} else
							cell_colours = {-1, 15};
						nch += colour_regex_match_results[1].length();
					} else
						cell_colours = {-1, 15};
					break;
				case '\x06':
					cell_attrs = (Canvas::CELL_ATTRS)((cell_attrs & Canvas::CATTR_ITALIC) ? (cell_attrs & ~Canvas::CATTR_ITALIC) : (cell_attrs | Canvas::CATTR_ITALIC)); break;
				case '\x0f':
					cell_attrs = Canvas::CATTR_NONE, cell_colours = {-1, 15}; break;
				case '\x16':
					std::swap(cell_colours.bg, cell_colours.fg); break;
				case '\x1f':
					cell_attrs = (Canvas::CELL_ATTRS)((cell_attrs & Canvas::CATTR_UNDERLINE) ? (cell_attrs & ~Canvas::CATTR_UNDERLINE) : (cell_attrs | Canvas::CATTR_UNDERLINE)); break;
				case '\t':
					for (size_t ncell = 0; ncell < 8; ncell++, point.x++)
						cell_row.push_back(Canvas::CELL{cell_attrs, cell_colours.bg, cell_colours.fg, point, L" "});
					break;
				default:
					cell_row.push_back(Canvas::CELL{cell_attrs, cell_colours.bg, cell_colours.fg, point, data[nch]}), point.x++; break;
				}
			}
			cell_map.push_back(cell_row); point.y++, pos_last = pos + 1;
			if (pos != std::wstring::npos)
				pos_last = pos + 1;
		} while ((pos != std::wstring::npos) && (pos_last < data.length()));
	}
	catch (std::bad_alloc) {
		status = Rtl::STATUS_POSIX(ENOMEM); /* XXX */
	}
	catch (std::invalid_argument) {
		status = Rtl::STATUS_POSIX(EINVAL); /* XXX */
	}
	catch (std::out_of_range) {
		status = Rtl::STATUS_POSIX(ERANGE); /* XXX */
	}
	if (status && normaliseCanvasMap(&status, cell_map, size))
		this->import(status, cell_map, size);
	return (bool)(pstatus = status);
}

bool
Canvas::importSAUCE(
	Rtl::STATUS&		pstatus,
	const std::wstring&	data
)
{
	Rtl::STATUS	status = Rtl::STATUS_NONE_SUCCESS;

	(void)data;
	return (bool)(pstatus = status);
}
