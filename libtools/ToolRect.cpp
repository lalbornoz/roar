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

#include "ToolRect.hpp"

/*
 * Private subroutine prototypes
 */

static Canvas::CELL_LIST drawRect(Canvas::BRUSH brush, Canvas::RECT rect);

/*
 * Private subroutines
 */

static Canvas::CELL_LIST
drawRect(
	Canvas::BRUSH	brush,
	Canvas::RECT	rect
)
{
	Canvas::CELL_LIST	cells;
	Canvas::COLOUR		colour;

	for (Canvas::COORD y = rect.p0.y, y_limit = (rect.p1.y + 1); y < y_limit; y++) {
		for (Canvas::COORD x = rect.p0.x, x_limit = (rect.p1.x + 1); x < x_limit; x++) {
			if (((x == rect.p0.x) || ((x_limit > x) && (x == (x_limit - 1))))
			||  ((y == rect.p0.y) || ((y_limit > y) && (y == (y_limit - 1)))))
				colour = brush.colours.fg;
			else
				colour = brush.colours.bg;
			cells.push_back(Canvas::CELL{Canvas::CATTR_NONE, colour, colour, {x, y}, L" "});
		}
	}
	return cells;
}

/*
 * Public class functions
 */

Tool::TOOL_CELLS
ToolRect::click(
	Canvas::BRUSH		brush,
	Canvas::POINT&		brushPos,
	Tool::MOUSE_BUTTON	button,
	const Canvas&		canvas,
	Canvas::POINT		pos
)
{
	Canvas::CELL_LIST	cells;
	Canvas::RECT		rect{pos, {pos.x + brush.size.w, pos.y + brush.size.h}};

	(void)canvas;
	brushPos = pos;
	if (button == Tool::MBUTTON_RIGHT)
		std::swap(brush.colours.bg, brush.colours.fg);
	cells = drawRect(brush, rect);
	return Tool::TOOL_CELLS(true, Tool::TOOL_CELLS_PAIR(cells, cells));
}

Tool::TOOL_CELLS
ToolRect::cursor(
	Canvas::BRUSH		brush,
	Canvas::POINT&		brushPos,
	const Canvas&		canvas,
	Canvas::POINT		pos
)
{
	Canvas::RECT	rect{pos, {pos.x + brush.size.w, pos.y + brush.size.h}};

	(void)canvas;
	brushPos = pos;
	return Tool::TOOL_CELLS(true, Tool::TOOL_CELLS_PAIR(Canvas::CELL_LIST(), drawRect(brush, rect)));
}

Tool::TOOL_CELLS
ToolRect::drag(
	Canvas::BRUSH		brush,
	Canvas::POINT&		brushPos,
	const Canvas&		canvas,
	DRAG_STATE		dragState,
	Canvas::POINT		pos
)
{
	Canvas::CELL_LIST	cells, cellsCursor;

	(void)canvas;
	switch (dragState.status) {
	case Tool::DSTATUS_BEGIN:
	case Tool::DSTATUS_MOVE:
		if (dragState.button == Tool::MBUTTON_RIGHT)
			std::swap(brush.colours.bg, brush.colours.fg);
		cellsCursor = drawRect(brush, Canvas::RECT{dragState.begin, pos}); break;
	case Tool::DSTATUS_SET:
		if (dragState.button == Tool::MBUTTON_RIGHT)
			std::swap(brush.colours.bg, brush.colours.fg);
		cells = cellsCursor = drawRect(brush, Canvas::RECT{dragState.begin, dragState.set}); break;
	default:
		break;
	}
	brushPos = pos;
	return Tool::TOOL_CELLS(true, Tool::TOOL_CELLS_PAIR(cells, cellsCursor));
}
