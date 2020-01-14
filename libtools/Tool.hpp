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

#ifndef _TOOL_HPP_
#define _TOOL_HPP_

#include <string>
#include <utility>

#include "../libcanvas/Canvas.hpp"

/*
 * Public types
 */

class Tool {
public:
	typedef enum drag_status_e {
		DSTATUS_NONE	= 0,
		DSTATUS_BEGIN	= 1,
		DSTATUS_MOVE	= 2,
		DSTATUS_SET	= 3,
	}		DRAG_STATUS;
	typedef enum mouse_button_e {
		MBUTTON_NONE	= 0,
		MBUTTON_LEFT	= 1,
		MBUTTON_MIDDLE	= 2,
		MBUTTON_RIGHT	= 3,
	}		MOUSE_BUTTON;
	typedef struct drag_state_e {
		MOUSE_BUTTON	button;
		Canvas::POINT	begin, set;
		DRAG_STATUS	status;
	}		DRAG_STATE;
	#define DRAG_STATE_EMPTY	Tool::MBUTTON_NONE, {0, 0}, {0, 0}, Tool::DSTATUS_NONE
	typedef std::pair<Canvas::CELL_LIST, Canvas::CELL_LIST>
			TOOL_CELLS_PAIR;
	typedef Rtl::Either<bool, TOOL_CELLS_PAIR>
			TOOL_CELLS;

	Tool(const std::wstring& name) : name(name) {};
	virtual TOOL_CELLS click(Canvas::BRUSH brush, Canvas::POINT& brushPos, Tool::MOUSE_BUTTON button, const Canvas& canvas, Canvas::POINT pos) = 0;
	virtual TOOL_CELLS drag(Canvas::BRUSH brush, Canvas::POINT& brushPos, const Canvas& canvas, DRAG_STATE dragState, Canvas::POINT pos) = 0;
	virtual TOOL_CELLS key(Canvas::BRUSH brush, Canvas::POINT& brushPos, const Canvas& canvas, wchar_t key, wchar_t modifiers) = 0;
	virtual TOOL_CELLS cursor(Canvas::BRUSH brush, Canvas::POINT& brushPos, const Canvas& canvas, Canvas::POINT pos) = 0;

	const std::wstring	name;
};

#endif /* _TOOL_HPP_ */
