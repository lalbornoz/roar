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

#include <cwctype>
#include <string>

#include "../librtl/rtldef.hpp"
#include "Canvas.hpp"

/*
 * Private subroutines
 */

static void encodeMiRCColours(std::wstring& buffer, const Canvas::CELL& cell, bool bgfl, bool fgfl);
static bool flipBit(const Canvas::CELL& cell, Canvas::CELL& state, Canvas::CELL_ATTRS bit);

static void
encodeMiRCColours(
	std::wstring&		buffer,
	const Canvas::CELL&	cell,
	bool			bgfl,
	bool			fgfl
)
{
	bool	paddingfl = iswdigit(cell.txt[0]);

	if ((bgfl && (cell.bg == -1)) && (fgfl && (cell.fg == -1)))
		buffer += L"\u000f";
	else if (!bgfl && (fgfl && (cell.fg != -1))) {
		if (!paddingfl || (cell.fg < 10))
			buffer += std::wstring(L"\u0003") + std::to_wstring((unsigned)cell.fg);
		else
			buffer += std::wstring(L"\u0003") + L"0" + std::to_wstring((unsigned)cell.fg);
	} else if ((bgfl && (cell.bg == -1)) && (fgfl && (cell.fg != -1))) {
		if (!paddingfl || (cell.fg < 10))
			buffer += std::wstring(L"\u0003\u0003") + std::to_wstring((unsigned)cell.fg);
		else
			buffer += std::wstring(L"\u0003\u0003") + L"0" + std::to_wstring((unsigned)cell.fg);
	} else if ((bgfl && (cell.bg != -1)) && (cell.fg != -1)) {
		if (!paddingfl || (cell.bg < 10))
			buffer += L"\u0003" + std::to_wstring((unsigned)cell.fg) + L"," + std::to_wstring((unsigned)cell.bg);
		else
			buffer += L"\u0003" + std::to_wstring((unsigned)cell.fg) + L",0" + std::to_wstring((unsigned)cell.bg);
	}
}

static bool
flipBit(
	const Canvas::CELL&	cell,
	Canvas::CELL&		state,
	Canvas::CELL_ATTRS	bit
)
{
	bool	rc = false;

	if ((cell.attrs & bit) && !(state.attrs & bit))
		rc = true, state.attrs |= bit;
	else if (!(cell.attrs & bit) && (state.attrs & bit))
		rc = true, state.attrs &= (Canvas::CELL_ATTRS)~bit;
	return rc;
}

/*
 * Public class methods
 */

bool
Canvas::exportANSi(
	Rtl::STATUS&	pstatus,
	std::wstring&	buffer
)
{
	Rtl::STATUS	status = Rtl::STATUS_POSIX(ENOSYS);

	(void)buffer;
	return (bool)(pstatus = status);
}

bool
Canvas::exportMiRC(
	Rtl::STATUS&	pstatus,
	std::wstring&	buffer
)
{
	Canvas::CELL	state;
	Rtl::STATUS	status = Rtl::STATUS_NONE_SUCCESS;

	printf("%zu rows\n", this->size.h);
	for (Canvas::COORD y = 0; y < this->size.h; y++) {
		state = Canvas::CELL{Canvas::CATTR_NONE, -1, 15, {0, 0}, L" "};
		for (Canvas::COORD x = 0; x < this->size.w; x++) {
			const auto& cell = this->cells[y][x];
			if (flipBit(cell, state, Canvas::CATTR_BOLD))
				buffer += L"\u0002";
			if (flipBit(cell, state, Canvas::CATTR_ITALIC))
				buffer += L"\u001d";
			if (flipBit(cell, state, Canvas::CATTR_UNDERLINE))
				buffer += L"\u001f";
			if ((cell.bg != state.bg) && (cell.fg != state.fg))
				encodeMiRCColours(buffer, cell, true, true), state.bg = cell.bg, state.fg = cell.fg;
			else if ((cell.bg != state.bg) && (cell.fg == state.fg))
				encodeMiRCColours(buffer, cell, true, false), state.bg = cell.bg;
			else if ((cell.bg == state.bg) && (cell.fg != state.fg))
				encodeMiRCColours(buffer, cell, false, true), state.fg = cell.fg;
			buffer += cell.txt;
		}
		buffer += L"\n";
	}
	if (buffer.length() == 0)
		status = Rtl::STATUS_ROAR("empty canvas");
	return (bool)(pstatus = status);
}

bool
Canvas::exportSAUCE(
	Rtl::STATUS&	pstatus,
	std::wstring&	buffer
)
{
	Rtl::STATUS	status = Rtl::STATUS_POSIX(ENOSYS);

	(void)buffer;
	return (bool)(pstatus = status);
}
