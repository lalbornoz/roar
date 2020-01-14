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

#include "ToolCircle.hpp"

/*
 * Public class functions
 */

Tool::TOOL_CELLS
ToolCircle::cursor(
	Canvas::BRUSH		brush,
	Canvas::POINT&		brushPos,
	const Canvas&		canvas,
	Canvas::POINT		pos
)
{
	Canvas::CELL_LIST	cellsCircle;

	(void)canvas;
	cellsCircle.push_back(Canvas::CELL{Canvas::CATTR_NONE, brush.colours.fg, brush.colours.fg, pos, L" "});
	brushPos = pos;
	return Tool::TOOL_CELLS(true, Tool::TOOL_CELLS_PAIR(Canvas::CELL_LIST(), cellsCircle));
}
