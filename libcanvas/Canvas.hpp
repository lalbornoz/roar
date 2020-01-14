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

#ifndef _CANVAS_HPP_
#define _CANVAS_HPP_

#include <stdint.h>
#include <wchar.h>

#include <vector>

#include "../librtl/rtldef.hpp"

/*
 * Public types
 */

class Canvas {
public:
	typedef int32_t		COLOUR;
	#define COLOUR_ALPHA(colour)\
				(((colour) >> 24) & 0xff)
	typedef struct colours_s {
		COLOUR		bg, fg;
	} COLOURS;
	typedef std::vector<std::vector<uint8_t>>
				COLOUR_LIST;

	typedef uint64_t	COORD;
	typedef struct point_s {
		COORD		x, y;
	} POINT;
	#define POINT_EMPTY	{0ULL, 0ULL}

	typedef enum cell_attrs_e : unsigned long {
		CATTR_NONE	= 0x00,
		CATTR_BOLD	= 0x01,
		CATTR_ITALIC	= 0x02,
		CATTR_UNDERLINE	= 0x04,
	} CELL_ATTRS;

	typedef struct cell_s {
		CELL_ATTRS	attrs;
		COLOUR		bg, fg;
		POINT		p;
		wchar_t		txt[8];
	} CELL;
	#define CELL_EMPTY	{CATTR_NONE, 0UL, 0UL, POINT_EMPTY, {L'\0',}}
	typedef std::vector<CELL>
				CELL_LIST;
	typedef std::vector<CELL_LIST>
				CELL_MAP;

	typedef enum data_type_e {
		DTYPE_ANSI	= 1,
		DTYPE_MIRC	= 2,
		DTYPE_SAUCE	= 3,
	} DATA_TYPE;

	typedef struct rect_s {
		POINT		p0, p1;
	} RECT;
	#define RECT_EMPTY	{POINT_EMPTY, POINT_EMPTY}
	#define RECT_HEIGHT(r)	((r).p1.y - (r).p0.y)
	#define RECT_WIDTH(r)	((r).p1.x - (r).p0.x)

	typedef struct size_s {
		uint64_t	w, h;
	} SIZE;
	#define SIZE_EMPTY	{0ULL, 0ULL}

	typedef struct brush_e {
		COLOURS		colours;
		SIZE		size;
	}			BRUSH;

	typedef struct undo_cells_e {
		size_t			index, size;
		std::vector<CELL_LIST>	redoList;
		std::vector<CELL_LIST>	undoList;
	}			UNDO_CELLS;
	#define UNDO_CELLS_EMPTY\
				0, 0, std::vector<CELL_LIST>(), std::vector<CELL_LIST>()

	Canvas(SIZE size);
	bool commit(const CELL_LIST& cells, bool inhibitUndo);
	bool export_(Rtl::STATUS& pstatus, std::wstring& buffer, DATA_TYPE type);
	bool import(Rtl::STATUS& pstatus, CELL_MAP& cells, SIZE size);
	bool import(Rtl::STATUS& pstatus, const std::wstring& data, DATA_TYPE type);
	const CELL_LIST *redo();
	const CELL_LIST *undo();

	/* subr_export.cpp */
	bool exportANSi(Rtl::STATUS& pstatus, std::wstring& buffer);
	bool exportMiRC(Rtl::STATUS& pstatus, std::wstring& buffer);
	bool exportSAUCE(Rtl::STATUS& pstatus, std::wstring& buffer);

	/* subr_import.cpp */
	bool importANSi(Rtl::STATUS& pstatus, const std::wstring& data);
	bool importMiRC(Rtl::STATUS& pstatus, const std::wstring& data);
	bool importSAUCE(Rtl::STATUS& pstatus, const std::wstring& data);

	CELL_MAP		cells;
	UNDO_CELLS		cellsUndo;
	SIZE			size;
};

constexpr Canvas::CELL_ATTRS operator&=(Canvas::CELL_ATTRS& lhs, const Canvas::CELL_ATTRS& rhs) {
	return lhs = static_cast<Canvas::CELL_ATTRS>(static_cast<unsigned long>(lhs) & static_cast<unsigned long>(rhs));
};

constexpr Canvas::CELL_ATTRS operator&=(Canvas::CELL_ATTRS& lhs, const unsigned long& rhs) {
	return lhs = static_cast<Canvas::CELL_ATTRS>(static_cast<unsigned long>(lhs) & static_cast<Canvas::CELL_ATTRS>(rhs));
};

constexpr Canvas::CELL_ATTRS operator|=(Canvas::CELL_ATTRS& lhs, const Canvas::CELL_ATTRS& rhs) {
	return lhs = static_cast<Canvas::CELL_ATTRS>(static_cast<unsigned long>(lhs) | static_cast<unsigned long>(rhs));
};

constexpr bool operator==(const Canvas::POINT& lhs, const Canvas::POINT& rhs) {
	return (lhs.x == rhs.x) && (lhs.y == rhs.y);
};

constexpr bool operator!=(const Canvas::POINT& lhs, const Canvas::POINT& rhs) {
	return (lhs.x != rhs.x) || (lhs.y != rhs.y);
};

#endif /* _CANVAS_HPP_ */
