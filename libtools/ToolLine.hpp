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

#ifndef _TOOLLINE_HPP_
#define _TOOLLINE_HPP_

#include "Tool.hpp"

/*
 * Public types
 */

class ToolLine : public Tool {
public:
	ToolLine() : Tool(L"Line") {};

	TOOL_CELLS click(Canvas::BRUSH brush, Canvas::POINT& brushPos, Tool::MOUSE_BUTTON button, const Canvas& canvas, Canvas::POINT pos) {
		(void)brush, (void)brushPos, (void)button, (void)canvas, (void)pos;
		return TOOL_CELLS(false, TOOL_CELLS_PAIR(Canvas::CELL_LIST(), Canvas::CELL_LIST()));
	};
	TOOL_CELLS cursor(Canvas::BRUSH brush, Canvas::POINT& brushPos, const Canvas& canvas, Canvas::POINT pos);
	TOOL_CELLS drag(Canvas::BRUSH brush, Canvas::POINT& brushPos, const Canvas& canvas, DRAG_STATE dragState, Canvas::POINT pos) {
		(void)brush, (void)brushPos, (void)canvas, (void)dragState, (void)pos;
		return TOOL_CELLS(false, TOOL_CELLS_PAIR(Canvas::CELL_LIST(), Canvas::CELL_LIST()));
	};
	TOOL_CELLS key(Canvas::BRUSH brush, Canvas::POINT& brushPos, const Canvas& canvas, wchar_t key, wchar_t modifiers) {
		(void)brush, (void)brushPos, (void)canvas, (void)key, (void)modifiers;
		return TOOL_CELLS(false, TOOL_CELLS_PAIR(Canvas::CELL_LIST(), Canvas::CELL_LIST()));
	};
};

#endif /* _TOOLLINE_HPP_ */
